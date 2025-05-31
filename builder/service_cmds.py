import os
from SCons.Script import DefaultEnvironment

env = DefaultEnvironment()

platform = env.PioPlatform()
board = env.BoardConfig()
mcu = board.get("build.mcu", "")
upload_protocol = env.subst("$UPLOAD_PROTOCOL")

if mcu == "K1921VK01T":
    openocd_flags=["-s", os.path.join(platform.get_package_dir("framework-k1921vk-sdk"),"tools","openocd","openocd-snippets","k1921vk035" ) or "", 
                   "-s", os.path.join(platform.get_package_dir("tool-openocd-k1921vk"),"scripts") or "",
                   "-f","interface/stlink-v2.cfg",
                   "-f","target/k1921vk01t.cfg",
                   "-c", "\"transport select hla_swd; init; reset init; flash probe 0; niietcm4 service_mode_erase 0; exit\""]
    openocd_bin  = os.path.join(platform.get_package_dir("tool-openocd-k1921vk"),"bin","openocd")
    openocd_cmd = [openocd_bin,*openocd_flags]

    env.AddCustomTarget(
        name="service_full_erase",
        dependencies=None,
        actions=[
            " ".join(openocd_cmd)
        ],
        title="service_full_erase",
        description="Service full erase when pin SERVEN = 1"
    )

if mcu == "K1921VK035":
    openocd_flags=["-s", os.path.join(platform.get_package_dir("framework-k1921vk-sdk"),"tools","openocd","openocd-snippets","k1921vk035" ) or "", 
                       "-s", os.path.join(platform.get_package_dir("tool-openocd-k1921vk"),"scripts") or "",
                       "-f","interface/%s.cfg" % upload_protocol,
                       "-f","target/k1921vk035.cfg",
                       "-c", "\"init; reset init; flash probe 0; k1921vk035 srv_erase; exit\""]
    openocd_bin  = os.path.join(platform.get_package_dir("tool-openocd-k1921vk"),"bin","openocd")
    openocd_cmd = [openocd_bin,*openocd_flags]

    env.AddCustomTarget(
        name="service_full_erase",
        dependencies=None,
        actions=[
            " ".join(openocd_cmd)
        ],
        title="service_full_erase",
        description="Service full erase when pin SERVEN = 1"
    )


    openocd_flags=["-s", os.path.join(platform.get_package_dir("framework-k1921vk-sdk"),"tools","openocd","openocd-snippets","k1921vk035" ) or "", 
                       "-s", os.path.join(platform.get_package_dir("tool-openocd-k1921vk"),"scripts") or "",
                       "-f","interface/%s.cfg" % upload_protocol,
                       "-f","target/k1921vk035.cfg",
                       "-c", "\"init; reset init; flash probe 0; k1921vk035 nvr_boot enable; reset; shutdown\""] # enable boot and disable jtag 
    openocd_bin  = os.path.join(platform.get_package_dir("tool-openocd-k1921vk"),"bin","openocd")
    openocd_cmd = [openocd_bin,*openocd_flags]

    env.AddCustomTarget(
        name="enable_boot",
        dependencies=None,
        actions=[
            " ".join(openocd_cmd),
            "python -c 'print(\"Reset mcu by reset button to apply the settings\")'"
        ],
        title="enable_boot",
        description="Enable bootloader memory,  reset bit BMODEDIS in CFGWORD"
    )

    openocd_flags=["-s", os.path.join(platform.get_package_dir("framework-k1921vk-sdk"),"tools","openocd","openocd-snippets","k1921vk035" ) or "", 
                       "-s", os.path.join(platform.get_package_dir("tool-openocd-k1921vk"),"scripts") or "",
                       "-f","interface/%s.cfg" % upload_protocol,
                       "-f","target/k1921vk035.cfg",
                       "-c", "\"init; reset init; flash probe 0; k1921vk035 nvr_boot disable; reset; shutdown\""] # enable boot and disable jtag 
    openocd_bin  = os.path.join(platform.get_package_dir("tool-openocd-k1921vk"),"bin","openocd")
    openocd_cmd = [openocd_bin,*openocd_flags]

    env.AddCustomTarget(
        name="disable_boot",
        dependencies=None,
        actions=[
            " ".join(openocd_cmd),
            "python -c 'print(\"Reset mcu by reset button to apply the settings\")'"
        ],
        title="disable_boot",
        description="Enable bootloader memory,  reset bit BMODEDIS in CFGWORD"
    )

    openocd_flags=["-s", os.path.join(platform.get_package_dir("framework-k1921vk-sdk"),"tools","openocd","openocd-snippets","k1921vk035" ) or "", 
                       "-s", os.path.join(platform.get_package_dir("tool-openocd-k1921vk"),"scripts") or "",
                       "-f","interface/%s.cfg" % upload_protocol,
                       "-f","target/k1921vk035.cfg",
                       "-c", "\"init; reset init; flash probe 0; k1921vk035 jtag enable; reset; shutdown\""] # enable boot and disable jtag 
    openocd_bin  = os.path.join(platform.get_package_dir("tool-openocd-k1921vk"),"bin","openocd")
    openocd_cmd = [openocd_bin,*openocd_flags]

    env.AddCustomTarget(
        name="disable_jtag",
        dependencies=None,
        actions=[
            " ".join(openocd_cmd),
            "python -c 'print(\"Reset mcu by reset button to apply the settings\")'"
        ],
        title="disable_jtag",
        description="Disable jtag, reset bit JTAGEN in CFGWORD"
    )
