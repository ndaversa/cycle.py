cycle.py
========
A simple python script to power cycle a WeMo switch when no internet connection is detected.

Background
==========
* [Some light reading on launchd](http://nathangrigg.net/2012/07/schedule-jobs-using-launchd/)
* [Excellent WeMo hack that makes this so simple](https://github.com/issackelly/wemo)

Usage
=====
* Read the `bin/configure` script first before executing so you understand
  what it does.

* Modify `com.ndaversa.cycle.py.plist` as to replace instances
  `/Users/ndaversa/...` with an appropriate location based on your username.

* Run the `bin/configure` script
