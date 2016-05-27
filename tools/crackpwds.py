#!/usr/bin/python3
# -*- coding: utf-8 -*-

from __future__ import with_statement
import sys
import argparse
import hashlib
import time
import threading

hash_counter = 0
LOWER_CASE_RANGE = range(0x61, 0x7b) # A-Z = [0x41-0x5a]

#{{{ error and usage
def error(message):
    """ Prints error message."""
    sys.stderr.write(message)


def usage(message):
    """ Prints message and quits the program."""

    if message:
        print("---------------------------------------------------------------")
        error(message + '\n')
        print("---------------------------------------------------------------")

    usage_str = "Usage: " + sys.argv[0] + "-f=<file>"
    error(usage_str)
    print('\n')
    print("-------------------------------------------------------------------")
    print("file   - path to a file containing the hashes (one per line)")
    print("-------------------------------------------------------------------")
    exit(1)
#}}}

##{{{ read file
def read_file(f):
    """
    reads the content of a given file f and returns its content as an array (one
    entry reflects one line)
    """
    return f.read().split('\n')
##}}}

###{{{ get next password candidate
#def get_next_pw(charset, size):
#    charset[0] = chr(ord(charset[0])+1)
#    if size == 1:
#        return charset
#    if ord(charset[0]) > ord('z'):
#        charset[0] = 'a'
#        charset[1] = chr(ord(charset[1])+1)
#        if size == 2:
#            return charset
#        if ord(charset[1]) > ord('z'):
#            charset[1] = 'a'
#            charset[2] = chr(ord(charset[2])+1)
#            if size == 3:
#                return charset
#            if ord(charset[2]) > ord('z'):
#                charset[2] = 'a'
#                charset[3] = chr(ord(charset[3])+1)
#                if size == 4:
#                    return charset
#                if ord(charset[3]) > ord('z'):
#                    charset[3] = 'a'
#                    charset[4] = chr(ord(charset[4])+1)
#                    if size == 5:
#                        return charset
#                    if ord(charset[4]) > ord('z'):
#                        charset[4] = 'a'
#                        charset[5] = chr(ord(charset[5])+1)
#    return charset
###}}}

##{{{ get next password candidate (generic)
def get_next_pw(m, i, num_chars, char):
    for j in reversed(range(num_chars)):
        rest = i % char
        i = i / char
        m[j] = chr(LOWER_CASE_RANGE[rest])

    return m
##}}}

##{{{ class thread_crack_pw
class thread_crack_pw(threading.Thread):
    def __init__(self, name, min_size, size, hashes, num_of_hashes, full_size):
        threading.Thread.__init__(self)
        self.name = name
        self.min_size = min_size
        self.size = size
        self.hashes = hashes
        self.num_of_hashes = num_of_hashes
        self.full_size = full_size

    def crack(self, curr):
        global hash_counter

        for i in range(0, pow(26, self.size)):
            curr = get_next_pw(curr, i, self.size, len(LOWER_CASE_RANGE))
            s = ''.join(curr)
            h2 = hashlib.sha1(s).hexdigest()
            if h2 in self.hashes:
                # maybe it is required to lock hash_counter
                hash_counter += 1
                print("Passwort: " + s)
                print("Hashwert: " + h2)
            if hash_counter == self.num_of_hashes:
                break

    def run(self):
        print("Starting Thread {0}\n".format(self.name))

        if not self.full_size:
            for i in range(self.min_size, self.size):
                curr = ['' for i in range(self.size)]
                self.crack(curr)
        else:
            curr = ['' for i in range(self.size)]
            self.crack(curr)
       
        print("Thread {0} terminated\n".format(self.name))
##}}}

##{{{ crack passwords
def pw_crack(hashes, current, min_size, max_size):
    """
    Gets an arbitrary number of hashes and checks all possible passwords of size
    min_size to max_size (characters) until all pairs (password, hash) are found
    or all possible passwords are tested
    """
    num_of_hashes = len(hashes) - 1

    threads = []
    thread_not_full_size = thread_crack_pw(
            "Thread 1",
            min_size,
            max_size - 1,
            hashes,
            num_of_hashes,
            False)
    thread_not_full_size.start()
    threads.append(thread_not_full_size)

    thread_full_size = thread_crack_pw(
            "Thread 2",
            min_size,
            max_size,
            hashes,
            num_of_hashes,
            True)
    thread_full_size.start()
    threads.append(thread_full_size)

    for thread in threads:
        thread.join()

##}}}

##{{{ sanitize_inputs
def sanitize_inputs(args):
    file_content = ""

    if args.file:
        try:
            f = open(args.file)
            file_content = read_file(f)
        except:
            error_str = "File '" + args.file + "' not found"
            usage(error_str)

    if args.min < 1:
        error_str = "Minimum password length must be a positive number"
        usage(error_str)

    if args.max < args.min:
        error_str = "Maximum password length must be at least equal to the\
                minimum password length"
        usage(error_str)

    return(file_content, args.min, args.max)
##}}}

##{{{ add parser arguments
def add_parser_arguments(parser):
    parser.add_argument("-f", "--file", help="specifies the path to the input\
            file", type=str, required=True)
    parser.add_argument("-min", help="minimum password size", type=int,
            required=True)
    parser.add_argument("-max", help="maximum password size", type=int,
            required=True)

    return parser.parse_args()
##}}}

# {{{ main
def main():
    parser = argparse.ArgumentParser(prog="Computing entropy of initials")

    args = add_parser_arguments(parser)

    (file_content, pw_size_min, pw_size_max) = sanitize_inputs(args)

    digits = 3
    start = time.clock()
    print(file_content)
    #pw_crack(file_content, [], 1, len(file_content))
    pw_crack(file_content, [], pw_size_min, pw_size_max)
    end = time.clock()
    print("required time: {0} ms".format(round(end - start,digits)))

# }}}

#    print(hashlib.sha1("prince").hexdigest())
#    print(hashlib.sha1("cicero").hexdigest())
#    print(hashlib.sha1("sirken").hexdigest())
#    print(hashlib.sha1("lustig").hexdigest())
#    print(hashlib.sha1("alanr").hexdigest())
#    print(hashlib.sha1("dbowie").hexdigest())

if __name__ == '__main__':
    main()
