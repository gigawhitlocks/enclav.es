#!/usr/local/bin/python

import sys
import pyinotify
from subprocess import call
import signal as sig
from os import getcwd


if ( len(sys.argv) != 3 ) :
	print("USAGE: ./autorsync LOCAL_DIRECTORY REMOTE_DIRECTORY")
	sys.exit(0)

if ( sys.argv[1][0] != '/' ):
	sys.argv[1] = getcwd()+"/"+sys.argv[1]

if ( sys.argv[1][0] == '~'):
	print("Tilde shorthand is not implemented. Exiting...")
	sys.exit(0)

def on_loop(notifier):
	call(["rsync","-davh",sys.argv[1],"miranda.theknown.net:~/"+sys.argv[2]])

def handle_sigTERM():
	sys.stdout.write("SIGTERM caught! Exiting...\n")
	notifier.stop()
	sys.exit(0)

sig.signal(sig.SIGTERM, handle_sigTERM)
wm = pyinotify.WatchManager()
notifier = pyinotify.Notifier(wm)
wm.add_watch(sys.argv[1], pyinotify.IN_CREATE | pyinotify.IN_DELETE | pyinotify.IN_MODIFY)

# Notifier instance spawns a new process when daemonize is set to True. This
# child process' PID is written to /tmp/pyinotify.pid (it also automatically
# deletes it when it exits normally). If no custom pid_file is provided it
# would write it more traditionally under /var/run/. Note that in both cases
# the caller must ensure the pid file doesn't exist when this method is called
# othewise it will raise an exception. /tmp/stdout.txt is used as stdout 
# stream thus traces of events will be written in it. callback is the above 
# function and will be called after each event loop.
try:
    notifier.loop(daemonize=True, callback=on_loop,
                  pid_file='/tmp/autorsync.pid', stdout='/tmp/autorsync.txt')
except pyinotify.NotifierError, err:
    print >> sys.stderr, err
