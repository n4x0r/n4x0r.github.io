---
layout: article
title:  "SHELF Loading"
date:   2021-08-04 06:30
categories: article
tags: [reversing, malware, ELF, packers]
author: ulexec
---

SHELF Loading is a new type of ELF binary reflective loading that my friend @Anonymous_ and I first documented on April 21st 2021.
This new `ELF reflective loading` methodology enables the capability to generate compiler-based artifacts with properties that resemble those of `shellcode`.
These compiler-based artifacts are ultimately a `Hybrid ELF` file between conventional static and PIE binaries.
Had the pleasure to publish this research at **Tmp0ut**, a Linux VX zine. This was Volume #1, and its first release and their official site can be found at [tmpout.sh](http://tmpout.sh).

Make sure to check other of the great articles published on this first volume if ELF mangling/golfing/fuckery is for you :)

<style>
	iframe {
		display: block;
  		width: 75vw;
  		height: 75vh;
	}
</style>


<br/>

You can also read the blog from tmpout official website [here](https://tmpout.sh/1/10/)
<iframe src="https://tmpout.sh/1/10/"></iframe>
