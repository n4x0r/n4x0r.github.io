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

Based on the arguments that sends has. we can see the buffer that contains the data intercepted.
If we look above `send` we can see that this buffer is passed to two more functions. these are at `0x402C97` and `0x401260`

![0x402c97](https://github.com/n4x0r/n4x0r.github.io/raw/master/images/SharifCTF7/6.png)

![0x401260](https://github.com/n4x0r/n4x0r.github.io/raw/master/images/SharifCTF7/7.png)

For sake of simplicity we are not really going to explain the purpose of function 0x402c97 since I think this function is merely used for confusion purposes. Depending how well we do debugging it, this function will return a value of `34`, `22`, `0` or instead redirect execution into an end_point of execution. More over this function even thou retrieves a different return value in `eax` depending of which path is executed, this return value is never actually used outside the context of itself. However it really doesnt matter what this function returns. The actual purpose of this function is to copy the contents of its 3rd argument to its 1st argument. wheter this copy transaction will be successfull will be determind by the value of the second argument. The following is a decpmpilation of this function:

```c
signed int __cdecl copy_cond(char *copy, int centinel, char *payload) {
  int v3; 
  _DWORD *v4; 
  signed int v5; 
  char v7; 
  signed int v8; 

  __debugbreak();
  v3 = centinel;
  if ( !centinel )
    goto LABEL_4;
  if ( !payload )
  {
    *copy = 0;
LABEL_4:
    v4 = junk();
    v8 = 22;
    goto LABEL_5;
  }
  v7 = *payload;
  *copy = *payload;
  if ( v7 )
  {
    v3 = centinel - 1;
    __debugbreak();
  }
  if ( v3 )
    return 0;
  *copy = 0;
  v4 = junk();
  v8 = 34;
LABEL_5:
  v5 = v8;
  *v4 = v8;
  trigger_exception();
  return v5;
}
```

However something more interesting happens when we analyze the function at `0x401260`. In this function, the function discussed above (`copy_con`) is called. Interesting enough, one of its arguments results some what familiar:

![payload](https://github.com/n4x0r/n4x0r.github.io/raw/master/images/SharifCTF7/8.png)

![payload_dump](https://github.com/n4x0r/n4x0r.github.io/raw/master/images/SharifCTF7/9.png)

That is the encrypted payload we intercepted previously with wireshark. Assuming that the contents of the payload are copied to the first argument of that call, seeing the following will be enlighten:

![xor_routine](https://github.com/n4x0r/n4x0r.github.io/raw/master/images/SharifCTF7/9.png) 

The previous routine is xoring each byte of the copy of the payload with `70 (0x46)`. Knowing this, I run the following python script:

```python
#!usr/bin/env python

payload = [ 0x12, 0x2e, 0x2f, 0x35, 0x19, 0x0f, 0x35, 0x19, \
            0x12, 0x2e, 0x23, 0x19, 0x15, 0x23, 0x25, 0x34, \
            0x23, 0x32, 0x19, 0x02, 0x27, 0x32, 0x27, 0x46 ]

print ''.join([chr(i ^ 70) for i in payload])

```

The output of this script is: `This_Is_The_Secret_Data`.

Having found the secret message, and knowing the IP address of the C&C server we can find the md5 for our flag, which happens to be:

`SharifCTF{fb0e90f2ec7a701783e70e674fa94848}`.

