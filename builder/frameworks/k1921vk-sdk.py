import glob
import os
import string

from SCons.Script import DefaultEnvironment

env = DefaultEnvironment()
platform = env.PioPlatform()
board = env.BoardConfig()
mcu = board.get("build.mcu", "")

env.SConscript("_bare.py")

SDK_DIR = platform.get_package_dir("framework-k1921vk-sdk")
DEVICE_DIR =  os.path.join(SDK_DIR,"platform","Device","NIIET",mcu)
DEVICE_RETARGET_DIR = os.path.join(SDK_DIR,"platform","retarget","Template",mcu)
DEVICE_SDK_DIR = ""
if mcu == "K1921VK01T":
    DEVICE_SDK_DIR=os.path.join(SDK_DIR,"platform","niietcm4_pd")
elif mcu == "K1921VK028":
    DEVICE_SDK_DIR=os.path.join(SDK_DIR,"platform","plib028")
elif mcu == "K1921VK035":
    DEVICE_SDK_DIR=os.path.join(SDK_DIR,"platform","plib035")

env.Append(
        CPPPATH=[
            os.path.join(DEVICE_SDK_DIR, "inc")
        ],
    )

if not board.get("build.ldscript", ""):
    env.Replace(LDSCRIPT_PATH=os.path.join(DEVICE_DIR, "Source","GCC","%s.ld"%mcu))


env.Append(
    CPPPATH=[
        os.path.join(DEVICE_DIR, "Include"),
        os.path.join( SDK_DIR, "platform","CMSIS","Core","Include")
    ]
)

#
# Compile startup_script
#
if not board.get("build.custom_startup_script", ""):
    sources_path = os.path.join(DEVICE_DIR, "Source","GCC")
    env.BuildSources(
        os.path.join("$BUILD_DIR", "startup_script"), sources_path,
        src_filter=[
            "-<*>",
            "+<startup_%s.S>" % mcu]
    )
else:
    sources_path =  os.path.dirname(board.get("build.custom_startup_script", ""))
    file_name =  os.path.basename(board.get("build.custom_startup_script", ""))
    print(sources_path)
    print(file_name) 
    env.BuildSources(
        os.path.join("$BUILD_DIR", "startup_script"), sources_path,
        src_filter=[
            "-<*>",
            "+<%s>" % file_name]
    )

#
# Compile CMSIS sources
#

sources_path = os.path.join(DEVICE_DIR, "Source")
env.BuildSources(
    os.path.join("$BUILD_DIR", "FrameworkCMSIS"), sources_path,
    src_filter=[
        "-<*>",
        "+<system_%s.c>" % mcu]
)

#
# Compile device SDK sources
#

sources_path = os.path.join(DEVICE_SDK_DIR, "src")
env.BuildSources(
    os.path.join("$BUILD_DIR", "device_sdk"), sources_path,
    src_filter=[
        "+<*>"]
)

#
# Compile retarget sources
#

# sources_path = DEVICE_RETARGET_DIR
# env.BuildSources(
#     os.path.join("$BUILD_DIR", "retarget_conf"), sources_path,
#     src_filter=[
#         "+<retarget_conf.c>"]
# )
# sources_path = os.path.join(SDK_DIR,"platform","retarget")
# env.BuildSources(
#     os.path.join("$BUILD_DIR", "retarget"), sources_path,
#     src_filter=[
#         "+<retarget.c>"]
# )