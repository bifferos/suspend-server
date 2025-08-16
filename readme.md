Intro
=====

This service suspends the system when it receives a UDP packet
with the text 'suspend' in it.  There is no security.

The service also responds to a 'ping' packet which gives an 
indication of whether the host is up.

dbus is used to establish when the network is up again
after suspend.  This is to allow transmission of a response
packet to the suspend request.  The response packet is sent
on wake, potentially hours or days after suspend.  Its
purpose is to allow fast determination of when the host is
up, however this mechanism should be backed up by ping
polling, and could be considered redundant if speed isn't
critical.


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

$ make test

This will only test the 'ping' on the server.  To test out suspend/wake
use:

suspend_me.py
wake_me.sh

However these scripts are best run remotely, from another machine!

Troubleshooting
===============

All my work first time, however...
Systemd can find many ways to avoid suspending your system, tasks need to 
be run prior to suspend and they can end up hanging.  If you want a trouble
free suspend it may be worth disabling hooks

make a backup dir (once)
$ sudo mkdir -p /usr/lib/systemd/system-sleep.disabled

move both hooks out
$ sudo mv /usr/lib/systemd/system-sleep/hdparm /usr/lib/systemd/system-sleep.disabled/
$ sudo mv /usr/lib/systemd/system-sleep/nvidia /usr/lib/systemd/system-sleep.disabled/

Reboot after doing this if the system is hung.  nvidia sleep operations are not 
really needed if your system is headless, and the hdparm shouldn't be needed for 
suspend as the disks should spin down after some idle time.

$ systemctl list-jobs

Will tell you if a suspend job has hung.  You will need to investigate why.
