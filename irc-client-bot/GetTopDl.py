#! /usr/bin/env python
#
# Example program using irc.client.
#
# This program is free without restrictions; do anything you like with
# it.
#

import os
import sys
import argparse
import itertools
import time
import yaml
import threading

import irc.client

import string
import logging
import Nickname

target = None
"The nick or channel to which to send messages"

def filter_nonprintable(text):
    # Get the difference of all ASCII characters from the set of printable characters
    nonprintable = set([chr(i) for i in range(128)]).difference(string.printable)
    # Use translate to remove all non-printable characters
    return text.translate({ord(character):None for character in nonprintable})

def is_file(text):
    '''
    return filesize if file exists
    '''
    filename = text.split()[1]
    if not os.path.isfile(filename):
        return text

    filesize = os.stat(filename).st_size
    return text + " exists {} rm".format(filesize)

class Lister():
    def __init__(self):
        self.done = threading.Event()
        self.underscores_count = 0
        self.notices = list()

    def on_notice(self, connection, event):
        '''
        grab notice messages and append to self.notices list
        '''
        for arg in event.arguments:
            printable = filter_nonprintable(arg)
            if printable.startswith('_________') and printable.endswith('____________'):
                self.underscores_count += 1
                logging.debug("underscores_count: %s", self.underscores_count)
            elif printable.startswith(' '):
                printable = is_file(printable.strip())
                self.notices.append(printable)
                logging.debug(self.notices[-1])

            if self.underscores_count == 3:
                connection.quit("goodbye")

    def on_connect(self, connection, event):
        '''
        when connected to irc server, join the target server
        '''
        if irc.client.is_channel(target):
            connection.join(target)
            self.send_msg_to_channel(connection)
            return

    def send_msg_to_channel(self, connection):
        time.sleep(5)
        logging.debug('send topdl')
        connection.privmsg(target, '!topdl')

    def on_disconnect(self, connection, event):
        '''
        when we disconnect from server, set done flag
        '''
        self.done.set()

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--server', default='irc.abjects.net', required=False)
    parser.add_argument('-t', '--target', default='#mg-chat', required=False)
    parser.add_argument('-p', '--port', default=6667, type=int, required=False)
    return parser.parse_args()

class Args():
    def __init__(self):
        self.server = 'irc.abjects.net'
        self.target = '#mg-chat'
        self.port = 6667

def get_top_dl():

    now = time.time()
    cache_file = 'get_top_dl.cache.yml'

    if os.path.isfile(cache_file):
        filetime = os.stat(cache_file).st_mtime
        if now - filetime < 10 * 60:
            logging.debug('returning cache')
            return yaml.safe_load(open(cache_file, 'r'))

    l = Lister()
    t = threading.Thread(target=get_listing, args=(l,),)
    t.daemon = True
    t.start()

    l.done.wait(60.0)

    with open(cache_file, 'w') as fout:
        yaml.safe_dump(l.notices, fout)

    return l.notices

def get_listing(lister):
    global target

    nickname = Nickname.Nickname()

    args = Args()
    target = args.target

    reactor = irc.client.Reactor()
    try:
        c = reactor.server().connect(args.server, args.port, nickname.nickname)
    except irc.client.ServerConnectionError:
        print(sys.exc_info()[1])
        raise SystemExit(1)

    c.add_global_handler("privnotice", lister.on_notice)
    c.add_global_handler("welcome", lister.on_connect)
    c.add_global_handler("disconnect", lister.on_disconnect)

    reactor.process_forever()

if __name__ == '__main__':

    logging.basicConfig(
            #filename='HISTORYlistener.log',
            level=logging.DEBUG,
            format='%(asctime)s %(levelname)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            )


    listing = get_top_dl()
    for item in listing:
        logging.debug(item)
