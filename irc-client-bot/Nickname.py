
import names
import logging

class Nickname():

    def __init__(self):
        self.nickname = names.get_full_name().replace(' ', '').lower()
        logging.info("nickname: %s", self.nickname)

