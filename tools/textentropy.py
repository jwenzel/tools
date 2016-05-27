#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import argparse
import urllib2
import httplib
from math import log

UPPER_CASE_RANGE = range(0x41, 0x5b) # a-z = [0x61-0x7a]
LOWER_CASE_RANGE = range(0x61, 0x7b) # A-Z = [0x41-0x5a]
CHAR_RANGE = list(LOWER_CASE_RANGE) + list(UPPER_CASE_RANGE)

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

    usage_str = "Usage: " + sys.argv[0] + "-m=<mode> -f=<file> -i=<ID of file>"
    error(usage_str)
    print('\n')
    print("-------------------------------------------------------------------")
    print("mode   - [file, gb]: file (reading text file from a given path;")
    print("                     gb   (read text file from Gutenberg project)")
    print("file   - path to a file containing the text")
    print("ID     - ID of a Gutenberg file")
    print("-------------------------------------------------------------------")
    exit(1)
#}}}

#{{{ is website available
def is_website_available(url):
    """
    Checks whether a given url is available
    """
    try:
        urllib2.urlopen(url)
    except urllib2.HTTPError, e:
        print(e.code)
    except urllib2.URLError, e:
        print(e.args)
#}}}

#{{{ read file from Gutenberg
def read_gutenberg_file(id):
    """
    Takes an ID of an eBook archived by www.gutenberg.com and downloads the
    corresponding book (.txt file).
    """
    url = 'http://www.gutenberg.org/files/' + str(id) + '/' + str(id) + '-0.txt'

    text = ""

    if is_website_available(url):
        text = urllib2.urlopen(url).read()
    else:
        url  = 'http://www.gutenberg.org/cache/epub/' + str(id) + '/pg' + str(id) + '.txt'
        if is_website_available(url):
            text = urllib2.urlopen(url).read()
        else:
            print("website not available; stop the program")
            sys.exit(1)

    if "<head>" in text:
        print("--------------------------------------------------")
        print("File request was not accepted by www.gutenberg.org")
        print("--------------------------------------------------")
        sys.exit(1)

    return text
##}}}

##{{{ read file
def read_file(f):
    """
    reads the content of a given file f and returns its content
    """
    return f.read()
##}}}

##{{{ get word list from text
def get_word_list(text):
    word_list = text.split(' ')

    return word_list
##}}}

##{{{ get initials from word list
def get_initials(word_list):

    initials = []

    for word in word_list:
        if (word != "") and (ord(word[0]) in CHAR_RANGE):
            initials.append(word[0])

    return initials
##}}}

##{{{ count occurrence of initials
def count_initials(initials):

    count_list = dict.fromkeys([chr(i) for i in CHAR_RANGE], 0)

    for char in initials:
        count_list[char] += 1

    return count_list
##}}}

##{{{ compute entropy of given initials count list
def compute_entropy(count_list):
    """
    Gets a list of initials with their corresponding number of occurrences in a
    text and computes the min as well as the Shannon entropy
    """
    total_num_initials = float(sum(count_list.values()))

    max_probability = max(count_list.values())/total_num_initials

    min_entropy = -log(max_probability, 2)

    shannon_entropy = 0.0

    for val in count_list:
        curr_prob = float(count_list[val])/total_num_initials
        if curr_prob > 0:
            shannon_entropy += curr_prob * -log(curr_prob, 2)

    return (shannon_entropy, min_entropy)
##}}}

##{{{ print count list
def print_count_list(count_list):
    print(count_list)
##}}}

##{{{ print entropy
def print_entropy(shannon_entropy, min_entropy):
    digits = 3
    print("------------------------------------------------")
    print("Shannon Entropy: {0} bit/char".format(round(shannon_entropy,digits)))
    print("Min Entropy:     {0} bit/char".format(round(min_entropy,digits)))
    print("------------------------------------------------")
##}}}

##{{{ sanitize_inputs
def sanitize_inputs(args):
    if args.mode == "file" and not args.file:
        error_str = "Missing input parameter, -f"
        usage(error_str)

    if args.mode == "gb" and not args.ID:
        error_str = "Missing input parameter, -i"
        usage(error_str)

    if args.ID and args.ID < 1:
        error_str = "ID must be a positive Integer value"
        usage(error_str)

    file_content = ""

    if args.file:
        try:
            f = open(args.file)
            file_content = read_file(f)
        except:
            error_str = "File '" + args.file + "' not found"
            usage(error_str)

    return (args.mode, args.ID, file_content)
##}}}

##{{{ add parser arguments
def add_parser_arguments(parser):
    parser.add_argument("-m", "--mode",help = "specifies the mode for the \
            program: file (takes a text file) or ID (takes an ID of a Gutenberg\
            document)", type = str, choices = ["file", "gb"], required = True)
    parser.add_argument("-f", "--file", help="specifies the path to the input\
            file", type=str, required=False)
    parser.add_argument("-i", "--ID", help="specifies the ID of a Gutenberg\
            file", type=int, required=False)

    return parser.parse_args()
##}}}

# {{{ main
def main():
    parser = argparse.ArgumentParser(prog="Computing entropy of initials")

    args = add_parser_arguments(parser)

    (mode, file_id, file_content) = sanitize_inputs(args)

    if mode == "file":
        word_list = get_word_list(file_content)
        initials = get_initials(word_list)
        count_list = count_initials(initials)

    if mode == "gb":
        file_content = read_gutenberg_file(file_id)
        word_list = get_word_list(file_content)
        initials = get_initials(word_list)
        count_list = count_initials(initials)

    print_count_list(count_list)
    print
    (shannon_entropy, min_entropy) = compute_entropy(count_list)
    print_entropy(shannon_entropy, min_entropy)
# }}}

if __name__ == '__main__':
    main()
