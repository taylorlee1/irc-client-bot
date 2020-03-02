
import os
import sys
import time
import logging

class RemoveFile():
    min_age = 10 # minutes

    def __init__(self, infile=None):
        self.infile = infile

    def remove_file(self):
        realpath = os.path.realpath(self.infile)

        if os.path.isfile(self.infile):
            try:
                filetime = os.stat(realpath).st_mtime
                now = time.time()
                if now - filetime < RemoveFile.min_age * 60:
                    logging.info("cannot remove young file %s", realpath)
                    return {
                            'msg' : '{} is too young to remove'.format(self.infile),
                            }

            except Exception as e:
                logging.error(e)
        else:
            return {
                    'msg' : '{} not found'.format(self.infile),
                    }

        self._remove_file()

    def _remove_file(self):

        res1 = self.unlink(self.infile)
        res2 = self.unlink(realpath)

        if res1 + res2 == 2:
            return {
                    'msg' : '{} is removed'.format(self.infile),
                    }

        else:

            return {
                    'msg' : 'error removing {}'.format(self.infile),
                    }

    def unlink(self, f):

        if os.path.isfile(f):
            os.unlink(f)
            if not os.path.isfile(f):
                logging.info("removed %s", f)
                return True


        return False

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    r = RemoveFile(sys.argv[1])
    msg = r.remove_file()
    logging.info(msg)
