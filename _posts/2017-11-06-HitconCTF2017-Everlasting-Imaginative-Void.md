---
layout: writeup
title:  "Hitcon2017CTF - 家徒四壁~Everlasting Imaginative Void~"
date:   2017-11-03 06:30
categories: writeup
tags: [reverse,Hitcon2017]
author: n4x0r
---

Everlasting Imaginative void was a Hitcon2017's reversing challenge worthing 300 points.
The challenge description was the following:

`Astonishingly impoverished elf`

Not much information.
Executing a `file` command, we get the following information:

```perl
n4x0r@pwn1e~$ file void-1b63cbab5d58da4294c2f97d6b60f568 
void-1b63cbab5d58da4294c2f97d6b60f568: ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 2.6.32, BuildID[sha1]=5f8a87150720003c217508ffd74883c715ffe7c3, stripped
```

If we execute the file we see the following:

```c
n4x0r@pwn1e~$ ./void-1b63cbab5d58da4294c2f97d6b60f568
blabla
hitcon{blabla}
```

Ok, Lets dig inside and see what we can find.
Surprisingly, the main function of the application was just the following:

<div style="text-align:center"><img src ="https://github.com/n4x0r/n4x0r.github.io/raw/master/images/HitconCTF7/1.png" /></div>

This means that the binary must have tampered control flow.
In my mind I thought about two potential possibilities:

* GOT/PLT hooks

* Constructor/Destructor pointer injection

Based that the binary is a `PIE` executable and that was bind using `BIND_NOW` flags, we can assume that GOT entries have not been tampered, and even if they had they will get overwritten at load time anyways. Regarding PLT hooks, I did a quick look up to the `.plt.got` section. and all jumps seem correct.

<div style="text-align:center"><img src ="https://github.com/n4x0r/n4x0r.github.io/raw/master/images/HitconCTF7/2.png" /></div>

The reason why there is not pivoting into PLT[0] for each PLT entry in `.plt.got` is because binary was linked with immediate binding as previously mentioned. Therefore, there is no need to jump back to resolver since all GOT entries will be resolved at load time.

Therefore, GOT/PLT hooks are discartded at this point.
The other technique that we have left is the Constructors/Destructors pointer injection.
This technique is based on injecting an additional pointer to the `.init_array`, `.fini_array` sections for constructors and destructors respectively.

```c
[Nr] Name              Type             Address           Offset
       Size              EntSize          Flags  Link  Info  Align

 ...

[18] .init_array       INIT_ARRAY       0000000000200dc8  00000dc8
       0000000000000008  0000000000000008  WA       0     0     8
[19] .fini_array       FINI_ARRAY       0000000000200dd0  00000dd0
       0000000000000008  0000000000000008  WA       0     0     8
```

We can see that the correspondent sizes of those sections seem to be correct. However, once one gets to know the purpose of sections and segments and the loading process of ELF files, one realizes that sections are complete rubish from an analysis standpoint. Section information can be easily crafted and they may not resemble the reality of the binary's layout. In addition, sections are only needed at compile time, but not at runtime. For runtime we have segments.

If we take a look at the binary's `DYNAMIC` segment, it tell us a different story:

```c
0x0000000000000019 (INIT_ARRAY)         0x200dc8
0x000000000000001b (INIT_ARRAYSZ)       8 (bytes)
0x000000000000001a (FINI_ARRAY)         0x200dd0
0x000000000000001c (FINI_ARRAYSZ)       16 (bytes)
```

We can clearly see, that `FINI_ARRAYSZ` is 1 pointer size bigger than what `.fini_array` section stated. Therefore, binary has corrupted control flow by destructor pointer injection.

I must emphasize that IDA and radare2 did not get this right since they prioritised section information over segment information:

<div style="text-align:center"><img src ="https://github.com/n4x0r/n4x0r.github.io/raw/master/images/HitconCTF7/3.png" /></div>

However, with radare2 we can see a pointer between the end of `.fini_array` and `.jcr` sections.

<div style="text-align:center"><img src ="https://github.com/n4x0r/n4x0r.github.io/raw/master/images/HitconCTF7/4.png" /></div>

As we can see from the radare2 screen shot, the pointer is initialised as 0. Therefore, most possibly that pointer will be a runtime relocation.

If we look at the relocations of the binary we see the following:

<div style="text-align:center"><img src ="https://github.com/n4x0r/n4x0r.github.io/raw/master/images/HitconCTF7/5.png" /></div>

