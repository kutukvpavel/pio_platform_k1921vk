# NIIET K1921VK: development platform for [PlatformIO](http://platformio.org)


# Usage

1. [Install VS_Code](https://code.visualstudio.com/)  
2. [Install VS_Code+PlatformIO](https://docs.platformio.org/en/latest/integration/ide/vscode.html#ide-vscode)  
3. Create PlatformIO project and configure a platform option in [platformio.ini](http://docs.platformio.org/page/projectconf.html) file:

## Stable version

```ini
[env:stable]
platform = k1921vk
framework = k1921vk_sdk
board = generic_K1921VK01T
...
```

# Configuration
platformio.ini example:
```ini
[platformio]
default_envs = release, debug

[env]
platform = k1921vk
board = kfdl441546
framework = k1921vk_sdk
board_build.f_ext = 12000000L # OSECLK_VAL 
board_build.clk_select = pll #pll - SYSCLK_PLL , internal - SYSCLK_OSI , external - SYSCLK_OSE
debug_tool = stlink
upload_protocol = stlink

[env:release]
build_type = release

[env:debug]
build_type = debug
build_flags = -DRETARGET
```

* `board_build.f_ext` - frequency of external clock source (qurtz oscillator)
* `board_build.clk_select` - select clock source for sysCLK
  * `pll` - define SYSCLK_PLL, pll use external clock source and set sysCLK to 100Mhz. pll mode supports `board_build.f_ext` only with values: 8000000L, 12000000L, 16000000L, 20000000L, 24000000L
  * `internal` - define SYSCLK_OSI, use internal clock source. K1921VK01T: 5 Mhz, K1921VK028: 16 Mhz, K1921VK035 8 Mhz
  * `external` - define SYSCLK_OSE, use external clock source
  * `custom` - nothing define, you should configure clock by youself
* `debug_tool` - you can use for debug `stlink`
* `upload_tool` - you can use for upload `stlink`