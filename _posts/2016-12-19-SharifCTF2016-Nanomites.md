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

My next steps after knowing this was to analyze it with IDA in order to retrive behavioral analysis.

Looking for strings XREFs, I found myself with the IP address of the C&C:

![Indirizzo IP](https://github.com/jbzteam/CTF/raw/master/SharifCTF2016/Nanomites/ip_address.png)

Troviamo l'indirizzo IP: `155.64.16.51`.

Ok, abbiamo recuperato la prima informazione. Adesso dobbiamo trovare i dati. Dato che quell'indirizzo IP è attivo (o almeno lo era durante il CTF), lanciamo l'eseguibile e mettiamo in ascolto wireshark. Una volta stabilita la connessione troviamo il payload:

![Payload trasmesso](https://raw.githubusercontent.com/jbzteam/CTF/master/SharifCTF2016/Nanomites/wireshark.png)

Ovviamente è cifrato. Cerchiamo nel binario come. Sappiamo che i dati vengono spediti, quindi scrollando verso il basso nell'asm cerchiamo una chiamata alla funzione `send`, e la troviamo qui:

![Funzione send](https://raw.githubusercontent.com/jbzteam/CTF/master/SharifCTF2016/Nanomites/send.png)

Vediamo che la variabile che contiene i dati è chiamata `buf` quindi scrolliamo in su per capire come viene generato quel buffer. Vediamo che ad un certo punto la variabile `buf` viene passata alla funzione `sub_401260`:

![Funzione contenente xor](https://raw.githubusercontent.com/jbzteam/CTF/master/SharifCTF2016/Nanomites/xor_function.png)

Che contiene:

![Cifratura con xor](https://raw.githubusercontent.com/jbzteam/CTF/master/SharifCTF2016/Nanomites/xor.png)

Notiamo che nella variabile `var_1` viene inserito il valore `0x44`, poi viene incrementata di `2` e viene usata per fare uno `xor`. La chiave quindi è `0x46`.

Con un paio di righe di python decifriamo il payload:

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
