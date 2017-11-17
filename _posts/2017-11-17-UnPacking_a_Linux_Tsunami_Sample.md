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


