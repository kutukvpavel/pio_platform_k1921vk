import glob
import os
import string
from SCons.Script import DefaultEnvironment

env = DefaultEnvironment()

platform = env.PioPlatform()
board = env.BoardConfig()
mcu = board.get("build.mcu", "")
f_ext = board.get("build.f_ext", "")
clk_select = board.get("build.clk_select", "")
clk_select_def = {"pll":"SYSCLK_PLL","internal":"SYSCLK_OSI","external":"SYSCLK_OSE","custom":""}

env.Append(
    ASFLAGS=[
        "-mthumb",
        "-mcpu=cortex-m4"
    ],

    CCFLAGS=[
        "-mthumb", 
        "-mcpu=cortex-m4",
        "-mfloat-abi=hard",
        "-mfpu=fpv4-sp-d16",
        "-Wall",
        "-Wextra",
        "-Os",
        #"-flto",
        #"-ffat-lto-objects",
        "-ffunction-sections",
        "-fno-builtin",
        "-fdata-sections",
        "-mlong-calls",
        "-fsingle-precision-constant"

    ],

    CXXFLAGS=[
        "-std=c++11",
        "-fno-exceptions",
        "-mcpu=cortex-m4",
        "-mfloat-abi=hard",
        "-mfpu=fpv4-sp-d16",
        "-mthumb",
        "-c",
        "-O1",
        "-ffunction-sections",
        "-fdata-sections",
        "-mlong-calls",
        "-nostdlib", 
        "-fno-threadsafe-statics",
        "-fno-rtti",
        "-fno-exceptions",
        "-fno-use-cxa-atexit",
        "-MMD",
        "-fsingle-precision-constant"
    ],

    CPPDEFINES=[
        ("OSECLK_VAL", str(f_ext)),# OSECLK value in Hz (0 if disconnected)
        (mcu),# MCU name
        ("MCUNAME",mcu),
        (clk_select_def[clk_select]), # SYSCLK source: PLL, OSI, OSE
        ("_GNU_SOURCE")
    ],

    LINKFLAGS=[
        "-mthumb",
        "-Os",
        "-mcpu=cortex-m4",
        "-mfloat-abi=hard",
        "-mfpu=fpv4-sp-d16",
        "-mlong-calls",
        "-Wl,--gc-sections",
        "-specs=nosys.specs",
        "-specs=nano.specs",
        "-lgcc",
        "-lc",
        "-flto"
    ],

    LIBS=["c", "gcc", "m", "stdc++"]
)



# copy CCFLAGS to ASFLAGS (-x assembler-with-cpp mode)
#env.Append(ASFLAGS=env.get("CCFLAGS", [])[:])
