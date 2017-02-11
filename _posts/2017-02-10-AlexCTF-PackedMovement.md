---
layout: post
title:  "AlexCTF - PackedMovement"
date:   2017-02-10 20:30
categories: CTF
tags: [reverse,AlexCTF]
author: n4x0r
---

`PackedMovement` was the last Reverse Engineering challenge on `AlexCTF 2017`. The puntuation of this challnege was of `350` points.

The only hint given to this challenge is its name. You will see why later on in this writeup.

The retrieved binary is called `move`. if we run the `file` command over it we find the following:

```bash
move: ELF 32-bit LSB executable, Intel 80386, version 1 (GNU/Linux), statically linked, stripped
```
Even more interestingly is when we see the binaries segments with `readelf -l move`

```bash
Elf file type is EXEC (Executable file)
Entry point 0xd906d0
There are 2 program headers, starting at offset 52

Program Headers:
  Type           Offset   VirtAddr   PhysAddr   FileSiz MemSiz  Flg Align
  LOAD           0x000000 0x00c01000 0x00c01000 0x18fea1 0x18fea1 R E 0x1000
  LOAD           0x000300 0x0880b300 0x0880b300 0x00000 0x00000 RW  0x1000
```

The fact that the binary only contains two `LOAD` segments suggest us that the binary is possibly packed.

Lets check the entry point of the binary and see how the first couple of instructions look:

