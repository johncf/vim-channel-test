import logging
import json

class VimX:

    def __init__(self, ch_in, ch_out):
        self.ch_in = ch_in
        self.ch_out = ch_out
        self.counter = -1
        self.buffer = [] # buffer for 'positive' objects
        self.logger = logging.getLogger(__name__)

    def recv(self, expect=0):
        """ Blocking function. Use with care!
            `expect` should either be 0 or a negative number. If `expect == 0`, any positive
            indexed object is returned. Otherwise, it will queue any positive objects until the
            first negative object is received. If the received negative object does not match
            `expect`, then a ValueError is raised.
        """
        if expect > 0:
            raise AssertionError('expect <= 0')
        if expect == 0 and len(self.buffer) > 0:
            return self.pop()
        while True:
            s = self.ch_in.readline()
            self.logger.info("read: %s", s)
            ind, obj = json.loads(s)
            if (expect == 0 and ind < 0) or (expect < 0 and expect != ind):
                raise ValueError('Incorrect index received! {} != {}', expect, ind)
            elif expect < 0 and ind > 0:
                self.buffer.insert(0, obj)
            else:
                break
        return obj

    def write(self, obj):
        s = json.dumps(obj)
        print(s, file=self.ch_out) # line break
        self.ch_out.flush()
        self.logger.info("write: %s", s)

    def send(self, obj):
        self.write([0, obj])

    def call(self, fname, *args, reply=True):
        obj = ['call', fname, args]
        if reply:
            obj += [self.counter]
            self.counter -= 1
        self.write(obj)
        if reply:
            re = self.recv(expect=self.counter)
            return re

    def eval(self, expr, reply=True):
        obj = ['expr', expr]
        if reply:
            obj += [self.counter]
            self.counter -= 1
        self.write(obj)
        if reply:
            re = self.recv(expect=self.counter)
            return re

    def command(self, cmd):
        obj = ['ex', expr]
        self.write(obj)

    def echox(self, msg, level=1):
        """ Execute echom in vim using appropriate highlighting. """
        level_map = ['None', 'WarningMsg', 'ErrorMsg']
        msg = msg.strip().replace('"', '\\"').replace('\n', '\\n')
        self.command('echohl {} | echom "{}" | echohl None'.format(level_map[level], msg))

    def buffer_add(self, name):
        """ Create a buffer (if it doesn't exist) and return its number. """
        bufnr = self.call('bufnr', name, 1)
        self.call('setbufvar', bufnr, '&bl', 1, reply=False)
        return bufnr

    def abspath(self, relpath):
        vim_cwd = self.call("getcwd")
        return path.join(vim_cwd, relpath)
