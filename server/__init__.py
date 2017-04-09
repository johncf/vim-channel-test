from __future__ import (absolute_import, division, print_function)

import logging
from multiprocessing import Queue
from select import select

__metaclass__ = type  # pylint: disable=invalid-name


class Middleman():

    def __init__(self, vimx):
        self.vimx = vimx
        self.queue = Queue(maxsize=2)
        self.logger = logging.getLogger(__name__)

    def safe_exec(self, fn):
        """ fn should take a VimX object as the only argument. """
        self.queue.put(['exec', fn])

    def loop(self):
        x = 1
        while True:
            ready, _, _ = select([self.vimx.ch_in, self.queue._reader], [], [], 2)
            for ev in ready:
                if ev == self.queue._reader:
                    req = self.queue.get()
                    if req[0] == 'exec':
                        fn = req[1]
                        fn(self.vimx)
                    elif req[0] == 'exit':
                        break
                elif ev == self.vimx.ch_in:
                    vi = self.vimx.wait()
                    self.logger.info("got: %s", vi)
            self.vimx.send('hello {}'.format(x))
            x += 1
