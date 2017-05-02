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
from gyr.server import Application
from gyr.matrix_objects import MatrixUser, MatrixRoom
from string import ascii_lowercase, ascii_uppercase

# Utility functions


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

# Class that interacts with app


class ReqHandler:
    """Attaches handlers to internal wsgi app to relay events."""

    def __init__(self, config):
        self.config = config
        self.app = Application(config["homeserver_addr"], config["as_token"])
        self.api = self.app.create_api()
        # {"!source:room": [["@relayed:users"], ["@relayed:to.rooms"]]}
        # An empty list of users indicates all users relayed
        self.links = {}
        # "@real:username": MatrixUser("@as_user:domain")
        self.users = {}

        self._process_links(config["relay"])
        self.app.add_handlers(room_handler=self._handle_room,
                              user_handler=self._handle_user,
                              transaction_handler=self._handle_txn)

    def _process_links(self, links_dict):
        self.links.update(links_dict)
        # Check for existence of users and rooms we're supposed to relay to
        for source_id, val in links_dict.items():
            if val[0]:
                unknown_users = (u for u in val[0] if u not in self.users)
                for user_id in unknown_users:
                    self.users[user_id] = MatrixUser(
                        mxid2localpart(user_id), self.app.create_api
                    )
            # Empty list means that all users must be relayed
            else:
                room = MatrixRoom(source_id, self.api)
                unknown_users = (u for u in room.members if u not in self.users)
                for user_id in unknown_users:
                    self.users[user_id] = MatrixUser(
                        mxid2localpart(user_id), self.app.create_api
                    )

    def _handle_room(room_id):
        return False

    def _handle_user(user_id):
        return False

    def _handle_txn(event_stream):
        return True
