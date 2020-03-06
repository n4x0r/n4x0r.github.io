---
layout: writeup
title:  "Building Kernel debugging images with Buildroot"
date:   2017-11-03 06:30
categories: misc
tags: [Kernel, Linux, Debugging]
author: n4x0r
---

Installing a new kernel image is quite simple thanks to the `buildroot` utility.
A number of steps must be followed:

<h3>1 - Download latest Buildroot</h3>
```c
wget http://buildroot.uclibc.org/downloads/buildroot-20XX.YY.tar.gz
```
<h3>2 - Generate Buildroot preset config</h3>
```c	
make qemu_x86_defconfig 	# EXAMPLE ARCH
make menuconfig

* Change the following to enable Kernel Debugging support:
		* In Build options, toggle build packages with debugging symbols.
		* In Toolchain, change linux version to desired one
		* In Toolchain, change Custom kernel version headers to desired ones
		* In Kernel, change Kernel version to desired one
```

<h3>3 - Download Kernel source and configure it</h3>
```c
make linux-menuconfig

* Change the following to enable Kernel Debugging support:

	* In Kernel hacking, toggle Kernel Debugging
	* Under Kernel hacking in Compile-time checks and compiler options toggle
	- Compile kernel with debug infopp
	- Provide GDB sripts for kernel debugging`
	- Compile kernel with frame pointers
```
		
<h3>4 - Build your kernel</h3>
```c
make
```	
<h3>5 - Run Kernel</h3>

Once you have covered all steps, The following files should have been created:

```c
* Kernel source code at output/build/linux-XXX
* Compressed kernel image at output/images/bzImage
* Root filesystem (rootfs) at output/images/rootfs.ext2
* Raw kernel image at output/build/linux-XXX/vmlinux

Done! all we got left is to execute the kernel image with qemu:

qemu-system-xx  -kernel images/bzImage  	\
	-hda images/rootfs.ext2 	\
	-append "nokaslr root=/dev/sda rw" 	\
	-s 				\
	-S


On another terminal execute gdb under the linux kernel directory:

(gdb) add-auto-load-safe-path output/build/linux-4.9.6/scripts/gdb/vmlinux-gdb.py
(gdb) file output/build/linux-XXX/vmlinux
(gdb) target remote :1234
(gdb) break init
(gdb) c
```
