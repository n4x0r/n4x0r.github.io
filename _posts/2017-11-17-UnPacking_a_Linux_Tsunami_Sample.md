---
layout: article
title:  "Manually Unpacking Modified UPX Packed Samples"
date:   2017-11-17 06:30
categories: article
tags: [reverse,malware, ELF, packers]
author: n4x0r
---

In this writeup we're going to unpack a Tsunami malware sample packed with a modified version of `UPX`. Hashes of this specific sample are the following:

```c
SHA256: f22ffc07e0cc907f00fd6a4ecee09fe8411225badb2289c1bffa867a2a3bd863
  SHA1: 76584c9a22835353186e753903ee0a853663bd83
   MD5: 171edd284f6a19c6ed3fe010b79c94af
```

In VirusTotal the malware is identified as a Tsunami Variant for the most part:

<div style="text-align:center"><img src ="https://github.com/n4x0r/n4x0r.github.io/raw/master/images/Tsunami/1.png" /></div>
<br/>
If we do some static recon about the file, we can see the following:
<br/>
```c
readelf -lh f22ffc07e0cc907f00fd6a4ecee09fe8411225badb2289c1bffa867a2a3bd863
ELF Header:
  Magic:   7f 45 4c 46 01 01 01 03 00 00 00 00 00 00 00 00 
  Class:                             ELF32
  Data:                              2's complement, little endian
  Version:                           1 (current)
  OS/ABI:                            UNIX - GNU
  ABI Version:                       0
  Type:                              EXEC (Executable file)
  Machine:                           Intel 80386
  Version:                           0x1
  Entry point address:               0xc8da20
  Start of program headers:          52 (bytes into file)
  Start of section headers:          0 (bytes into file)
  Flags:                             0x0
  Size of this header:               52 (bytes)
  Size of program headers:           32 (bytes)
  Number of program headers:         2
  Size of section headers:           40 (bytes)
  Number of section headers:         0
  Section header string table index: 0

Program Headers:
  Type           Offset   VirtAddr   PhysAddr   FileSiz MemSiz  Flg Align
  LOAD           0x000000 0x00c01000 0x00c01000 0x8d1c2 0x8d1c2 R E 0x1000
  LOAD           0x000304 0x0819b304 0x0819b304 0x00000 0x00000 RW  0x1000
```

The binary's string table has been stripped, aswell as the section header table.
In addition, the binary only contains two segments. Based on the number of segments, and the strange base address it holds (0x00c01000) we can assume that the file is packed.
Furthermore, note that the file and size memory for the second `PT_LOAD` segment are set to 0. meaning that when segment will get loaded to memory, there will be a 0x1000 chunk at `0x0819b304` due to segment alignment.

Is common in Linux systems to encounter packed malware with UPX. I then tried to see if I could find the `UPX` magic in the file.

```c
[0x00c8da20]> / UPX
Searching 3 bytes from 0x00000000 to 0xffffffffffffffff: 55 50 58 
Searching 3 bytes in [0xc01000-0xc8e1c2]
hits: 1
0x00c8ddaa hit0_0 .@M{UPX!u>RBuvkk.
[0x00c8da20]> s hit0_0 -2
[0x00c8dda8]> pd 1
            0x00c8dda8  ~   81f955505821   CMP ECX, 0x21585055
[0x00c8dda8]> ? 0x21585055~[6]
"UPX!" 
[0x00c8dda8]> 
```
This is quite interesting because if we try to use the automated unpacking feature of `UPX` we get an error:

```c
upx -d f22ffc07e0cc907f00fd6a4ecee09fe8411225badb2289c1bffa867a2a3bd863
                       Ultimate Packer for eXecutables
                          Copyright (C) 1996 - 2017
UPX 3.94        Markus Oberhumer, Laszlo Molnar & John Reiser   May 12th 2017

        File size         Ratio      Format      Name
   --------------------   ------   -----------   -----------
upx: f22ffc07e0cc907f00fd6a4ecee09fe8411225badb2289c1bffa867a2a3bd863: 
NotPackedException: not packed by UPX

Unpacked 0 files.
```

Threfore, we may be dealing with a custom packer based on a modified version of `UPX`.
We will statically analyse the sample first, then we will continue our analysis with some dynamic analysis. At the end a brief summary of the sample will be discussed. Let's start with static analysis.

<br/>
<br/>
<h2> Static Analysis</h2>
<br/>

