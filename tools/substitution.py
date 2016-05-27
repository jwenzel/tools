#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__  = 'Jakob Wenzel'
__email__   = 'jakob.wenzel at uni-weimar dot de'
__date__    = '2016-04-19'
__version__ = 1.0

import sys
import re
import argparse

alphabet = "abcdefghijklmnopqrstuvwxyz"

##{{{ error and usage
def error(message):
    """ Prints error message."""
    sys.stderr.write(message)

def usage(message):
    """ Prints message and quits the program."""

    if message:
        print("---------------------------------------------------")
        error(message)
        print
        print("---------------------------------------------------")

    print
    usage_str = "Usage: " + sys.argv[0] + " <mode> <file>"
    error(usage_str)
    print
    print("-----------------------------------------------------------------------------")
    print("possible modes [encrypt, decrypt, analyze, replace]")
    print("encrypt   - encrypt a given text in a file and print the ciphertext")
    print("decrypt   - decrypt a given text in a file and print the plaintext")
    print("analyze   - print character frequency")
    print("replace   - replace individual characters")
    print("pattern   - searches for a given string pattern")
    print("file      - contains the plaintext")
    print("-----------------------------------------------------------------------------")
    exit(1)
##}}}

##{{{ read file
def read_file_lower_case(f):
    """
    reads the content of a given file f and returns an all lower-case string
    containing all symbols found in alphabet
    """
    content = f.read()
#    content = content.replace('\n',' ').lower()
    content = content.lower()

    output = ""

    # clean string (remove extra symbols, white space, ...)
    for c in content:
        if c == ' ' or c in alphabet:
            output += c

    return output
##}}}

##{{{ frequency of characters
def get_frequency_of_characters(s):
    """
    return how often each character from 'a'..'z' occurs in the string s
    """
    frequencies = {}

    for c in alphabet:
        frequencies[c] = s.count(c)

    return frequencies
##}}}

##{{{ return string pattern as array
def get_pattern(p):
    pattern = dict()
    pattern_out = []

    for c in p:
        pattern[c] = [m.start() for m in re.finditer(c, p)]
        pattern_out.append(pattern[c]);
    return pattern_out
##}}}

##{{{ check for string pattern
def find_pattern(p,s):
    """
    searches for a string pattern p in a string s and returns the corresponding
    part(s) of the string
    """
    output = ""

    len_p = len(p)
    len_s = len(s)

    # get the pattern for each character in p
    pattern = get_pattern(p)

    # get all substrings of length of p
    sub_strings = [s[i:i+len_p] for i in xrange(len_s-len_p)]

    for i in xrange(len(sub_strings)):
        pattern_compare = get_pattern(sub_strings[i])
        if pattern_compare == pattern:
            output = sub_strings[i]

    return output
##}}}

##{{{ encrypt
def encrypt(p,key):
    ciphertext = ""

    idx = 0

    for c in p:
        if c in alphabet:
            idx = alphabet.index(c)
            ciphertext += key[idx]
        elif c == ' ':
            ciphertext += c

    return ciphertext
##}}}

##{{{ decrypt
def decrypt(c,key):
    plaintext = ""

    idx = 0

    for ch in c:
        if ch in alphabet:
            idx = key.index(ch)
            plaintext += alphabet[idx]
        elif ch == ' ':
            plaintext += ch

    return plaintext
##}}}

#{{{ replace
def replace(ciphertext, args_dict):
    """
    given a ciphertext and a dictionary of characters, this functions replaced
    all occurrences of key in the ciphertexts with the corresponding values from
    the dictionary values
    """
    result = ''

    for c in ciphertext:
      if c == ' ':
        result += c
      elif (c in args_dict) and (args_dict[c] != None):
        result += args_dict[c]
      else:
        result += '.'

    return result
##}}}

##{{{ main
def main():
    parser = argparse.ArgumentParser(prog="Substitution Cipher Support Program")
    parser.add_argument("--mode",help = "specifies the mode for the \
            program:", type = str, choices = ["encrypt", "decrypt", "analyze",\
            "replace", "pattern"], required = True)
    parser.add_argument("--input", help = "specifies the input file",\
            type = str, required = True)
    parser.add_argument("--key", help = "key for the substitution cipher",\
            required = False, type = str, default = alphabet)
    parser.add_argument("--pattern", help = "string pattern to search for",\
            required = False, type = str)

    # add all possible characters to replace as arguments
    for c in alphabet:
        parser.add_argument("--" + c, default = None)

    args = parser.parse_args()

    mode    = args.mode
    fname   = args.input
    key     = args.key
    pattern = args.pattern
    
    if len(key) != 26:
        error_str = "key must consist of 26 characters"
        usage(error_str)
    elif not isinstance(key, str):
        error_str = "key must be of type string (str)"
        usage(error_str)

    try:
        f = open(fname)
        content = read_file_lower_case(f)
    except:
        error_str = "File '" + fname + "' not found"
        usage(error_str)

    c = ""
    p = ""

    if mode == "encrypt":
        c = encrypt(content, key)
        print(c)
    elif mode == "decrypt":
        p = decrypt(c, key)
        print(p)
    elif mode == "analyze":
        print(get_frequency_of_characters(content))
    elif mode == "replace":
        print(content)
        replaced_content = replace(content, args.__dict__)
        print(replaced_content)
    elif mode == "pattern":
        content = content.replace(' ','')
        pattern_out = find_pattern(pattern, content)
        print(pattern_out)
    else:
        usage("")
##}}}

    if __name__ == '__main__':
        main()
