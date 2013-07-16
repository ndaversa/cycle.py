#!/usr/bin/env python
import sys
import urllib2
import time
import datetime

def connected():
    try:
        # IP below is a google.ca server, using IP to avoid DNS lookup
        response = urllib2.urlopen('http://74.125.226.120',timeout=2)
        return True
    except urllib2.URLError as err: pass
    return False

timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

if not connected():
    print timestamp, "No internet connected detected :("

    from vendor.wemo import get, on, off
    powered = get()

    if powered:
        print "Turning WeMo off"
        off()
    else:
        print "Turning WeMo on"
        on()
else:
    print timestamp, "Internet connection detected :)"

sys.exit(0)
