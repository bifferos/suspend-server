Intro
=====

This service suspends the system when it receives a UDP packet
with the text 'suspend' in it.  There is no security.


Installation
============

You need dbus libs for linux mint, if you don't have them:

$ sudo apt install python3-dbus

To install and start the service:

$ make install


Testing
=======

Start the server from the source directory for local development with

$ make run

Then in another terminal basic test of the server with:

$ ./test.py

