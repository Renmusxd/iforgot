import sys
from . import iforgot


def main():
    args = sys.argv[1:]
    if len(args)>0:
        iforgot.check(args)
    else:
        print "usage: iforgot <prompt>"
        print "example:"
        print ">>iforgot how to change my MAC address to aa:bb:cc:dd"
        print "Possible matches:"
        print "spoof set aa:bb:cc:dd <on>"