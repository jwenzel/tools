#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__  = 'Jakob Wenzel'
__email__   = 'jakob.wenzel at uni-weimar dot de'
__date__    = '2016-04-18'
__version__ = 1.0

import sys

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
    usage_str = "Usage: " + sys.argv[0] + " <mode> <file> <key>"
    error(usage_str)
    print
    print("-----------------------------------------------------------------------------")
    print("mode(e,c) - encrypt a file (e) or show keys/plaintexts for a ciphertext(c)")
    print("file      - contains the plaintext")
    print("key       - key for the CAESAR cipher")
    print("-----------------------------------------------------------------------------")
    exit(1)
##}}}

##{{{ read file
def read_file(f):
    """
    reads the content of a given file f and returns an all lower-case string
    containing all symbols found in alphabet
    """
    content = f.read()
    content = content.replace('\n','').lower()

    output = ""

    # clean string (remove extra symbols, white space, ...)
    for c in content:
        if c not in alphabet:
            continue
        else:
            output += c

    return output
##}}}

##{{{ caesar encrypt
def caesar_encrypt(p,k):
    """
    gets a plaintext p (string) and a key k (numeric) as input and encrypts p
    using the CAESAR cipher with the key K
    """
    ciphertext = ""

    for c in p:
        c_pos       = alphabet.index(c)
        new_char    = alphabet[(c_pos + k) % 26] 
        ciphertext += new_char

    return ciphertext
##}}}

##{{{ caesar decrypt
def caesar_decrypt(c,k):
    """
    gets a ciphertext c (string) and a key k (numeric) as input and decrypts c
    using the CAESAR cipher with the key K
    """
    plaintext = ""

    for ch in c:
        c_pos      = alphabet.index(ch)
        new_char   = alphabet[(c_pos - k) % 26] 
        plaintext += new_char

    return plaintext
##}}}

##{{{ print
def print_format(add_info, c):
    output     = ""
    chunk_size = 5
    ctr = 0

    for ch in c:
        ctr += 1
        output += ch
        if ctr % chunk_size == 0:
            output += ' '

    print(add_info + output);
##}}}
        
##{{{ check crypto_grams
def show_possible_plaintexts(c):
    plaintext = ""
    # k = 26 is equal to k = 0 and thus, neglected
    for k in range(1,26):
        plaintext = caesar_decrypt(c,k)
        tmp_str = "Key = " + str(k) + ": Plaintext = "
        print_format(tmp_str, plaintext)
##}}}

##{{{ main
def main():
    # check number of arguments
    if (len(sys.argv) != 3) and (len(sys.argv) != 4):
        usage("")

    # first check which mode is chosen
    # if e: all arguments are required
    # if c: no key is required (but may be given)
    # check if mode is character and valid
    if sys.argv[1].isalpha() and (sys.argv[1] == 'e' or sys.argv[1] == 'c'):
        mode = sys.argv[1]
    else:
        error_str = "Argument '" + sys.argv[1] + "' is not a valid mode"
        usage(error_str)

    if mode == 'e':
        if len(sys.argv) != 4:
            usage("")
        if not unicode(sys.argv[3], 'utf-8').isnumeric() or int(sys.argv[3]) < 0:
            error_str = "Argument '" + sys.argv[3] + "' is not valid"
            usage(error_str)
    elif mode == 'c':
        if len(sys.argv) != 4 and len(sys.argv) != 3:
            usage("")

    # check if file exists
    try:
        f = open(sys.argv[2])
    except:
        error_str = "File '" + sys.argv[2] + "' not found"
        usage(error_str)

    # check type of key (numeric type and positive)

    if mode == 'e':
        key = int(sys.argv[3])
        plaintext  = read_file(f)
        ciphertext = caesar_encrypt(plaintext, key)
        print_format("Ciphertext: ", ciphertext)
    else:
        ciphertext = read_file(f)
        show_possible_plaintexts(ciphertext)
##}}}

if __name__ == '__main__':
    main()
