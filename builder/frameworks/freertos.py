import sys
from os.path import join, isfile

from SCons.Script import DefaultEnvironment, SConscript

env = DefaultEnvironment()

env.SConscript("k1921vk-sdk.py")

build_script = join(env.PioPlatform().get_package_dir(
    "framework-k1921vk-freertos"), "platformio-build.py")

if not isfile(build_script):
    sys.stderr.write(
        "Error: Missing PlatformIO build script %s!\n" % build_script)
    env.Exit(1)

SConscript(build_script)