If we open the binary with `IDA PRO` we can confirm that the sample is indeed packed:

<br/>
<div style="text-align:center"><img src ="https://github.com/n4x0r/n4x0r.github.io/raw/master/images/Tsunami/2.png" /></div>
<br/>
<div style="text-align:center"><img src ="https://github.com/n4x0r/n4x0r.github.io/raw/master/images/Tsunami/3.png" /></div>
<br/>

There are only 3 identifiable functions. Second and third functions seem straight forward. One allocates a `RWX` page sized chunk, and the latter executes a write syscall and then exits.

<br/>
<div style="text-align:center"><img src ="https://github.com/n4x0r/n4x0r.github.io/raw/master/images/Tsunami/5.png" /></div>
<br/>
<div style="text-align:center"><img src ="https://github.com/n4x0r/n4x0r.github.io/raw/master/images/Tsunami/4.png" /></div>
<br/>

The entry point of the application looks certainly more messier, and by first glance we can assume that it will have a decryptor/decoder functionality.

<br/>
<div style="text-align:center"><img src ="https://github.com/n4x0r/n4x0r.github.io/raw/master/images/Tsunami/6.png" /></div>
<br/>

The first thing that the entrypoint does is calling `0x00C8DC28`, which itself redirects execution to `allocate_rwx_page` and stores the return address (`start+5`) in ebp.

<br/>
<div style="text-align:center"><img src ="https://github.com/n4x0r/n4x0r.github.io/raw/master/images/Tsunami/7.png" /></div>
<br/>
<div style="text-align:center"><img src ="https://github.com/n4x0r/n4x0r.github.io/raw/master/images/Tsunami/8.png" /></div>
<br/>

Note the stub of data on `0x00C8DC31`, we will come back to it later.
Execution then falls into `allocate_rwx_page` function, which as said before just allocates a memory page with `RXW` permissions. This buffer will be allocated at `0x00C8F000`. If the allocation fails, then execution will branch into the `write_message_and_exit` funtion, in which the string `'nandemo wa shiranai wa yo,'` gets printed to `stderr`. On the other hand, if allocation of RWX chunk is sucessfull, execution will pivot back to `start+5`.

After allocating RWX memory, the malware will then proceed to copy and decode a given stub inside it. After a while analysing the code, I got to the conclusion that function `start+5` (entrypoint+5) is the routine the malware uses to decode and copy packer stub. At this point I coudn't do much progress just by static analysis. Therefore, I fired up the debugger ready to do some dynamic analysis.

<br/>
<br/>
<h2> Dynamic Analysis </h2>
<br/>

Now that we have identified what routine the malware uses to decode and copy packer stub, It will be straight forward to trace the malware's first stage, that is to decode some stub inside the RWX chunk by decoding the data block previosly shown. We will try to follow along execution flow until the destination chunk (chunk `0x00c8f000`) of the decoded stub to remain with our analysis. One way this could be achieved would be by setting a hardware breakpoint on execution at the `RXW` chunk. However, we want to find the cleanest possible way to withness the execution transition into the chunk in order to not overlook details about the first malware's pivoting endeavour. 

On the entrypoint routine, after the function `pivot_to_allocate_rwx_pg` we can clearly see that the register context is being saved with a `pusha` instruction. Furthermore, two pointers are loaded into the `esi` and `edi` registers. Those pointers are the stub source address to be decoded, and the destination buffer address to transfer the decoded stub.

<br/>
<div style="text-align:center"><img src ="https://github.com/n4x0r/n4x0r.github.io/raw/master/images/Tsunami/10.png" /></div>
<br/>

Further down `start` we can see the set of instructions in charge of copying data from stub to the destination buffer:

<br/>
<div style="text-align:center"><img src ="https://github.com/n4x0r/n4x0r.github.io/raw/master/images/Tsunami/15.png" /></div>
<br/>

Nevertheless, There are specific bytes that get processed differently. Some of the stub bytes have a many to one relationship with decoded bytes, so that multiple decoded bytes get derived from a single stub byte. Based on this we can assume that the decoding algorithm must be some sort of deflate implementation.
 
<br/>
<div style="text-align:center"><img src ="https://github.com/n4x0r/n4x0r.github.io/raw/master/images/Tsunami/16.png" /></div>
<br/>

We can see that decoding will stop when second argument `stub_size` + first argument `stub_base` == current stub pointer at `esi`. If this condition is true, the function simply returns.

