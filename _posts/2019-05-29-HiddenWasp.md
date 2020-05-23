---
layout: article
title:  "HiddenWasp: Another piece of Winnti's Toolkit"
date:   2019-05-29 06:30
categories: article
tags: [reverse,malware, ELF, packers]
author: ulexec
---

This article is a copy of the original report we published at Intezer Labs we we reported this threat. The original report can be found [here](https://intezer.com/blog/linux/hiddenwasp-malware-targeting-linux-systems/)

<br/>

Although the Linux threat ecosystem is crowded with IoT DDoS botnets and crypto-mining malware, it is not very common to spot trojans or backdoors in the wild. Unlike Windows malware, Linux malware authors do not seem to invest too much effort writing their implants. In an open-source ecosystem there is a high ratio of publicly available code that can be copied and adapted by attackers. 

In addition, Anti-Virus solutions for Linux tend to not be as resilient as in other platforms. Therefore, threat actors targeting Linux systems are less concerned about implementing excessive evasion techniques since even when reusing extensive amounts of code, threats can relatively manage to stay under the radar. 

Nevertheless, malware with strong evasion techniques do exist for the Linux platform. There is also a high ratio of publicly available open-source malware that utilize strong evasion techniques and can be easily adapted by attackers. We believe this fact is alarming for the security community since many implants today have very low detection rates, making these threats difficult to detect and respond to.

While working at Intezer, we discovered an undetected Linux malware that appear to be enforcing advanced evasion techniques with the use of rootkits to leverage trojan-based implants, which later seems that it was [linked](https://www.scmagazine.com/home/security-news/malware/a-sophisticated-malware-campaign-dubbed-hiddenwasp-is-targeting-linux-systems-with-the-goal-of-targeted-remote-control/) to the Winnti Umbrella (cluster of adversaries). In this blog we will present a **technical analysis** of each of the different components that this new malware, HiddenWasp, is composed of. We will also highlight interesting code-reuse connections that we have observed to several open-source malware. The following images are screenshots from VirusTotal of the newer undetected malware samples discovered: 

<br/>

![technical analysis](http://intezer.com/wp-content/uploads/2019/05/pasted-image-0-1.png) 

<br/>
<br/>

### **1\. Technical Analysis**

When we came across these samples we noticed that similar to the recent Winnti Linux variants reported by [Chronicle](https://medium.com/chronicle-blog/winnti-more-than-just-windows-and-gates-e4f03436031a), the infrastructure of this malware is composed of a user-mode rootkit, a trojan and an initial deployment script. We will cover each of the three components in this post, analyzing them and their interactions with one another. 

<br/>

#### **2.1 Initial Deployment Script:** 
When we spotted these undetected files in VirusTotal it seemed that among the uploaded artifacts there was a bash script along with a trojan implant binary. 

<br/>

![Initial Deployment Script](http://intezer.com/wp-content/uploads/2019/05/2019-05-23-084551_1082x412_scrot.png)

<br/>

We observed that these files were uploaded to VirusTotal using a path containing the name of a Chinese-based forensics company known as [Shen Zhou Wang Yun Information Technology Co., Ltd](http://www.china-forensic.com/ccfc/en/). Furthermore, the malware implants seem to be hosted in servers from a physical server hosting company known as ThinkDream located in Hong Kong.
 
<br/>
<div style="text-align:center"><img src ="http://intezer.com/wp-content/uploads/2019/05/pasted-image-0-10.png" /></div>
<br/>

Among the uploaded files, we observed that one of the files was a bash script meant to deploy the malware itself into a given compromised system, although it appears to be for testing purposes:

<br/>

![ThinkDream](http://intezer.com/wp-content/uploads/2019/05/2019-05-23-085049_997x237_scrot.png) 

<br/>

Thanks to this file we were able to download further artifacts not present in VirusTotal related to this campaign. This script will start by defining a set of variables that would be used throughout the script. 

<br/>
<div style="text-align:center"><img src ="http://intezer.com/wp-content/uploads/2019/05/2019-05-23-085725_713x536_scrot.png" /></div>
<br/>

Among these variables we can spot the credentials of a user named ‘sftp’, including its hardcoded password. This user seems to be created as a means to provide initial persistence to the compromised system:

<br/>
<div style="text-align:center"><img src ="http://intezer.com/wp-content/uploads/2019/05/2019-05-23-085815_1044x268_scrot.png" /></div>
<br/>

Furthermore, after the system’s user account has been created, the script proceeds to clean the system as a means to update older variants if the system was already compromised:

<br/>
<div style="text-align:center"><img src ="http://intezer.com/wp-content/uploads/2019/05/2019-05-23-090036_563x378_scrot.png" /></div>
<br/>

The script will then proceed to download a tar compressed archive from a download server according to the architecture of the compromised system. This tarball will contain all of the components from the malware, containing the rootkit, the trojan and an initial deployment script:

<br/>
<div style="text-align:center"><img src ="http://intezer.com/wp-content/uploads/2019/05/2019-05-23-090228_818x570_scrot.png" /></div>
<br/> 

After malware components have been installed, the script will then proceed to execute the trojan: 

<br/>
<div style="text-align:center"><img src ="http://intezer.com/wp-content/uploads/2019/05/2019-05-23-090327_793x511_scrot.png" /></div>
<br/> 

We can see that the main trojan binary is executed, the rootkit is added to LD_PRELOAD path and another series of environment variables are set such as the ‘I_AM_HIDDEN’. We will cover throughout this post what the role of this environment variable is. To finalize, the script attempts to install reboot persistence for the trojan binary by adding it to /etc/rc.local. Within this script we were able to observe that the main implants were downloaded in the form of tarballs. As previously mentioned, each tarball contains the main trojan, the rootkit and a deployment script for x86 and x86_64 builds accordingly. 

<br/>
<div style="text-align:center"><img src ="http://intezer.com/wp-content/uploads/2019/05/2019-05-24-195845_1152x222_scrot.png" /></div>
<br/> 

The deployment script has interesting insights of further features that the malware implements, such as the introduction of a new environment variable ‘HIDE_THIS_SHELL’: 

<br/>
<div style="text-align:center"><img src ="http://intezer.com/wp-content/uploads/2019/05/2019-05-23-144740_819x467_scrot.png" /></div>
<br/> 

We found some of the environment variables used in a open-source rootkit known as [Azazel](https://github.com/chokepoint/azazel/search?q=HIDE_THIS_SHELL&unscoped_q=HIDE_THIS_SHELL):


<br/>
<div style="text-align:center"><img src ="http://intezer.com/wp-content/uploads/2019/05/2019-05-24-053134_528x38_scrot.png" /></div>
<br/> 

It seems that this actor changed the default environment variable from Azazel, that one being HIDE_THIS_SHELL for I_AM_HIDDEN. We have based this conclusion on the fact that the environment variable HIDE_THIS_SHELL was not used throughout the rest of the components of the malware and it seems to be residual remains from Azazel original code. The majority of the code from the rootkit implants involved in this malware infrastructure are noticeably different from the original Azazel project. Winnti Linux variants are also known to have reused code from this open-source project. 

<br/>

#### **2.2 The Rootkit:**

The rootkit is a user-space based rootkit enforced via LD_PRELOAD linux mechanism. It is delivered in the form of an ET_DYN stripped ELF binary. This shared object has an DT_INIT dynamic entry. The value held by this entry is an address that will be executed once the shared object gets loaded by a given process:

<br/>
<div style="text-align:center"><img src ="https://intezer.com/wp-content/uploads/2019/05/2019-05-29-164708_842x473_scrot.png" /></div>
<br/> 

Within this function we can see that eventually control flow falls into a function in charge to resolve a set of dynamic imports, which are the functions it will later hook, alongside with decoding a series of strings needed for the rootkit operations. 

<br/>
<div style="text-align:center"><img src ="http://intezer.com/wp-content/uploads/2019/05/pasted-image-0-4.png" /></div>
<br/> 

We can see that for each string it allocates a new dynamic buffer, it copies the string to it to then decode it. It seems that the implementation for dynamic import resolution slightly varies in comparison to the one used in [Azazel](https://github.com/chokepoint/azazel/blob/master/config.py) rootkit. 

When we wrote the script to simulate the cipher that implements the string decoding function we observed the following algorithm:

<br/>
<div style="text-align:center"><img src ="http://intezer.com/wp-content/uploads/2019/05/2019-05-23-072903_318x253_scrot.png" /></div>
<br/> 

We recognized that a similar algorithm to the one above was used in the past by [Mirai](https://github.com/jgamblin/Mirai-Source-Code/blob/master/mirai/bot/scanner.c#L963), implying that authors behind this rootkit may have ported and modified some code from Mirai.

<br/>
<div style="text-align:center"><img src ="http://intezer.com/wp-content/uploads/2019/05/2019-05-23-073253_483x407_scrot.png" /></div>
<br/> 

After the rootkit main object has been loaded into the address space of a given process and has decrypted its strings, it will export the functions that are intended to be hooked. We can see these exports to be the following:

<br/>
<div style="text-align:center"><img src ="http://intezer.com/wp-content/uploads/2019/05/pasted-image-0-8.png" /></div>
<br/> 

For every given export, the rootkit will hook and implement a specific operation accordingly, although they all have a similar layout. Before the original hooked function is called, it is checked whether the environment variable ‘I_AM_HIDDEN’ is set:

<br/>
<div style="text-align:center"><img src ="http://intezer.com/wp-content/uploads/2019/05/2019-05-27-074838_796x779_scrot.png" /></div>
<br/> 

We can see an example of how the rootkit hooks the function fopen in the following screenshot: 

<br/>
<div style="text-align:center"><img src ="http://intezer.com/wp-content/uploads/2019/05/2019-05-23-081200_847x623_scrot.png" /></div>
<br/> 

We have observed that after checking whether the ‘I_AM_HIDDEN’ environment variable is set, it then runs a function to hide all the rootkits’ and trojans’ artifacts. In addition, specifically to the fopen function it will also check whether the file to open is ‘/proc/net/tcp’ and if it is it will attempt to hide the malware’s connection to the cnc by scanning every entry for the destination or source ports used to communicate with the cnc, in this case 61061\. This is also the default port in [Azazel](https://github.com/chokepoint/azazel/blob/master/config.py) rootkit. 

<br/>
<div style="text-align:center"><img src ="http://intezer.com/wp-content/uploads/2019/05/2019-05-23-081703_569x553_scrot.png" /></div>
<br/>

The rootkit primarily implements artifact hiding mechanisms as well as tcp connection hiding as previously mentioned. Overall functionality of the rootkit can be illustrated in the following diagram: 

<br/>
<div style="text-align:center"><img src ="http://intezer.com/wp-content/uploads/2019/05/pasted-image-0-6.png" /></div>
<br/>
<br/>

#### **2.3 The Trojan:** 

The trojan comes in the form of a statically linked ELF binary linked with stdlibc++. We noticed that the trojan has code connections with ChinaZ’s Elknot implant in regards to some common MD5 implementation in one of the statically linked libraries it was linked with: 

<br/>
<div style="text-align:center"><img src ="http://intezer.com/wp-content/uploads/2019/05/pasted-image-0-2.png" /></div>
<br/>

In addition, we also see a high rate of shared strings with other known ChinaZ malware, reinforcing the possibility that actors behind HiddenWasp may have integrated and modified some MD5 implementation from Elknot that could have been shared in Chinese hacking forums: 

<br/>
<div style="text-align:center"><img src ="http://intezer.com/wp-content/uploads/2019/05/2019-05-22-182452_629x580_scrot.png" /></div>
<br/>

When we analyze the main we noticed that the first action the trojan takes is to retrieve its configuration: 

<br/>
<div style="text-align:center"><img src ="http://intezer.com/wp-content/uploads/2019/05/2019-05-23-162703_694x669_scrot.png" /></div>
<br/>

The malware configuration is appended at the end of the file and has the following structure:

<br/>
<div style="text-align:center"><img src ="http://intezer.com/wp-content/uploads/2019/05/2019-05-28-195155_776x314_scrot.png" /></div>
<br/>

The malware will try to load itself from the disk and parse this blob to then retrieve the static encrypted configuration. 

<br/>
<div style="text-align:center"><img src ="http://intezer.com/wp-content/uploads/2019/05/2019-05-23-162730_602x688_scrot.png" /></div>
<br/>

Once encryption configuration has been successfully retrieved the configuration will be decoded and then parsed as json. The cipher used to encode and decode the configuration is the following:

<br/>
<div style="text-align:center"><img src ="http://intezer.com/wp-content/uploads/2019/05/2019-05-23-162515_1073x533_scrot.png" /></div>
<br/>

This cipher seems to be an RC4 alike algorithm with an already computed PRGA generated key-stream. It is important to note that this same cipher is used later on in the network communication protocol between trojan clients and their CNCs. After the configuration is decoded the following json will be retrieved:

<br/>
<div style="text-align:center"><img src ="http://intezer.com/wp-content/uploads/2019/05/2019-05-23-165252_547x332_scrot.png" /></div>
<br/>

Moreover, if the file is running as root, the malware will attempt to change the default location of the dynamic linker’s LD_PRELOAD path. This location is usually at /etc/ld.so.preload, however there is always a possibility to patch the dynamic linker binary to change this path:

<br/>
<div style="text-align:center"><img src ="http://intezer.com/wp-content/uploads/2019/05/2019-05-23-165828_589x343_scrot.png" /></div>
<br/>

Patch_ld function will scan for any existent /lib paths. The scanned paths are the following:

<br/>
<div style="text-align:center"><img src ="http://intezer.com/wp-content/uploads/2019/05/2019-05-23-171459_539x146_scrot.png" /></div>
<br/>

The malware will attempt to find the dynamic linker binary within these paths. The dynamic linker filename is usually prefixed with ld-[version number=""].

<br/>
<div style="text-align:center"><img src ="http://intezer.com/wp-content/uploads/2019/05/2019-05-23-171605_538x442_scrot.png" /></div>
<br/>

Once the dynamic linker is located, the malware will find the offset where the /etc/ld.so.preload string is located within the binary and will overwrite it with the path of the new target preload path, that one being /sbin/.ifup-local.

<br/>
<div style="text-align:center"><img src ="http://intezer.com/wp-content/uploads/2019/05/2019-05-23-171714_614x151_scrot.png" /></div>
<br/>

To achieve this patching it will execute the following formatted string by using the xxd hex editor utility by previously having encoded the path of the rootkit in hex:

<br/>
<div style="text-align:center"><img src ="http://intezer.com/wp-content/uploads/2019/05/2019-05-23-172157_752x79_scrot.png" /></div>
<br/>

Once it has changed the default LD_PRELOAD path from the dynamic linker it will deploy a thread to enforce that the rootkit is successfully installed using the new LD_PRELOAD path. In addition, the trojan will communicate with the rootkit via the environment variable ‘I_AM_HIDDEN’ to serialize the trojan’s session for the rootkit to apply evasion mechanisms on any other sessions.

<br/>
<div style="text-align:center"><img src ="http://intezer.com/wp-content/uploads/2019/05/2019-05-23-172825_1080x583_scrot.png" /></div>
<br/>

After seeing the rootkit’s functionality, we can understand that the rootkit and trojan work together in order to help each other to remain persistent in the system, having the rootkit attempting to hide the trojan and the trojan enforcing the rootkit to remain operational. The following diagram illustrates this relationship:

<br/>
<div style="text-align:center"><img src ="http://intezer.com/wp-content/uploads/2019/05/pasted-image-0-3.png" /></div>
<br/>

Continuing with the execution flow of the trojan, a series of functions are executed to enforce evasion of some artifacts: 

<br/>
<div style="text-align:center"><img src ="http://intezer.com/wp-content/uploads/2019/05/2019-05-23-173455_514x329_scrot.png" /></div>
<br/>

These artifacts are the following:

<br/>
<div style="text-align:center"><img src ="http://intezer.com/wp-content/uploads/2019/05/2019-05-23-173529_619x157_scrot.png" /></div>
<br/>

By performing some OSINT regarding these artifact names, we found that they belong to a Chinese open-source rootkit for Linux known as [Adore-ng](https://github.com/yaoyumeng/adore-ng) hosted in GitHub: 

<br/>
<div style="text-align:center"><img src ="http://intezer.com/wp-content/uploads/2019/05/pasted-image-0-9.png" /></div>
<br/>

The fact that these artifacts are being searched for suggests that potentially targeted Linux systems by these implants may have already been compromised with some variant of this open-source rootkit as an additional artifact in this malware’s infrastructure. Although those paths are being searched for in order to hide their presence in the system, it is important to note that none of the analyzed artifacts related to this malware are installed in such paths.

This finding may imply that the target systems this malware is aiming to intrude may be already known compromised targets by the same group or a third party that may be collaborating with the same end goal of this particular campaign.

Moreover, the trojan communicated with a simple network protocol over TCP. We can see that when connection is established to the Master or Stand-By servers there is a handshake mechanism involved in order to identify the client.

<br/>
<div style="text-align:center"><img src ="http://intezer.com/wp-content/uploads/2019/05/2019-05-24-005754_610x411_scrot.png" /></div>
<br/>

With the help of this function we where able to understand the structure of the communication protocol employed. We can illustrate the structure of this communication protocol by looking at a pcap of the initial handshake between the server and client: 

<br/>
<div style="text-align:center"><img src ="http://intezer.com/wp-content/uploads/2019/05/pasted-image-0-7.png" /></div>
<br/>

We noticed while analyzing this protocol that the Reserved and Method fields are always constant, those being 0 and 1 accordingly. The cipher table offset represents the offset in the hardcoded key-stream that the encrypted payload was encoded with. The following is the fixed keystream this field makes reference to:

<br/>
<div style="text-align:center"><img src ="http://intezer.com/wp-content/uploads/2019/05/2019-05-29-164756_1179x415_scrot.png" /></div>
<br/>

After decrypting the traffic and analyzing some of the network related functions of the trojan, we noticed that the communication protocol is also implemented in json format. To show this, the following image is the decrypted handshake packets between the CNC and the trojan:

<br/>
<div style="text-align:center"><img src ="http://intezer.com/wp-content/uploads/2019/05/2019-05-24-022934_892x114_scrot.png" /></div>
<br/>

After the handshake is completed, the trojan will proceed to handle CNC requests:

<br/>
<div style="text-align:center"><img src ="http://intezer.com/wp-content/uploads/2019/05/2019-05-24-023211_974x507_scrot.png" /></div>
<br/>

Depending on the given requests the malware will perform different operations accordingly. An overview of the trojan’s functionalities performed by request handling are shown below:


<br/>
<div style="text-align:center"><img src ="http://intezer.com/wp-content/uploads/2019/05/pasted-image-0-5.png" /></div>
<br/>

#### **IOCs** 

```c
103.206.123[.]13
103.206.122[.]245 
http://103.206.123[.]13:8080/system.tar.gz 
http://103.206.123[.]13:8080/configUpdate.tar.gz 
http://103.206.123[.]13:8080/configUpdate-32.tar.gz 

e9e2e84ed423bfc8e82eb434cede5c9568ab44e7af410a85e5d5eb24b1e622e3
f321685342fa373c33eb9479176a086a1c56c90a1826a0aef3450809ffc01e5d
d66bbbccd19587e67632585d0ac944e34e4d5fa2b9f3bb3f900f517c7bbf518b
0fe1248ecab199bee383cef69f2de77d33b269ad1664127b366a4e745b1199c8
2ea291aeb0905c31716fe5e39ff111724a3c461e3029830d2bfa77c1b3656fc0
d596acc70426a16760a2b2cc78ca2cc65c5a23bb79316627c0b2e16489bf86c0
609bbf4ccc2cb0fcbe0d5891eea7d97a05a0b29431c468bf3badd83fc4414578
8e3b92e49447a67ed32b3afadbc24c51975ff22acbd0cf8090b078c0a4a7b53d
f38ab11c28e944536e00ca14954df5f4d08c1222811fef49baded5009bbbc9a2
8914fd1cfade5059e626be90f18972ec963bbed75101c7fbf4a88a6da2bc671b

```