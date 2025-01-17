import sys

from python1.libraries.sayings import hello

if len(sys.argv) == 2:
    hello(sys.argv[1])