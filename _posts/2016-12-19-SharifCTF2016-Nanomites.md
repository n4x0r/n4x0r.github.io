---
layout: post
title:  "SharifCTF7 - Nanomites"
date:   2016-12-19 20:30
categories: CTF
tags: [reverse,SharifCTF7]
author: n4x0r
---

Nanomites was a Reverse engineering challenge of 300 point in SharifCTF7. The specification of this problem was the following: 

```bash
Analyze the given file. Find the C&C IP address and the data sent to it in plain text.
Flag = SharifCTF{md5(strcat(IP, Data))}_
```
For the ones that coud not attend the competition, You can download the challenge from [here](../files/Nanomites.exe).

After running the command `file` against the binary, I got the following output:

`Nanomites.exe: PE32 executable (GUI) Intel 80386, for MS Windows`

My next steps after knowing this was to analyze it with IDA in order to find  out any evidence of the binary connecting to a remote host.

Once the file is in IDA, we can see that the binary is some what obfuscated.

![relative call](https://github.com/n4x0r/n4x0r.github.io/raw/master/images/SharifCTF7/1.png)
![int3](https://github.com/n4x0r/n4x0r.github.io/raw/master/images/SharifCTF7/2.png)

Looking for strings XREFs, I found myself with the IP address of the C&C:

![C&C IP](https://github.com/n4x0r/n4x0r.github.io/raw/master/images/SharifCTF7/3.png)

After knowing the IP address of the C&C, I then opened wireshark to see if I could intercept any communications. I indeed intercepted a stream. This stream looked like this:

![Message intercpeted](https://github.com/n4x0r/n4x0r.github.io/raw/master/images/SharifCTF7/4.png)

Clearly that message that our host was sending to `155.64.16.51` is encrypted.

After knowing this information, then I proceeded to look where the application sent the encrypted buffer.
Looking at the imported functions. We can see that `send` is at address `0x40151d`

![send XREF](https://github.com/n4x0r/n4x0r.github.io/raw/master/images/SharifCTF7/5.png)



```python
data = [ 0x12, 0x2e, 0x2f, 0x35, 0x19, 0x0f, 0x35, 0x19, 0x12, 0x2e, 0x23, 0x19, 0x15, 0x23, 0x25, 0x34, 0x23, 0x32, 0x19, 0x02, 0x27, 0x32, 0x27, 0x46 ]
print ''.join([chr(x ^ 0x46) for x in data])
```

E otteniamo come output `This_Is_The_Secret_Data`.

Sappiamo quindi i due valori necessari per calcolare la flag. Dopo averli concatenati, ne calcoliamo l'`md5`:

```bash
$ echo -n '155.64.16.51This_Is_The_Secret_Data' | md5
fb0e90f2ec7a701783e70e674fa94848
```

La flag è quindi `SharifCTF{fb0e90f2ec7a701783e70e674fa94848}`.
