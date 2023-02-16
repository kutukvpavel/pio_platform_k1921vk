import sys
from os.path import join, isfile

from SCons.Script import DefaultEnvironment, SConscript

env = DefaultEnvironment()
mcu = env.BoardConfig().get("build.mcu")
core = env.BoardConfig().get("build.core", "")

env.SConscript("_bare.py")

build_script = join(env.PioPlatform().get_package_dir(
        "vostok-1-frmwrk-vn-arduino"), "tools", "platformio", "platformio-build.py")

if not isfile(build_script):
    sys.stderr.write("Error: Missing PlatformIO build script %s!\n" % build_script)
    env.Exit(1)

SConscript(build_script)