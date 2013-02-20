#!/usr/local/bin/python
import sys
import pyinotify
from subprocess import call
import signal as sig
from os import getcwd




# print usage info if args are wrong
if ( len(sys.argv) != 3 ) :
	print("USAGE: ./autorsync LOCAL_DIRECTORY REMOTE_DIRECTORY\nEXAMPLE: ./autorsync . upload_dir")
	sys.exit(0)

# handle relative paths, because apparently daemonized pyinotify thinks the cwd is / by default
if ( sys.argv[1][0] != '/' ):
	sys.argv[1] = getcwd()+"/"+sys.argv[1]

# too lazy to write tilde expansion, so it just prints a warning if you try to use it
# this is totally half-assed
if ( sys.argv[1][0] == '~'):
	print("Tilde shorthand is not implemented. Exiting...")
	sys.exit(0)

# actually call rsync when an event is called
def on_loop(notifier):
	call(["rsync","-avh","--delete",sys.argv[1],"miranda.theknown.net:~/"+sys.argv[2]])

# handle sigterm so that the program shuts down gracefully when killed
def handle_sigTERM():
	sys.stdout.write("SIGTERM caught! Exiting...\n")
	notifier.stop()
	sys.exit(0)

# register the SIGTERM handler
sig.signal(sig.SIGTERM, handle_sigTERM)

# set up the pyinotify stuff
wm = pyinotify.WatchManager()
notifier = pyinotify.Notifier(wm)

# this only watches the current directory.
# TODO: make this watch child directories also
wm.add_watch(sys.argv[1], pyinotify.IN_CREATE | pyinotify.IN_DELETE | pyinotify.IN_MODIFY, rec=True, auto_add=True)


# run pyinotify's notify loop, daemonized.
# note that rsync breaks the stdout redirection for some reason, could debug it if I never need it
try:
    notifier.loop(daemonize=True, callback=on_loop,
                  pid_file='/tmp/autorsync.pid', stdout='/tmp/autorsync.txt')
except pyinotify.NotifierError, err:
    print >> sys.stderr, err