<br/>
<div style="text-align:center"><img src ="https://github.com/n4x0r/n4x0r.github.io/raw/master/images/Tsunami/11.png" /></div>
<br/>

If we put a breakpoint on this `retn` instruction and then resume the application we will get control of execution back when decoding is over.

<br/>
<div style="text-align:center"><img src ="https://github.com/n4x0r/n4x0r.github.io/raw/master/images/Tsunami/12.png" /></div>
<br/>

Upon decoding finalization, decoding routine does not pivot directly to the RWX chunk at `0x00c8f000`, but it returns first to `allocate_rwx_page+49` to then unwind the stack and return to the RWX chunk.

<br/>
<div style="text-align:center"><img src ="https://github.com/n4x0r/n4x0r.github.io/raw/master/images/Tsunami/13.png" /></div>
<br/>

When execution reaches the `0x00C8F000` chunk, we see the following routine:

<br/>
<div style="text-align:center"><img src ="https://github.com/n4x0r/n4x0r.github.io/raw/master/images/Tsunami/14.png" /></div>
<br/>

The main purpose of this routine is to retrieve the `ELF Auxiliar vector` from the stack and copy it into a local stack buffer. The retrieved struture of the Auxiliar vector looks as follows:

<br/>
<div style="text-align:center"><img src ="https://github.com/n4x0r/n4x0r.github.io/raw/master/images/Tsunami/17.png" /></div>
<br/>

Once Auxiliar vector is retrived from stack then `call_read_link` function gets called. This function looks as follows:
 
<br/>
<div style="text-align:center"><img src ="https://github.com/n4x0r/n4x0r.github.io/raw/master/images/Tsunami/18.png" /></div>
<br/>

In this function a series of statistics are retrieved from the current file such as the location of the embedded `Elf` file in the first `PT_LOAD` segment along with 2 more flags used for decoding. Furthermore, the address of the page-aligned end of the first `PT_LOAD` segment is computed and a stack buffer is reserved in order to store decoded stub. After collecting these fields this function proceeds with `stage1` of the decoding process and calls `init_decoding_stage` function. This function looks as follows:

<br/>
<div style="text-align:center"><img src ="https://github.com/n4x0r/n4x0r.github.io/raw/master/images/Tsunami/19.jpg" /></div>
<br/>

This routine is the entry point of what would be the stub decoding stage. the first part of this function calls `set_for_decoding` function . This function gets called with the previously reserved stack buffer dedicated for storing decoded stub and two stub flags as arguments. Function `set_for_decoding` looks as follows:
 
<br/>
<div style="text-align:center"><img src ="https://github.com/n4x0r/n4x0r.github.io/raw/master/images/Tsunami/20.jpg" /></div>
<br/>
 
Based on the flags passed to this function it will copy different values of the stub into a prepared buffer. We see that when stub buffer is ready the decoding function will get called (`start+5`).
If we step into the decoding function we see that the values in `esi` and `edi` registers have changed in comparison with the earlier call to this function:
 
<br/>
<div style="text-align:center"><img src ="https://github.com/n4x0r/n4x0r.github.io/raw/master/images/Tsunami/21.png" /></div>
<br/>

If we continue until our previously saved breakpoint at `retn` instruction we can identify an ELF header and a program header table within the destination buffer after decoding.
  
<br/>
<div style="text-align:center"><img src ="https://github.com/n4x0r/n4x0r.github.io/raw/master/images/Tsunami/22.png" /></div>
<br/>

Once the ELF header and the Program header table of embedded file get decded, execution continues after the call to `set_for_decoding` in the `init_decoding_stage` function.
  
<br/>
<div style="text-align:center"><img src ="https://github.com/n4x0r/n4x0r.github.io/raw/master/images/Tsunami/23.png" /></div>
<br/>

Now that the program header table of embedded executable is decoded the malware is able to parse some of its fields in order to figure out where to load in memory its correspondent segments for sucesfull unpacking. Furthermore, the malware updates it's own `Auxiliar vector` with statistics of the embedded file in order to reuse that same structure on the loading process of the embedded executable. Malware updates `AT_PHNUM` , `AT_PHENT` and `AT_PHDR` fields of the `Auxiliar vector` at this point but it will be updating more fields in the remaining decoding process. After updating the Auxiliar vector, malware calls `ux_exec` function. This function is sort of an `execve` userland implementation which is in charge of loading the embedded executable segments and pivot execution to the `OEP` without interaction with the kernel. This function looks as follows:
  
