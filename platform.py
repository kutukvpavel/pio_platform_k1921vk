# Copyright 2014-present PlatformIO <contact@platformio.org>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import os

from platform import system

from platformio.managers.platform import PlatformBase
from platformio.util import get_systype

class K1921vkPlatform(PlatformBase):

    def configure_default_packages(self, variables, targets):
        board = variables.get("board")
        board_config = self.board_config(board)
        build_core = variables.get(
            "board_build.core", board_config.get("build.core", "arduino"))
        build_mcu = variables.get("board_build.mcu", board_config.get("build.mcu", ""))
        frameworks = variables.get("pioframework", [])
        return PlatformBase.configure_default_packages(self, variables,
                                                       targets)

    def get_boards(self, id_=None):
        result = PlatformBase.get_boards(self, id_)
        if not result:
            return result
        if id_:
            return self._add_default_debug_tools(result)
        else:
            for key, value in result.items():
                result[key] = self._add_default_debug_tools(result[key])
        return result

    def _add_default_debug_tools(self, board):
        non_debug_protocols = ["k1921vkx_flasher"]
        SDK_DIR = self.get_package_dir("framework-k1921vk-sdk")
        mcu = board.get("build.mcu", "")
        debug = board.manifest.get("debug", {})
        upload_protocols = board.manifest.get("upload", {}).get(
            "protocols", [])
        if "tools" not in debug:
            debug['tools'] = {}

        # J-Link, ST-Link
        for link in upload_protocols:
            if link not in upload_protocols or link in debug['tools'] or link in non_debug_protocols:
                continue

            server_args = ["-s", "$PACKAGE_DIR/scripts"]
            server_args.extend([
                    "-s", os.path.join(SDK_DIR or "","tools","openocd","openocd-snippets",mcu.lower())
                ])
            if debug.get("openocd_board"):
                server_args.extend([
                    "-f", "board/%s.cfg" % debug.get("openocd_board")
                ])
            else:
                assert debug.get("openocd_target"), (
                    "Missed target configuration for %s" % board.id)
                server_args.extend([
                    "-f", "connect_%s.cfg" % link
                ])
                server_args.extend(debug.get("openocd_extra_args", []))
            debug['tools'][link] = {
                "server": {
                    "package": "tool-openocd-k1921vk",
                    "executable": "bin/openocd",
                    "arguments": server_args
                }
            }
        board.manifest['debug'] = debug
        return board
