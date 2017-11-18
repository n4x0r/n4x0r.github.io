---
layout: writeup
title:  "Unpacking a Linux/Tsunami Sample"
date:   2017-11-17 06:30
categories: writeup
tags: [reverse,malware, ELF, packers]
author: n4x0r
---

This writeup is going to be a walktrough on how to unpack a modified version of UPX, for a given ELF malware sample. Hashes of this sample are the following:

```c
SHA256: f22ffc07e0cc907f00fd6a4ecee09fe8411225badb2289c1bffa867a2a3bd863
  SHA1: 76584c9a22835353186e753903ee0a853663bd83
   MD5: 171edd284f6a19c6ed3fe010b79c94af
```

In VirusTotal we can see that the malware is identified as a Tsunami Variant for the most part:

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

We can see that the binary's string table has been stripped, aswell as the section header table.
In addition, the binary only contains two segments. Based on the number of segments, and the strange base address it holds (0x00c01000) we can assume that the file is packed.

<h2> Static Analysis</h2>
<br/>
If we open the binary with `IDA PRO` we can confirm this statement:
<br/>

<div style="text-align:center"><img src ="https://github.com/n4x0r/n4x0r.github.io/raw/master/images/Tsunami/2.png" /></div>
<br/>

<div style="text-align:center"><img src ="https://github.com/n4x0r/n4x0r.github.io/raw/master/images/Tsunami/3.png" /></div>

Second and third function seem straight forward. One allocates a `RWX` page sized chunk, and the latter executes a write syscall, and then exits.
<br/>

<div style="text-align:center"><img src ="https://github.com/n4x0r/n4x0r.github.io/raw/master/images/Tsunami/5.png" /></div>
<br/>

<div style="text-align:center"><img src ="https://github.com/n4x0r/n4x0r.github.io/raw/master/images/Tsunami/4.png" /></div>

However, the entry point of the application looks certainly more messier, and by first glance we can assume that it will have a decryptor/decoder functionality
<br/>

<div style="text-align:center"><img src ="https://github.com/n4x0r/n4x0r.github.io/raw/master/images/Tsunami/6.png" /></div>

Let's start the tour shall we.
The very first thing that the entrypoint does is calling `0x00C8DC28`, which itself redirects execution to `allocate_rwx_page` and stores the return address (`start+5`) in ebp.
<br/>

<div style="text-align:center"><img src ="https://github.com/n4x0r/n4x0r.github.io/raw/master/images/Tsunami/7.png" /></div>
<br/>

<div style="text-align:center"><img src ="https://github.com/n4x0r/n4x0r.github.io/raw/master/images/Tsunami/8.png" /></div>

Note the stub of data on `0x00C8DC31`, we will come back to it later.
Execution then is driven by the `allocate_rwx_page` function, which as said before just allocates a page of memory with `RXW`permissions. This buffer will be allocated at `0x00C8F000`. If the allocation fails, then execution will branch into the `write_message_and_exit` funtion, in which the string `'nandemo wa shiranai wa yo,'` gets printed to `stderr`. On the other hand, if allocation of RWX chunk is sucessfull, execution will pivot back to `start+5`.

After allocating RWX memory, the malware then proceeds and copies a subroutine inside that chunk. The data at `0x00C8DC31` is used to decode this routine. The malware uses different routines to copy data/code to different locations. The following picture is sort of a helper the malware uses for copying contents of different locations, and its used several times in the unpacking process.

<div style="text-align:center"><img src ="https://github.com/n4x0r/n4x0r.github.io/raw/master/images/Tsunami/9.png" /></div>
<br/>

At this point, I coudnt do much progress just by static analysis. Now we will cover the Dynamic analysis phase.

<h2> Dynamic Analysis </h2>

Now that we know that the malware is building sort of a shellcode by decoding the data block we saw previously, we need to pivot to it somehow to remain with our analysis. One way to do it could be putting a hardware breakpoint on access on the `RXW` chunk. However, we want to find the cleanest possible way to withness that transition in order to not miss details about the malware's behaviour. 
On the entrypoint routine, after the function `pivot_to_allocate_rwx_pg` we can clearly see that the register context is being saved with a `pusha` instruction. At some point the malware will need to restore the register context. if we search  in the start rotine for `popad` instructions, we see that there are two of them and they are just before the routine returns.

<div style="text-align:center"><img src ="https://github.com/n4x0r/n4x0r.github.io/raw/master/images/Tsunami/10.png" /></div>
<br/>

<div style="text-align:center"><img src ="https://github.com/n4x0r/n4x0r.github.io/raw/master/images/Tsunami/11.png" /></div>

If we put one breakpoint on each on this location, and then we resume the application's execution, we will have control of execution when decoding routine is over.
On resume we will see that the trigered breakpoint is the one at `0x00C8DB46`.
<br/>

<div style="text-align:center"><img src ="https://github.com/n4x0r/n4x0r.github.io/raw/master/images/Tsunami/12.png" /></div>

We see that it does not pivot directly to the RWX chunk at `0x00c8f000`, but it returns first to `allocate_rwx_page+49`, to then unwind the stack and return to the RWX chunk.

<br/>
<div style="text-align:center"><img src ="https://github.com/n4x0r/n4x0r.github.io/raw/master/images/Tsunami/13.png" /></div>