The third relocation of type `R_X86_64_RELATIVE` is the one we are looking for.
Now lets analyse the injected routine.

The injected routine is based in the `.eh_frame` section. This section usually contains `dwarf` information about stack unwinding for exception handling such as dwarf bytecode along with dwarf flags. However, it does not normally contain code.
As we can see in the previous screenshot, the first thing this routine does is a `call 0x284`. This function pivots inside a crafted `.build-id` section.

 <div style="text-align:center"><img src ="https://github.com/n4x0r/n4x0r.github.io/raw/master/images/HitconCTF7/6.png" /></div>

This section usually holds a SHA1 specific of the binary's build. so we can say that both `.eh_frame` and `.build-id` sections have been crafted specifically for this challenge, as a form of code cave to embed code.

Futhermore, we can see a comparison of the contents of `rdi + 0x200715` with `'!'`. In fact, this is the 16th byte of the input retrived with `scanf` function at `main`. If this check holds, it jumps back to function `0x284 + 5` and resumes execution in the `.eh_frame` routine. Otherwise, will pivot to `ld.so` and will do further clean up until application termination.

At this point we can guess that the binaries flag must be `16 bytes`, and must end with `'!'`.

Further down the rabbit hole, we can see how it executes an mprotect systemcall which essentially does the following:
`mprotect(imageBase, 0x1000, PROT_READ|PROT_WRITE|PROT_EXEC)`

 <div style="text-align:center"><img src ="https://github.com/n4x0r/n4x0r.github.io/raw/master/images/HitconCTF7/7.png" /></div>

It gives write permissions to the CODE segment of the main application.
Moreover, it jumps back to the routine in the `.build-id` section, to then pivot to the following routine:

 <div style="text-align:center"><img src ="https://github.com/n4x0r/n4x0r.github.io/raw/master/images/HitconCTF7/8.png" /></div>

This routine basically copies spread bytes to a known memory location to then jump to it.
After stub if finally written, we end up in the following routine:

 <div style="text-align:center"><img src ="https://github.com/n4x0r/n4x0r.github.io/raw/master/images/HitconCTF7/9.png" /></div>

In this routine, 10 rounds of aes encription are performed using the Intel's processors AES instruction set. At the end of the 10 rounds, this routine checks ciphertext with input from `scanf`. if check holds, the program will print `Good!` string by jumping to the sycall gate previously shown (the mprotect one), changing its arguments so that it executes a write instead of mprotect syscall.
 
Something important to note about this aes routine, is that round-keys are actually hardcoded at adreses pointed by `rsi` (at the beginning of routine), so round keys can be restored and perform the `InvMixColumn` transformation in order to use them for decription. In order to do this we can user the `aesimc` instruction (note that aesimc should not be used either with the first or last round key). Furthermore, final cipher text can also be aquired by just getting the result of the `xmm1` register after `aesenclast` instruction at the end of the 10 rounds.

The following code replicates the decription routine:

