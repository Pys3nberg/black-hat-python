import sys, socket, optparse, threading, subprocess


# define some global variables
listen = False
command = False
upload = False
execute = ""
target = ""
upload_destination = ""
port = 0

# Create Option parser and add all of teh require options

parser = optparse.OptionParser()

parser.add_option('-l','--listen', action='store_true', dest="listen")

(options, args) = parser.parse_args()

if options.listen:
    print(options.listen)