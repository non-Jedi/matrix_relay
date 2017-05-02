# Copyright 2016, 2017 Adam Beckmeyer
#
# This file is part of matrix_relay.
#
# matrix_relay is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# matrix_relay is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with matrix_relay.  If not, see
# <http://www.gnu.org/licenses/>.
import json
import os
from .relay import ReqHandler


# Load configuration
dir_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
with open(os.path.join(dir_path, "config.json"), "r") as f:
    config = json.load(f)

# Define objects that will run the wsgi app
handler = ReqHandler(config)
app = handler.app
