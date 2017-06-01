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
from . import utils


# Class that interacts with app


class ReqHandler:
    """Attaches handlers to internal wsgi app to relay events."""

    def __init__(self, config):
        self.config = config
        self.app = Application(config["homeserver_addr"], config["hs_token"])
        self.api = self.app.Api()
        # {"!source:room": {"@ex:user": ["!relayed:to.rooms"]}}
        # An empty string indicates all users relayed
        self.links = {}
        # {"@real:username": {"!room:id": MatrixRoom}}
        self.users = {}

        self._process_links(config["links"])
        self.app.add_handlers(room_handler=self._handle_room,
                              user_handler=self._handle_user,
                              transaction_handler=self._handle_txn)

    def _process_links(self, links_dict):
        self._verify_links_format(links_dict)
        # TODO: what if already relaying from a room?
        self.links.update(links_dict)
        for source_room_id, user_dict in links_dict.items():
            for user_id in user_dict:
                if user_id and user_id not in self.users:
                    for room_id in user_dict[user_id]:
                        a = self.app.Api(identity=utils.mxid2localpart(user_id))
                        rm = MatrixRoom(room_id, a)
                        self.users[user_id][room_id] = rm
                # Empty list means that all users must be relayed
                elif not user_id:
                    room = MatrixRoom(source_room_id, self.api)
                    unknown_users = (u for u in room.members if u not in self.users)
                    for user_id in unknown_users:
                        self.users[user_id] = MatrixUser(
                            utils.mxid2localpart(user_id), self.app.Api
                        )

            # TODO: Check existence of source room

    def _verify_links_format(self, links_dict):
        # TODO: should raise error if bad format
        pass

    def _handle_room(self, room_id):
        return False

    def _handle_user(self, user_id):
        return False

    def _handle_txn(self, event_stream):
        # TODO
        for event in event_stream:
            if (
                event.id in self.links and
                event.type == "m.room.message" and
                event.mxid in self.links[event.id]
            ):
                for user_id in self.links[event.id]:
                    for dest_room_id in self.links[event.id][user_id]:
                        rm = self.users[user_id][dest_room_id]
                        rm.send_notice(event.content["body"])
        return True
