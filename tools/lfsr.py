#!/usr/bin/python3
# -*- coding: utf-8 -*-

""" lsfr.py

    Helper program for building and using an LFSR.
"""

import sys
import argparse

# {{{ error and usage
def error(message):
    """ Prints error message."""
    sys.stderr.write(message)


def usage(message):
    """ Prints message and quits the program."""

    if message:
        print("---------------------------------------------------------------")
        error(message + '\n')
        print("---------------------------------------------------------------")

    usage_str = "Usage: " + sys.argv[
        0] + "\n -m=<mode>\n -pol=<polynom>\n -i=<initial state>\n -n=<output length>\n -p=<plaintext>\n -c=<ciphertext>\n -kl=<keystream length>\n -ks=<keystream start>"
    error(usage_str)
    print('\n')
    print("-------------------------------------------------------------------")
    print("mode             - [encrypt, decrypt, keystream]")
    print("polynom          - feedback polynom of the LSFR")
    print("initial state    - starting configuration of the LFSR")
    print("output length    - number of output bits generated")
    print("plaintext        - plaintext to be encrypted")
    print("ciphertext       - ciphertext to be decrypted")
    print("keystream length - length of the keystream")
    print("keystream start  - position of the first bit of the keystream")
    print("-------------------------------------------------------------------")
    exit(1)
# }}}

# {{{ update state
def update_state(state, curr):
    """ Updates the internal state of the LFSR """
    for i in range(0, len(state) - 1):
        state[i] = state[i + 1]

    state[len(state) - 1] = curr

    return state
# }}}

# {{{ generate_keystream
def generate_keystream(state, pol, n, k, ks):
    """
    Gets an initial state and a feedback polynom and computes the n outputs of
    the LFSR (n bits of keystream from ks to ks + k]
    """
    output = []
    curr = 0

    for i in range(0, n):
        for j in range(0, len(state)):
            curr ^= (pol[j] * state[j])

        if i in range(ks, ks + k):
            output.append(state[0])

        state = update_state(state, curr)
        curr = 0

    return output
# }}}

# {{{ convert string to int array
def string_to_int_array(s):
    # list conversion required in python3
    return list(map(int, s))
# }}}

# {{{ encrypt
def encrypt(p, ks):
    return [a ^ b for a, b in zip(p, ks)]
# }}}

# {{{ decrypt
def decrypt(c, ks):
    return [a ^ b for a, b in zip(c, ks)]
# }}}

##{{{ sanitize_inputs
def sanitize_inputs(args):

    if args.outputlength < 1:
        error_str = "Number of output bits must be at least 1"
        usage(error_str)

    if args.keylength < 0 or (
        args.plaintext is not None and args.keylength < len(
            args.plaintext)) or (
            args.ciphertext is not None and args.keylength < len(
                args.ciphertext)):
        error_str = "Key length is negative or smaller than message length"
        usage(error_str)

    if (args.keystreamstart < 0) or\
            ((args.keystreamstart + args.keylength) > args.outputlength):
        error_str = "Keystream bits exceed the range of output bits"
        usage(error_str)

    if len(args.polynom) != len(args.initial):
        error_str = "Lengths of initial state and feedback polynom do not match"
        usage(error_str)

    mode = args.mode

    (plaintext, ciphertext) = "", ""

    if mode == "encrypt":
        if args.plaintext is None:
            error_str = "Plaintext must be specified for encryption"
            usage(error_str)
        plaintext = string_to_int_array(args.plaintext)
    if mode == "decrypt":
        if args.ciphertext is None:
            error_str = "Ciphertext must be specified for decryption"
            usage(error_str)
        ciphertext = string_to_int_array(args.ciphertext)

    polynom = string_to_int_array(args.polynom)
    init_state = string_to_int_array(args.initial)
    key_length = args.keylength
    output_length = args.outputlength
    start_key = args.keystreamstart

    return (mode, plaintext, ciphertext, polynom, init_state, key_length,
            output_length, start_key)
##}}}

##{{{ print_result
def print_result(plaintext, keystream, ciphertext):
    print("Plaintext  = " + str(plaintext))
    print("Keystream  = " + str(keystream))
    print("Ciphertext = " + str(ciphertext))
##}}}

##{{{ add parser arguments
def add_parser_arguments(parser):
    parser.add_argument("-m", "--mode", help="specifies the mode for the\
            program:", type=str, choices=["encrypt", "keystream",
                                          "decrypt"], required=True)
    parser.add_argument("-pol", "--polynom", help="specifies the feedback \
            polynom for the LSFR", type=str, required=True)
    parser.add_argument("-i", "--initial", help="specifies the initial state",
                        type=str, required=True)
    parser.add_argument("-kl", "--keylength", help="specifies the length of\
            the key produces by the LFSR", type=int, required=True)
    parser.add_argument("-n", "--outputlength", help="specifies the length of\
            the output stream of the LFSR", type=int, required=True)
    parser.add_argument("-p", "--plaintext", help="specifies the plaintext to \
            encrypt", type=str, required=False)
    parser.add_argument("-c", "--ciphertext", help="specifies the ciphertext\
            to decrypt", type=str, required=False)
    parser.add_argument("-ks", "--keystreamstart", help="specified the index\
            of the first bit from the output used as key", type=int, required=True)

    return parser.parse_args()
##}}}

# {{{ main
def main():
    parser = argparse.ArgumentParser(prog="Linear Feedback Shift Register")

    args = add_parser_arguments(parser)

    (mode, p, c, pol, init, keyl, outputl, start_key) = sanitize_inputs(args)

    if mode == "encrypt":
        ks = generate_keystream(init, pol, outputl, keyl, start_key)
        ciphertext = encrypt(p, ks)
        print_result(p, ks, ciphertext)
    if mode == "decrypt":
        ks = generate_keystream(init, pol, outputl, keyl, start_key)
        plaintext = decrypt(ciphertext, ks)
        print_result(plaintext, ks, c)
    if mode == "keystream":
        ks = generate_keystream(init, pol, outputl, keyl, start_key)
        print_result("", ks, "")
# }}}

if __name__ == '__main__':
    main()
