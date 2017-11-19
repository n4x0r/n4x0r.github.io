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
Furthermore, note that the file and size memory for the second `PT_LOAD` segment are set to 0. meaning that when segment will get loaded to memory, there will be a 0x1000 chunk at `0x0819b304` due to segment alignment.

In Linux systems is typical to encounter packed malware with UPX. If we check for the `UPX` magic in the file we see the following:

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
This is quite interesting because if we try to use the automated unpacking feature of UPX we get the following:

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

Threfore, we may be dealing against a custom packer based on a modified version of `UPX`.
We will start analysing the sample by doing static analysis, then I will continue with some dynamic analysis, and at the end will do a brief summary of the sample as a whole. Let's start with static analysis.

<br/>
<br/>
<h2> Static Analysis</h2>
<br/>

If we open the binary with `IDA PRO` we can confirm that the sample is indeed packed.:

<br/>
<div style="text-align:center"><img src ="https://github.com/n4x0r/n4x0r.github.io/raw/master/images/Tsunami/2.png" /></div>
<br/>
<div style="text-align:center"><img src ="https://github.com/n4x0r/n4x0r.github.io/raw/master/images/Tsunami/3.png" /></div>
<br/>

There are only 3 identifiable functions. Second and third functions seem straight forward. One allocates a `RWX` page sized chunk, and the latter executes a write syscall, and then exits.

<br/>
<div style="text-align:center"><img src ="https://github.com/n4x0r/n4x0r.github.io/raw/master/images/Tsunami/5.png" /></div>
<br/>
<div style="text-align:center"><img src ="https://github.com/n4x0r/n4x0r.github.io/raw/master/images/Tsunami/4.png" /></div>
<br/>

However, the entry point of the application looks certainly more messier, and by first glance we can assume that it will have a decryptor/decoder functionality

<br/>
<div style="text-align:center"><img src ="https://github.com/n4x0r/n4x0r.github.io/raw/master/images/Tsunami/6.png" /></div>
<br/>

Let's start the tour shall we.
The very first thing that the entrypoint does is calling `0x00C8DC28`, which itself redirects execution to `allocate_rwx_page` and stores the return address (`start+5`) in ebp.

<br/>
<div style="text-align:center"><img src ="https://github.com/n4x0r/n4x0r.github.io/raw/master/images/Tsunami/7.png" /></div>
<br/>
<div style="text-align:center"><img src ="https://github.com/n4x0r/n4x0r.github.io/raw/master/images/Tsunami/8.png" /></div>
<br/>

Note the stub of data on `0x00C8DC31`, we will come back to it later.
Execution then is driven by the `allocate_rwx_page` function, which as said before just allocates a page of memory with `RXW`permissions. This buffer will be allocated at `0x00C8F000`. If the allocation fails, then execution will branch into the `write_message_and_exit` funtion, in which the string `'nandemo wa shiranai wa yo,'` gets printed to `stderr`. On the other hand, if allocation of RWX chunk is sucessfull, execution will pivot back to `start+5`.

After allocating RWX memory, the malware will then proceed to copy and decode a given stub inside that chunk. After a while analysing the code, I came to the conclusion that function `start+5` (entrypoint+5) is the routine the malware uses to decode and copy packer stub. At this point, I coudnt do much progress just by static analysis, so I fired up the debugger to do some Dynamic analysis.

<br/>
<br/>
<h2> Dynamic Analysis </h2>
<br/>

Now that we know what subroutine the malware uses to decode and copy packer stub, the first stage the malware will do is to decode some stub inside the RWX chunk by decoding the data block previosly shown. On our next move we will try to pivot to the destination chunk (chunk `0x00c8f000`) of the decoded stub somehow to remain with our analysis. One way to do it could be putting a hardware breakpoint on execution at the `RXW` chunk. However, we want to find the cleanest possible way to withness that transition in order to not miss details about the malware's behaviour. 
On the entrypoint routine, after the function `pivot_to_allocate_rwx_pg` we can clearly see that the register context is being saved with a `pusha` instruction. After that we can see that two pointers are loaded into the `esi` and `edi` registers. Those pointers are the stub source address to be decoded, and the destination buffer addres to transfer the decoded stub.

<br/>
<div style="text-align:center"><img src ="https://github.com/n4x0r/n4x0r.github.io/raw/master/images/Tsunami/10.png" /></div>
<br/>

Further down `start` we can see how some of the data in the stub gets copied to the destination buffer:

<br/>
<div style="text-align:center"><img src ="https://github.com/n4x0r/n4x0r.github.io/raw/master/images/Tsunami/15.png" /></div>
<br/>

On the other hand, there are specific bytes that get processed differently, and multiple bytes get derived from a single byte. Based on this we can assume that the decoding algorithm must be some sort of deflate implementation.
 
<br/>
<div style="text-align:center"><img src ="https://github.com/n4x0r/n4x0r.github.io/raw/master/images/Tsunami/16.png" /></div>
<br/>

We can see that decoding will stop when second argument `stub_size` + first argument `stub_base` == current stub pointer at `esi`. If this condition is true, the function simply returns.

<br/>
<div style="text-align:center"><img src ="https://github.com/n4x0r/n4x0r.github.io/raw/master/images/Tsunami/11.png" /></div>
<br/>

If we put one breakpoint on this ret instruction, and then we resume the application's execution, we will get control of execution back when decoding is over.

<br/>
<div style="text-align:center"><img src ="https://github.com/n4x0r/n4x0r.github.io/raw/master/images/Tsunami/12.png" /></div>
<br/>

We see that it does not pivot directly to the RWX chunk at `0x00c8f000`, but it returns first to `allocate_rwx_page+49`, to then unwind the stack and return to the RWX chunk.

<br/>
<div style="text-align:center"><img src ="https://github.com/n4x0r/n4x0r.github.io/raw/master/images/Tsunami/13.png" /></div>
<br/>

When execution reaches the `0x00C8F000` chunk, we see the following routine:

<br/>
<div style="text-align:center"><img src ="https://github.com/n4x0r/n4x0r.github.io/raw/master/images/Tsunami/14.png" /></div>
<br/>

The main purpose of this routine is to retrieve the `ELF Auxiliar vector` from the stack, and copy it into a local stack buffer. The struture of the Auxiliar vector looks as follows:

<br/>
<div style="text-align:center"><img src ="https://github.com/n4x0r/n4x0r.github.io/raw/master/images/Tsunami/17.png" /></div>
<br/>

Once Auxiliar vector is retrived from stack then this function calls `call_read_link` function which looks as follows:
 
<br/>
<div style="text-align:center"><img src ="https://github.com/n4x0r/n4x0r.github.io/raw/master/images/Tsunami/18.png" /></div>
<br/>

In this function, a series of statistics are retrieved from the current file such as the location of the decoded elf in the `PT_LOAD` segment along with 2 more flags used for decoding. Furthermore, the address of the aligned end of the first `PT_LOAD` segment is computed, and a stack buffer is set in order to hold the resulting decoded stub. After collecting these series of statistics, the function proceeds with stage 1 of the decoding process, and calls `init_decoding_stage` function. This function looks as follows:

 
<br/>
<div style="text-align:center"><img src ="https://github.com/n4x0r/n4x0r.github.io/raw/master/images/Tsunami/19.jpg" /></div>
<br/>