<br/>
<div style="text-align:center"><img src ="https://github.com/n4x0r/n4x0r.github.io/raw/master/images/Tsunami/24.jpg" /></div>
<br/>

`Ux_exec` function first scans all segments in decoded proram header table in order to find the `CODE` segment( the first `PT_LOAD` segment). Once `CODE` segment has been found, a mmap system call gets invoked via `mmap_gate` function, passing the segment's `p_vaddr` value along with its page aligned `p_memsz` field as arguments. Upon`CODE` segment allocation execution flow enters a loop in which every `PT_LOAD` segments existent in the program header table gets scanned to be decoded. For every `PT_LOAD` segment that is not the `CODE` segment, this loop will call `mmap_gate` function again in order to map the segment.

For every existent `PT_LOAD` segment, a call to `set_for_decoding` is made. We already cover this function previously. Therefore, I will try to avoid redundancy and I will not explain this routine again. After the `set_fo_decoding` call, our breakpoint in the decoding routine gets triggered once again and this time seems to be decoding into the base address of the embedded binary:
  
<br/>
<div style="text-align:center"><img src ="https://github.com/n4x0r/n4x0r.github.io/raw/master/images/Tsunami/25.png" /></div>
<br/>

Once our `retn` breakpoint gets triggered, the destination buffer seems partially decoded:
  
<br/>
<div style="text-align:center"><img src ="https://github.com/n4x0r/n4x0r.github.io/raw/master/images/Tsunami/26.png" /></div>
<br/>

The segments get decoded in rounds, the following screenshot is the second round of the `CODE` segment's decoding, so we can have an idea how the decoding looks like:
 
<br/>
<div style="text-align:center"><img src ="https://github.com/n4x0r/n4x0r.github.io/raw/master/images/Tsunami/27.png" /></div>
<br/>

<br/>
<div style="text-align:center"><img src ="https://github.com/n4x0r/n4x0r.github.io/raw/master/images/Tsunami/28.png" /></div>
<br/>

Upon segment decoding completion, a `mprotect` system call is invoked in order to enforce the original segment's attributes. This is due to the fact that when container chunk was allocated by `mmap` syscall it must had wrtie permissions in order to write the decoded stub into the chunk.
The code also checks if current segment base + size exceeds the end of the `DATA` segment. If that is the case, a chunk will be mmapped after the `DATA` segment, and a `brk` syscall will be invoked. The `brk` system call will initialise a series of pointers that would make the mmap chunk at the end of the data segment being initialised as the `HEAP` segment. `brk` systemcall does not actually allocate any memory, just initialises `program break`, `start_brk` and `end_data`. However, at this very point there is no `HEAP` segment since initially program break = start_brk. Nevertheless, in future malloc calls the program break address will increase and the `HEAP` segment (space between start_brk and program break) will fall within the mmapped chunk at the end of the `DATA` segment.

<br/>
<div style="text-align:center"><img src ="https://github.com/n4x0r/n4x0r.github.io/raw/master/images/Tsunami/29.png" /></div>
<br/>

After `ux_exec` function is done loading all segments of embedded executable, control flow returns back to `init_decoding_stage` after the call to `ux_exec`. There is just one more thing remaining to do before pivoting to OEP, check for a `PT_INTERP` segment. If this segment exists then the embedded executable is a dynamically linked executable, and the `RTLD` must be mapped. The `RTLD` will be opened, read and then a call to `ux_exec` will be done again in order to map the shared object's segments into the right location within the virtual address space. 

<br/>
<div style="text-align:center"><img src ="https://github.com/n4x0r/n4x0r.github.io/raw/master/images/Tsunami/30.png" /></div>
<br/>

So far we covered all steps the packer does for decoding and loading the embedded executable. A brief overview of the packer's functionality is the following:

<br/>
<div style="text-align:center"><img src ="https://github.com/n4x0r/n4x0r.github.io/raw/master/images/Tsunami/prev.png" /></div>
<br/>


At this point we know that the file is fully loaded into its respective virtual address. If we check the mappings we see the following:

<br/>
<div style="text-align:center"><img src ="https://github.com/n4x0r/n4x0r.github.io/raw/master/images/Tsunami/31.png" /></div>
<br/>

In order to retrieve the embedded executable we can use the following IDA script to dump the embedded file succesfully:


