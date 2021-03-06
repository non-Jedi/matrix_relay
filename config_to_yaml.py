# Copyright 2016 Adam Beckmeyer
#
# This file is part of Matrix Relay.
#
# Matrix Relay is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Matrix Relay is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Matrix Relay.  If not, see
# <http://www.gnu.org/licenses/>.
"""Copies config.json in same directory to config.yaml

Since Synapse currently doesn't take json-formatted config, this script is
necessary
"""

import json
import yaml
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(dir_path, "config.json"), "r") as json_config:
    with open(os.path.join(dir_path, "config.yaml"), "w") as yaml_config:
        yaml.dump(json.load(json_config), yaml_config)
