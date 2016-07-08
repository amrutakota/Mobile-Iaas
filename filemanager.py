#! /usr/bin/python

import sys

from fileops import FileManager

args=[arg for arg in sys.argv]

test=FileManager()
test.filename=args[1]
test.k=int(args[2])
test.n=int(args[3])

test.init()
test.encode()
test.authenticate()
test.send()
wait=raw_input()
test.recv()
test.decode()