```python
import struct

class Elf32Phdr:
    def __init__(self, bytes):
        (self.p_type,
        self.p_offset,
        self.p_vaddr,
        self.p_paddr,
        self.p_filesz,
        self.p_memsz,
        self.p_flags,
        self.p_align,
        ) = struct.unpack("8I", bytes[:0x20])

class ElfEhdr:
    def __init__(self, bytes):
         (self.e_type,
         self.e_machine,
         self.e_version,
         self.e_entry,
         self.e_phoff,
         self.e_shoff,
         self.e_flags,
         self.e_ehsize,
         self.e_phentsize,
         self.e_phnum,
         self.e_shentsize,
         self.e_shnum,
         self.e_shstrndx) = struct.unpack("2H5I6H", bytes[16:52])
     
    def __str__(self):
         return struct.pack("2H5I6H",
         self.e_type,
         self.e_machine,
         self.e_version,
         self.e_entry,
         self.e_phoff,
         self.e_shoff,
         self.e_flags,
         self.e_ehsize,
         self.e_phentsize,
         self.e_phnum,
         self.e_shentsize,
         self.e_shnum,
         self.e_shstrndx) 

def dumpElf(image_base):
    file = open("/Users/n4x0r/Desktop/dumped.elf", 'wb')
    bytes = GetManyBytes(image_base, 0x100)
    
    ehdr  = ElfEhdr(bytes) 
    phoff = ehdr.e_phoff
    phnum = ehdr.e_phnum
    phdrtbl = bytes[phoff:]

    ehdr.e_shoff = 0
    ehdr.e_shnum = 0
    ehdr.e_shstrndx = 0
    
    for n in range(phnum):
        phdr = Elf32Phdr(phdrtbl[:0x20])
        if phdr.p_type == 1:
            poffs = phdr.p_offset
            psize = phdr.p_filesz
            paddr = phdr.p_vaddr
            phdata = GetManyBytes(paddr, psize)
            file.seek(poffs)
            file.write(phdata)
        phdrtbl = phdrtbl[0x20:]
    file.seek(0)
    file.write(bytes[:16] + str(ehdr))   
    file.close()
    print "[+] Elf Dumped"
```

Once on disk we see that the dumped file is a 1.3M statically linked binary:

```c
ELF Header:
  Magic:   7f 45 4c 46 01 01 01 03 00 00 00 00 00 00 00 00 
  Class:                             ELF32
  Data:                              2's complement, little endian
  Version:                           1 (current)
  OS/ABI:                            UNIX - GNU
  ABI Version:                       0
  Type:                              EXEC (Executable file)
  Machine:                           Intel 80386
  Version:                           0x1
  Entry point address:               0x8048d86
  Start of program headers:          52 (bytes into file)
  Start of section headers:          0 (bytes into file)
  Flags:                             0x0
  Size of this header:               52 (bytes)
  Size of program headers:           32 (bytes)
  Number of program headers:         6
  Size of section headers:           40 (bytes)
  Number of section headers:         0
  Section header string table index: 0

Program Headers:
  Type           Offset   VirtAddr   PhysAddr   FileSiz MemSiz  Flg Align
  LOAD           0x000000 0x08048000 0x08048000 0x14ba2e 0x14ba2e R E 0x1000
  LOAD           0x14bea4 0x08194ea4 0x08194ea4 0x02374 0x06460 RW  0x1000
  NOTE           0x0000f4 0x080480f4 0x080480f4 0x00044 0x00044 R   0x4
  TLS            0x14bea4 0x08194ea4 0x08194ea4 0x00014 0x00038 R   0x4
  GNU_STACK      0x000000 0x00000000 0x00000000 0x00000 0x00000 RW  0x10
  GNU_RELRO      0x14bea4 0x08194ea4 0x08194ea4 0x0115c 0x0115c R   0x1
```

<br/>
<br/>
<h2>Summary</h2>
This packer was straight forward to unpack since it did not implement any anti-debugging/anti-dump/anti-analysis techniques. 
Therefore, the unpacking process could have been much quicker:

* Tracing until decoding of Elf header and program header table.
* Set hardware breapoint on execution at entry-point address in the Elf header.
* Profit.

<script type="text/javascript" src="https://asciinema.org/a/OfiADjXfl73JB9mfe8vBqnidR.js" id="asciicast-OfiADjXfl73JB9mfe8vBqnidR" async></script>

In the next write up I will cover the analysis process of the unpacked file. 
Thanks for reading and I hope you learned something useful from this post!.

n4x0r.