{% raw %}
```c
#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include <stdlib.h>

void aes_decrypt(uint8_t *ctext, uint8_t *flag, uint8_t *round_keys) {
	asm volatile (	"movdqu (%0), %%xmm11	\n" 
   	    		"movdqu (%1), %%xmm10	\n" 
	    		"movdqu (%2), %%xmm9	\n"
			"movdqu (%3), %%xmm8	\n" 
			"movdqu (%4), %%xmm7	\n" 
			"movdqu	(%5), %%xmm6	\n" 
			"movdqu (%6), %%xmm5	\n" 
			"movdqu (%7), %%xmm4	\n" 
			"movdqu (%8), %%xmm3	\n" 
			"movdqu (%9), %%xmm2	\n" 
			"movdqu (%10), %%xmm1	\n" 
			"movdqu (%11), %%xmm0	\n" 
			
			"aesimc %%xmm9, %%xmm9	\n"
	     		"aesimc %%xmm8, %%xmm8	\n"
	     		"aesimc %%xmm7, %%xmm7	\n"
	     		"aesimc %%xmm6, %%xmm6	\n"
	     		"aesimc %%xmm5, %%xmm5	\n"
	     		"aesimc %%xmm4, %%xmm4	\n"
	     		"aesimc %%xmm3, %%xmm3	\n"
	     		"aesimc %%xmm2, %%xmm2	\n"
	     		"aesimc %%xmm1, %%xmm1	\n"
			
			"pxor 	%%xmm10, %%xmm11\n"
	     		"aesdec %%xmm9, %%xmm11	\n"
	     		"aesdec %%xmm8, %%xmm11	\n"
	     		"aesdec %%xmm7, %%xmm11	\n"
	     		"aesdec %%xmm6, %%xmm11	\n"
	     		"aesdec %%xmm5,	%%xmm11	\n"
	     		"aesdec %%xmm4, %%xmm11	\n"
	    	 	"aesdec %%xmm3, %%xmm11	\n"
	     		"aesdec %%xmm2, %%xmm11	\n"
	     		"aesdec %%xmm1, %%xmm11	\n"
	     		"aesdeclast %%xmm0, %%xmm11\n"
			
			"movdqu %%xmm11, (%12)	\n"
			
			:
			:  "r"(ctext),
			   "r"(round_keys + 160),
		       	   "r"(round_keys + 144),
			   "r"(round_keys + 128),
			   "r"(round_keys + 112),
			   "r"(round_keys + 96),
			   "r"(round_keys + 80),
			   "r"(round_keys + 64),
			   "r"(round_keys + 48),
			   "r"(round_keys + 32),
			   "r"(round_keys + 16),
			   "r"(round_keys),
			   "r"(flag)
			: "memory"
	);
}

int main() {
  uint8_t flag[17];
  int8_t round_keys[] = { 0x48, 0xc1, 0xfd, 0x03, 0xe8, 0x07, 0xfe, 0xff, 
			  0xff, 0x48, 0x85, 0xed, 0x74, 0x20, 0x31, 0xdb, 
			  0x0f, 0x1f, 0x84, 0x00, 0x00, 0x00, 0x00, 0x00, 
			  0x4c, 0x89, 0xea, 0x4c, 0x89, 0xf6, 0x44, 0x89, 
			  0xff, 0x41, 0xff, 0x14, 0xdc, 0x48, 0x83, 0xc3, 
			  0x01, 0x48, 0x39, 0xdd, 0x75, 0xea, 0x48, 0x83, 
			  0xc4, 0x08, 0x5b, 0x5d, 0x41, 0x5c, 0x41, 0x5d, 
			  0x41, 0x5e, 0x41, 0x5f, 0xc3, 0x90, 0x66, 0x2e, 
			  0x0f, 0x1f, 0x84, 0x00, 0x00, 0x00, 0x00, 0x00, 
			  0xf3, 0xc3, 0x00, 0x00, 0x48, 0x83, 0xec, 0x08, 
			  0x48, 0x83, 0xc4, 0x08, 0xc3, 0x00, 0x00, 0x00, 
			  0x01, 0x00, 0x02, 0x00, 0x25, 0x73, 0x00, 0x68, 
			  0x69, 0x74, 0x63, 0x6f, 0x6e, 0x7b, 0x25, 0x73, 
			  0x7d, 0x0a, 0x00, 0x00, 0x01, 0x1b, 0x03, 0x3b, 
			  0x40, 0x00, 0x00, 0x00, 0x07, 0x00, 0x00, 0x00, 
			  0xbc, 0xfd, 0xff, 0xff, 0x8c, 0x00, 0x00, 0x00, 
			  0xcc, 0xfd, 0xff, 0xff, 0xb4, 0x00, 0x00, 0x00, 
			  0xec, 0xfd, 0xff, 0xff, 0x5c, 0x00, 0x00, 0x00, 
			  0x1c, 0xff, 0xff, 0xff, 0xcc, 0x00, 0x00, 0x00, 
			  0x57, 0xff, 0xff, 0xff, 0xec, 0x00, 0x00, 0x00, 
			  0x6c, 0xff, 0xff, 0xff, 0x0c, 0x01, 0x00, 0x00, 
			  0xdc, 0xff, 0xff, 0xff, 0x54, 0x01, 0x00, 0x00 };

  unsigned char ctext[] = {0xe7, 0x47, 0x04, 0x12, 0x49, 0x6d, 0xcf, 0x47, 
	  		   0xb0, 0xe9, 0x1b, 0x17, 0x67, 0xfb, 0x46, 0x28};
  aes_decrypt(ctext, flag, round_keys);
  printf("hitcon{%s}\n", flag);
  return 0;
}
```
{% endraw %}
if we execute the previous code, we will get the flag `hitcon{code_in_BuildID!}`

