---
title: PicoCTF - Some Assembly Required 1
date: 2023-12-14
categories: [CTF, Web Exploitation]
tags: [picoctf, web-exploitation, assembly, ]
img_path: /assets/picoctf/web_exploitation/assembly_required_1
published: true
---

![](room_banner.png){: width='80%'}

1. Visiting the site we encounter just an input box:

    ![](home.png)

    ![](test_incorrect.png)

2. Inspecting the page we notice two files:

    ![](first_js.png)

    ![](second_js.png)

3. The first one looks like obfuscated JS code:

    ```javascript
        const _0x402c = [
    'value',
    '2wfTpTR',
    'instantiate',
    '275341bEPcme',
    'innerHTML',
    '1195047NznhZg',
    '1qfevql',
    'input',
    '1699808QuoWhA',
    'Correct!',
    'check_flag',
    'Incorrect!',
    './JIFxzHyW8W',
    '23SMpAuA',
    '802698XOMSrr',
    'charCodeAt',
    '474547vVoGDO',
    'getElementById',
    'instance',
    'copy_char',
    '43591XxcWUl',
    '504454llVtzW',
    'arrayBuffer',
    '2NIQmVj',
    'result'
    ];
    const _0x4e0e = function (_0x553839, _0x53c021) {
    _0x553839 = _0x553839 - 470;
    let _0x402c6f = _0x402c[_0x553839];
    return _0x402c6f;
    };
    (
    function (_0x76dd13, _0x3dfcae) {
        const _0x371ac6 = _0x4e0e;
        while (!![]) {
        try {
            const _0x478583 = - parseInt(_0x371ac6(491)) + parseInt(_0x371ac6(493)) + - parseInt(_0x371ac6(475)) * - parseInt(_0x371ac6(473)) + - parseInt(_0x371ac6(482)) * - parseInt(_0x371ac6(483)) + - parseInt(_0x371ac6(478)) * parseInt(_0x371ac6(480)) + parseInt(_0x371ac6(472)) * parseInt(_0x371ac6(490)) + - parseInt(_0x371ac6(485));
            if (_0x478583 === _0x3dfcae) break;
            else _0x76dd13['push'](_0x76dd13['shift']());
        } catch (_0x41d31a) {
            _0x76dd13['push'](_0x76dd13['shift']());
        }
        }
    }(_0x402c, 627907)
    );
    let exports;
    (
    async() => {
        const _0x48c3be = _0x4e0e;
        let _0x5f0229 = await fetch(_0x48c3be(489)),
        _0x1d99e9 = await WebAssembly[_0x48c3be(479)](await _0x5f0229[_0x48c3be(474)]()),
        _0x1f8628 = _0x1d99e9[_0x48c3be(470)];
        exports = _0x1f8628['exports'];
    }
    ) ();
    function onButtonPress() {
    const _0xa80748 = _0x4e0e;
    let _0x3761f8 = document['getElementById'](_0xa80748(484)) [_0xa80748(477)];
    for (let _0x16c626 = 0; _0x16c626 < _0x3761f8['length']; _0x16c626++) {
        exports[_0xa80748(471)](_0x3761f8[_0xa80748(492)](_0x16c626), _0x16c626);
    }
    exports['copy_char'](0, _0x3761f8['length']),
    exports[_0xa80748(487)]() == 1 ? document[_0xa80748(494)](_0xa80748(476)) [_0xa80748(481)] = _0xa80748(486) : document[_0xa80748(494)](_0xa80748(476)) [_0xa80748(481)] = _0xa80748(488);
    }
    ```

4. The second one looks like assembly code, and inside the `wasm` directory. So, let's find out what that is:

    _[WebAssembly](https://developer.mozilla.org/en-US/docs/WebAssembly) is a type of code that can be run in modern web browsers — it is a low-level assembly-like language with a compact binary format that runs with near-native performance and provides languages such as C/C++, C# and Rust with a compilation target so that they can run on the web. It is also designed to run alongside JavaScript, allowing both to work together._

    The wasm script is quite large, but we can see its start and end below:

    ```wasm
        (module
    (table $table0 1 1 funcref)
    (memory $memory0 2)
    (global $global0 (mut i32) (i32.const 66864))
    (global $global1 i32 (i32.const 1072))
    (global $global2 i32 (i32.const 1024))
    (global $global3 i32 (i32.const 1328))
    (global $global4 i32 (i32.const 1024))
    (global $global5 i32 (i32.const 66864))
    (global $global6 i32 (i32.const 0))
    (global $global7 i32 (i32.const 1))
    (export "memory" (memory $memory0))
    (export "__wasm_call_ctors" (func $func0))
    (export "strcmp" (func $func1))
    (export "check_flag" (func $func2))
    (export "input" (global $global1))
    (export "copy_char" (func $func3))
    (export "__dso_handle" (global $global2))
    (export "__data_end" (global $global3))
    (export "__global_base" (global $global4))
    (export "__heap_base" (global $global5))
    (export "__memory_base" (global $global6))
    (export "__table_base" (global $global7))
    (func $func0
    ...

    ...
    (func $func3 (param $var0 i32) (param $var1 i32)
        (local $var2 i32) (local $var3 i32) (local $var4 i32) (local $var5 i32) (local $var6 i32)
        global.get $global0
        local.set $var2
        i32.const 16
        local.set $var3
        local.get $var2
        local.get $var3
        i32.sub
        local.set $var4
        local.get $var4
        local.get $var0
        i32.store offset=12
        local.get $var4
        local.get $var1
        i32.store offset=8
        local.get $var4
        i32.load offset=12
        local.set $var5
        local.get $var4
        i32.load offset=8
        local.set $var6
        local.get $var6
        local.get $var5
        i32.store8 offset=1072
        return
    )
    (data (i32.const 1024) "picoCTF{d88090e679c48f3945fcaa6a7d6d70c5}\00\00")
    )
    ```

    Our flag is just at the end of it!

    ![](flag_correct.png)

    ![](room_pwned.png)