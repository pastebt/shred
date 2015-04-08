#! /usr/bin/env python

import os
import sys
import random
from getopt import gnu_getopt, GetoptError


def RAND(size):
    dat = 'abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    return (random.choice(dat) * size).encode("utf8")


def ZERO(size):
    #return ("0" * size).encode("utf8")
    return bytearray(size)


def do_one(fn, src, verbose):
    bsize = 102400
    with open(fn, "r+b") as fout:
        fout.seek(0, os.SEEK_END)
        size = left = fout.tell()
        fout.seek(0, os.SEEK_SET)
        while left >= bsize:
            fout.write(src(bsize))
            fout.flush()
            left = left - bsize
            if verbose:
                sys.stdout.write("%02.2f%%\r" % ((size - left) * 100.0 / size))
        if left:
            fout.write(src(left))
        if verbose:
            print("100.0% ")


def delete(fn, verbose):
    dn = os.path.dirname(fn)
    nl = len(os.path.basename(fn))
    on = fn
    while nl > 0:
        nn = os.path.join(dn, "0" * nl)
        if verbose:
            print("rename %s to %s" % (on, nn))
        os.rename(on, nn)
        on = nn
        nl = nl - 1
    if verbose:
        print("Remove file " + nn)
    os.unlink(nn)

def run(fn, num, unlink, set_zero, verbose):
    if not os.path.exists(fn):
        sys.stderr.write("Error! can not find file " + fn + "\n")
        sys.exit(1)
    print("\nshred file " + fn)
    for i in range(num):
        if verbose:
            print("Overwrite time %d:" % (i + 1))
        do_one(fn, RAND, verbose)

    if set_zero:
        if verbose:
            print("Overwrite with zero")
        do_one(fn, ZERO, verbose)

    if unlink:
        delete(fn, verbose)


def usage():
    print("Usage: " + sys.argv[0] + " [-v|-u|-z] [-n N] filename")
    print("     -n N overwrite N times instead of the default (3)")
    print("     -u   truncate and remove file after overwriting")
    print("     -v   show progress")
    print("     -z   add a final overwrite with zeros to hide shredding")
    sys.exit(1)


def main():
    try:
        opts, args = gnu_getopt(sys.argv[1:], "vuzn:")
    except GetoptError as ge:
        print(ge)
        usage()
    if len(args) < 1:
        usage()
    om = dict(opts)
    for fn in args:
        run(fn, int(om.get("-n", 3)), "-u" in om, "-z" in om, "-v" in om)


if __name__ == '__main__':
    main()
