---
layout: writeup
title:  "Unpacking a Linux/Tsunami Sample"
date:   2017-11-17 06:30
categories: writeup
tags: [reverse,malware, ELF, packers]
author: n4x0r
---

This writeup is going to be a walktrough on how to unpack a modified version of UPX, for a given ELF malware sample. Hashes of this sample are the following:

```perl
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





