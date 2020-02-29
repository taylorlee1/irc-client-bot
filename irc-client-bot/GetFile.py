#! /usr/bin/env python
#
# Example program using irc.client.
#
# This program is free without restrictions; do anything you like with
# it.
#

#from __future__ import print_function

import time
import os
import struct
import sys
import argparse
import shlex
import logging
import Nickname

import irc.client
logging.basicConfig(level=logging.INFO)


class DCCReceive(irc.client.SimpleIRCClient):
    def __init__(self, filename=None):
        irc.client.SimpleIRCClient.__init__(self)
        self.received_bytes = 0
        self.filename = filename

    def on_ctcp(self, connection, event):
        payload = event.arguments[1]
        parts = shlex.split(payload)
        command, filename, peer_address, peer_port, size = parts
        if command != "SEND":
            return
        self.filename = os.path.basename(filename)
        if os.path.exists(self.filename):
            print("A file named", self.filename, "already exists. Refusing to save it.")
            self.connection.quit()
            return
        self.file = open(self.filename, "wb")
        logging.info("getting %s", self.filename)
        peer_address = irc.client.ip_numstr_to_quad(peer_address)
        peer_port = int(peer_port)
        self.dcc = self.dcc_connect(peer_address, peer_port, "raw")

    def on_dccmsg(self, connection, event):
        data = event.arguments[0]
        self.file.write(data)
        self.received_bytes = self.received_bytes + len(data)
        self.dcc.send_bytes(struct.pack("!I", self.received_bytes))

    def on_dcc_disconnect(self, connection, event):
        self.file.close()
        print("Received file %s (%d bytes)." % (self.filename, self.received_bytes))
        self.connection.quit()

    def on_disconnect(self, connection, event):
        sys.exit(0)

    '''
    custom
    '''
    def on_welcome(self, c, e):
        c.join('#moviegods')
        c.join('#mg-chat')

        time.sleep(10)

        self.connection.privmsg('#mg-chat', '!g {}'.format(self.filename))
        logging.info("requesting %s", self.filename)

def get_args():
    parser = argparse.ArgumentParser(
        description="Receive a single file to the current directory via DCC "
        "and then exit."
    )
    parser.add_argument('-s', '--server', default='irc.abjects.net')
    parser.add_argument('-p', '--port', default=6667, type=int)
    parser.add_argument('--filename', default=None, required=True)
    return parser.parse_args()

def get_file():
    args = get_args()

    if os.path.isfile(args.filename):
        logging.warning("%s exists, returning", args.filename)
        return

    nickname = Nickname.Nickname()
    c = DCCReceive(filename=args.filename)
    try:
        c.connect(args.server, args.port, nickname.nickname)
    except irc.client.ServerConnectionError as x:
        print(x)
        sys.exit(1)
    c.start()

if __name__ == "__main__":
    get_file()
