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
from string import ascii_lowercase, ascii_uppercase


def mxid2localpart(mxid):
    """Converts mxid of form @localpart:domain to an allowable localpart string.

    Args:
        mxid(str): The string to convert into allowable localpart.
    """
    sub_lower = ["".join(("_", i)) for i in ascii_lowercase]
    munge_rules = dict(zip(ascii_uppercase, sub_lower))
    # mxid localparts cannot contain @ or :
    munge_rules.update({"@": "=40", ":": "=3a"})
    return mxid.translate(str.maketrans(munge_rules))