![entry](https://github.com/n4x0r/n4x0r.github.io/raw/master/images/AlexCTF7/1.png)

Several packers use the intruction `pusha` in order to save the registry contents before running the decompression routine. One famous packer that uses this instruction is the `UPX` packer.

If we run the `strings move | grep UPX` command we will confirm this binary has been packed with `UPX`:

```bash
9vUPX!
$Info: This file is packed with the UPX executable packer http://upx.sf.net $
$Id: UPX 3.91 Copyright (C) 1996-2013 the UPX Team. All Rights Reserved. $
UPX!u
UPX!
UPX!
```

Fortunately, `UPX` also contains a flag for decompression. If we run the `upx -d move -o dem` command it will decompress the `move` binary and save a copy of the decompressed binary into disk with the name `dem`

If we run `readelf -l dem` command to see `dem's` segments we see the following:

```bash
Elf file type is EXEC (Executable file)
Entry point 0x804829c
There are 6 program headers, starting at offset 52

Program Headers:
  Type           Offset   VirtAddr   PhysAddr   FileSiz MemSiz  Flg Align
  PHDR           0x000034 0x08048034 0x08048034 0x000c0 0x000c0 R E 0x4
  INTERP         0x0000f4 0x080480f4 0x080480f4 0x00013 0x00013 R   0x1
      [Requesting program interpreter: /lib/ld-linux.so.2]
  LOAD           0x000000 0x08048000 0x08048000 0x18b3c 0x18b3c R E 0x1000
  LOAD           0x018f58 0x08061f58 0x08061f58 0x5a93a4 0x7a93a8 RW  0x1000
  DYNAMIC        0x018f58 0x08061f58 0x08061f58 0x000a8 0x000a8 RW  0x4
  GNU_RELRO      0x018f58 0x08061f58 0x08061f58 0x000a8 0x000a8 R   0x1

 Section to Segment mapping:
  Segment Sections...
   00     
   01     .interp 
   02     .interp .hash .dynsym .dynstr .gnu.version .gnu.version_r .rel.plt .plt .text 
   03     .dynamic .got.plt .data .bss 
   04     .dynamic 
   05     .dynamic 
```

This looks more like what we are looking for. Now that we have a decompress file is a good chance to see what the binary on execution looks like. When we execute the file we see the following:

```bash
Guess a flag: AAAAAAA
Wrong Flag!
```
Easy enough. Lets see how the binary looks like. When we open the `dem` binary in `IDA` we see the following:

![main](https://github.com/n4x0r/n4x0r.github.io/raw/master/images/AlexCTF7/2.png)

The binary looks like its obfuscated with [movfuscator](https://github.com/xoreaxeaxeax/movfuscator)

There is a tool called [demovfuscator](https://github.com/kirschju/demovfuscator) however this tool still under development. All I could achieve with it was to replace a chunk of mov instructions with a `lea` instruction equivalent. However `demovfuscator` can geneate flow-graphs of the actuall execution flow of the executable.

This is an example of one of them:

![cfg](https://github.com/n4x0r/n4x0r.github.io/raw/master/images/AlexCTF7/cfg.png)

As we can see, the binary seems that has an if else behavior.

Addiditonally, the binary itself seem to be a stack based virtual machine. One can assure this is true just by looking the name of some of its global variables:

![gb1](https://github.com/n4x0r/n4x0r.github.io/raw/master/images/AlexCTF7/3.png)
![gb2](https://github.com/n4x0r/n4x0r.github.io/raw/master/images/AlexCTF7/4.png)

This being said I had to make a choice on the stategy I was going to follow to solve this challenge. I had two different options

 * 1 - Attempt to make an assembler of the actual machine opcodes in order to be able to identify clearly the verification of the flag

 * 2 - Attempt to find the verification mechanism without crafting an assembler of the actual machine.

I choose the 2nd approach so that if it fails I can always attempt to craft an assembler for it.

After I made this decission I started to do some dynamic analysis. At the beginning I felt like I was looking throuh a glass, My assumptions would change every 5 intructions. However at one point I saw the light.
This point was at address `0x080493DB`

![light](https://github.com/n4x0r/n4x0r.github.io/raw/master/images/AlexCTF7/5.png)

At that instruction I saw what it could be an initial assumption of how the binary validates each byte of the flag. It Would Load the particular byte of the flag into `R2` virtual register and the input byte will be loaded into de `R3` virtual register. Both of this registers will then be loaded into the `ALU` module of the machine. it would held a set of operations and it will leave the result of them in the `rax` register which would be pass to a `test eax, eax` intruction, and if this instruction does not return 1, it would finish execution. Otherwise it will proceed and compare the next byte.

Something somewhat curious about this whole procedure is that the flag byte is always loaded into the `R2` virtual register. If we can see all the instructions where some value is being stored into `R2` we may be able to see all the bytes our input is being compared against.

Running the following `IDA python` sript will help us find exactly that:

```python
from idc import *
from idaapi import *

main = None

for func in Functions():
    if GetFunctionName(func) == "main":
        main = func
    
code = list(FuncItems(main))

for line in code:
        if GetOpnd(line,0) == 'R2':
            print hex(line), "\t", GetDisasm(line)
```

Make sure to extend the end of the main function down to the end of the `_text` section. That is address `0x08060B38`

The result of this script is the following:

```nasm
0x80493dbL 	mov     R2, 41h
0x8049ddeL 	mov     R2, 4Ch
0x804a7e1L 	mov     R2, 45h
0x804b1e4L 	mov     R2, 58h
0x804bb9cL 	mov     R2, 43h
0x804c59fL 	mov     R2, 54h
0x804cfa2L 	mov     R2, 46h
0x804d9a5L 	mov     R2, 7Bh
0x804e357L 	mov     R2, 4Dh
0x804ed5aL 	mov     R2, 30h
0x804f75dL 	mov     R2, 56h
0x8050160L 	mov     R2, 66h
0x8050b0cL 	mov     R2, 75h
0x805150fL 	mov     R2, 73h
0x8051f12L 	mov     R2, 63h
0x8052915L 	mov     R2, 34h
0x80532bbL 	mov     R2, 74h
0x8053cbeL 	mov     R2, 30h
0x80546c1L 	mov     R2, 72h
0x80550c4L 	mov     R2, 5Fh
0x8055a64L 	mov     R2, 77h
0x8056467L 	mov     R2, 30h
0x8056e6aL 	mov     R2, 72h
0x805786dL 	mov     R2, 6Bh
0x8058207L 	mov     R2, 35h
0x8058c0aL 	mov     R2, 5Fh
0x805960dL 	mov     R2, 6Ch
0x805a010L 	mov     R2, 31h
0x805a9a4L 	mov     R2, 6Bh
0x805b3a7L 	mov     R2, 65h
0x805bdaaL 	mov     R2, 5Fh
0x805c7adL 	mov     R2, 6Dh
0x805d13bL 	mov     R2, 34h
0x805db3eL 	mov     R2, 67h
0x805e541L 	mov     R2, 31h
0x805ef44L 	mov     R2, 63h
0x805f8ccL 	mov     R2, 7Dh
```

If we modify the script above to print the bytes that are been stored into `R2` we should get the flag.

final script is: 

```python
from idc import *
from idaapi import *

flag = ''
main = None

for func in Functions():
    if GetFunctionName(func) == "main2":
        main = func
    
code = list(FuncItems(main))

for line in code:
        if GetOpnd(line,0) == 'R2':
            flag += chr(int(GetOpnd(line, 1)[:-1], 16))
            
print "\n\n", flag
```

By Executing the previous script we will get the flag : ```ALEXCTF{M0Vfusc4t0r_w0rk5_l1ke_m4g1c}```
