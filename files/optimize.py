from future.utils import viewitems, viewvalues
from argparse import ArgumentParser
from miasm.analysis.binary import Container
from miasm.analysis.machine import Machine
from miasm.jitter.llvmconvert import *
from llvmlite import ir as llvm_ir
from miasm.expression.simplifications import expr_simp_high_to_explicit
from miasm.analysis.cst_propag import propagate_cst_expr
from miasm.analysis.data_flow import DeadRemoval, merge_blocks, remove_empty_assignblks
from future.utils import viewitems
from miasm.ir.ir import IntermediateRepresentation, AssignBlock

parser = ArgumentParser("LLVM export example")
parser.add_argument("target", help="Target binary")
parser.add_argument("addr", help="Target address")
parser.add_argument("--architecture", "-a", help="Force architecture")
args = parser.parse_args()

# Opening Target File and storing it in a 'Container' object
cont = Container.from_stream(open(args.target, 'rb'))

# Instantiating Disassembler
machine = Machine(args.architecture if args.architecture else cont.arch)
dis = machine.dis_engine(cont.bin_stream, loc_db=cont.loc_db)

# Disassembling and extracting CFG
asmcfg = dis.dis_multiblock(int(args.addr, 0))

# Include this class to specify target function subfunctions calling convention
# since for x86 all arguments are in the stack, we can live this deffinition empty
class IRAX86FuncCalls(machine.ira):
        def call_effects(self, ad, instr):
            call_assignblk = AssignBlock(
            [
               
            ],
            instr
        )
            return [call_assignblk], []


# Extracting IR Archive and IRCFG
ir_arch = IRAX86FuncCalls(cont.loc_db)
ircfg = ir_arch.new_ircfg_from_asmcfg(asmcfg)

# Printing IR before simplification
print('Before Simplification:')
for lbl, irb in viewitems(ircfg.blocks):
    print(irb)


# Simplifying 
deadrm = DeadRemoval(ir_arch)
entry_points = set([dis.loc_db.get_offset_location(args.addr)])
init_infos = ir_arch.arch.regs.regs_init
cst_propag_link = propagate_cst_expr(ir_arch, ircfg, args.addr, init_infos)
deadrm(ircfg)
remove_empty_assignblks(ircfg)
ircfg.simplify(expr_simp_high_to_explicit)

# Printing IR After simplification
print('After Simplification:')
for lbl, irb in viewitems(ircfg.blocks):
    print(irb)

# Instantiate an LLVM context and Function to fill
context = LLVMContext_IRCompilation()
context.ir_arch = ir_arch

func = LLVMFunction_IRCompilation(context, name="test")
func.ret_type = llvm_ir.VoidType()
func.init_fc()

# Initializing Registers for LLVM mock Function (needed to export function)
all_regs = set()
for block in viewvalues(ircfg.blocks):
    for irs in block.assignblks:
        for dst, src in viewitems(irs.get_rw(mem_read=True)):
            elem = src.union(set([dst]))
            all_regs.update(
                x for x in elem
                if x.is_id()
            )
reg2glob = {}
for var in all_regs:
    data = context.mod.globals.get(str(var), None)
    if data is None:
        data = llvm_ir.GlobalVariable(context.mod,  LLVMType.IntType(var.size), name=str(var))
    data.initializer = LLVMType.IntType(var.size)(0)
    func.local_vars_pointers[var.name] = func.builder.alloca(llvm_ir.IntType(var.size), name=var.name)
    print(var.name)
    if var.name in ("ESP", "EBP"):
        value = func.builder.load(data)
        func.builder.store(value, func.local_vars_pointers[var.name])

# IRCFG is imported, without the final "ret void"
func.from_ircfg(ircfg, append_ret=False)

# Finish the function
func.builder.ret_void()

# Extract LLVM IR if needed
#open("out.ll", "w").write(str(func))

# Parsing LLVM IR
M = llvm.parse_assembly(str(func))
M.verify()

# Initialising Native Exporter
llvm.initialize()
llvm.initialize_native_target()
llvm.initialize_native_asmprinter()

# Optimisation to clean value computation
pmb = llvm.create_pass_manager_builder()
pmb.opt_level = 2
pm = llvm.create_module_pass_manager()
pmb.populate(pm)
pm.run(M)

# Generate Binary output
target = llvm.Target.from_default_triple()
target = target.from_triple('i386-pc-linux-gnu')
target_machine = target.create_target_machine()
obj_bin = target_machine.emit_object(M)
obj = llvm.ObjectFileRef.from_data(obj_bin)
open("./dump_full", "w").write(obj_bin)
