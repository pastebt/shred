#! /usr/bin/env python

import os
import sys
from getopt import gnu_getopt, GetoptError


class SRC(object):
    def __init__(self, s=1024):
        self.s = 1024

    def __len__(self):
        return self.s

    def __call__(self, sz=None):
        self.gen(sz if sz else self.s)

    def gen(self, size):
        pass


class RAND(SRC):
    def gen(self, size):
        return "a" * size


class ZERO(SRC):
    def gen(self, size):
        return "0" * size


def do_one(fn, src, verbose):
    with open(fn, "r+b") as fout:
        fout.seek(0, os.SEEK_END)
        sz = fout.tell()
        fout.seek(0, os.SEEK_SET)
        while sz > len(src):
            fout.write(src())
        if sz:
            fout.write(src(sz))


def run(fn, unlink, set_zero, verbose):
    for i in range(4):
        do_one(fn, RAND(), verbose)
    if set_zero:
        do_one(fn, ZERO(), verbose)
    if unlink:
        os.unlink(fn)


def usage():
    print("Usage: " + sys.argv[0] + " [-v|-u|-z] filename")
    sys.exit(1)


def main():
    try:
        opts, args = gnu_getopt(sys.argv[1:], "vuz")
    except GetoptError as ge:
        print(ge)
        usage()
    if len(args) != 1:
        usage()
    om = dict(opts)
    run(args[0], "-u" in om, "-z" in om, "-v" in om)


if __name__ == '__main__':
    main()
