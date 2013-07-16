#!/usr/bin/env python
import sys
import urllib2

def connected():
    try:
        # IP below is a google.ca server, using IP to avoid DNS lookup
        response = urllib2.urlopen('http://74.125.226.120',timeout=2)
        return True
    except urllib2.URLError as err: pass
    return False


if not connected():
    import time
    import datetime
    from vendor.wemo import get, on, off

    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    print timestamp, "No internet connected detected :("

    powered = get()
    if powered:
        print timestamp, "Turning WeMo off"
        off()
    else:
        print timestamp, "Turning WeMo on"
        on()

sys.exit(0)
