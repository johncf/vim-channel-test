import logging
from server.vimx import VimX
from server import Middleman
import sys

def main():
    print('hello from the other side', file=sys.stderr)
    ch_in = sys.stdin
    ch_out = sys.stdout
    vimx = VimX(ch_in, ch_out)

    Middleman(vimx).loop()

if __name__ == '__main__':
    handler = logging.FileHandler('chtest.log', 'w')
    handler.formatter = logging.Formatter(
        '%(asctime)s [%(levelname)s @ '
        '%(filename)s:%(funcName)s:%(lineno)s] - %(message)s')
    logging.root.addHandler(handler)
    logging.root.setLevel(logging.DEBUG)
    main()
