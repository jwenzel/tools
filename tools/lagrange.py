#!/usr/bin/python3
# -*- coding: utf-8 -*-

# pretty error print in python3
from __future__ import print_function
# used to get certain elements from a list
from operator import itemgetter

""" 
    Lagrange Interpolation

    Takes the number of value pairs k, a modulus n, and k pairs of values
    (integer) as input and outputs the corresponding polynomial using Lagrange
    interpolation.

    Output is given as an easy-to-read polynomial.
"""

__author__  = 'Jakob Wenzel'
__email__   = 'jakob.wenzel at uni-weimar dot de'
__date__    = '2016-01-07'
__version__ = 1.0

import sys
import random


NUM_TESTS_FERMAT = 10

##{{{ doctests
"""
>>> import lagrange
>>> lagrange.lagrange(3,479,[4,6,1,9,2,4])
[2, 468, 18]
>>> lagrange.lagrange(3,127,[1,48,3,5,7,104])
[13, 117, 45]
>>>
"""
##}}}

##{{{ error and usage
def error(message):
    """ Prints error message. """
    print(message, file=sys.stderr)

def usage(message):
    """ Prints message and quits the program. """
    if message:
        print("---------------------------------------------------")
        error(message)
        print("---------------------------------------------------")

    print()
    usage_str = "Usage: " + sys.argv[0]+ " <k> <n> <a_1,b_1> ... <a_k,b_k> "
    error(usage_str)
    print
    print("-----------------------------------------------------------------")
    print("k       - number of pairs")
    print("n       - prime modulus (defines the field of the coefficients)")
    print("a_i,b_i - pair of values which satisfies p(a_i) = b_i")
    print("-----------------------------------------------------------------")
    exit(1)
##}}}

##{{{ fermat_test (test if prime)
def fermat_test(n, k):
    """
    Uses the Fermat Test with k iterations to check whether the input n is a
    composite number or likely to be a prime

    returns True if probably prime
    returns False if composite
    """

    if n <= 3:
        return False

    for i in range(k):
        a = random.randrange(2, n-2)
        b = pow(a, n-1, n)
        if b != 1:
            return False

    return True
##}}}

##{{{ extended_euclid (multiplicative inverse)
def extended_euclid(a,b):
    """
    Computes the extended Euclidean Algorithm. Input are two values with a > b
    Outputs three values (d,x,y):
        d     - gcd(a,b)
        (x,y) - coefficients of the linear combination L = x*a + y*b
        y     - is the multiplicative inverse of b mod a
    """
    
    # for the algorithm it is required that a > b
    # if this is not the case: swap

    if a <= b:
        tmp = a
        a = b
        b = tmp

    r = a % b
    if r == 0:
        return (b,0,1)
    else:
        (d,x,y) = extended_euclid(b,a % b)
        z = a // b
        return (d,y,x - (z * y))
##}}}

##{{{ check if input is a number (check compatible with python2/3)
def is_number(x):
    try:
        float(x)
        return True
    except ValueError:
        return False
##}}}

##{{{ print
def print_pol(x):
    """ 
        Gets a list x as input, where the elements denote the coefficients of a
        polynomial in Z[X]_p. Outputs the polynomial in a readable format:

        a_ix^i + a_{i-1}x^{i-1} + ... + a_1x + a_0
    """
    
    x_len = len(x)

    # check whether the list x is empty
    if not x:
        output_str = '0'
    else:
        output_str = ""

        # add the coeff with the highest order
        output_str += str(x[0]) + "x^" + str(x_len - 1)

        # add all but the constant value to output_str
        for coeff in range(1,x_len - 1):
            output_str += " + " + str(x[coeff]) + "x^" + str(x_len - coeff - 1)

        # add the constant value
        output_str += " + " + str(x[x_len - 1])

    print("p(x) = " + output_str)
##}}}

##{{{ multiplying polynomials
def pol_mul(p,q):
    """ 
        Accepts two polynomials as list of coefficients (constants first) and
        outputs their product, where the output is again given as a list
        (constant equals first element).
    """

    # multiplication as suggested by miracle173 on stackoverflow
    # http://stackoverflow.com/questions/5413158/multiplying-polynomials-in-python
#    return [sum([ p[i]*q[k-i] for i in range(max([0,k-len(q)+1]),1+min([k,len(p)-1]))]) for k in range(len(p)+len(q)-1)]

    # easy-to-read variant:
    # it must hold that deg(p) <= deg(q)
    if (len(p) > len(q)):
        tmp = p
        p = q
        q = tmp

    res = [0] * (len(p) + len(q) - 1)

    for i in range(0, len(p)):
        for j in range(0, len(q)):
            res[i + j] += p[i] * q[j]

    return res
##}}}

##{{{ lagrange (generic)
def lagrange_generic(k,n,value_pairs):
    """ 
        Accepts a modulus n and a list consisting of k value pairs (<int a_i>,
        <int b_i>). Outputs the corresponding polynomial satisfying p(a_i) = b_i
        for all pairs (a_i, b_i) as a bitstring.
    """

    # list for storing the coefficients of the three polynomials
    p_coeffs = [[] * k] * k

    for i in range(0, k):
        # get all values a_j with a_j != a_i
        curr_ais = [x for j, x in enumerate(value_pairs[::2]) if j != i]

        # get coefficient of the polynomial (nominator)
        # (first elements is the constant term)
        # NOTE: pol_mul accepts the polynomial in reversed order
        p_coeffs[i] = [-curr_ais[0], 1]

        for l in range(1, k-1):
            p_coeffs[i] = pol_mul(p_coeffs[i], [-curr_ais[l], 1])

        # get the current b_i
        curr_bi = value_pairs[(2 * (i + 1)) - 1]

        # get current ai and compute the denominator (+ normalize)
        curr_ai = value_pairs[2 * i]

        denom = curr_ai - curr_ais[0]

        for l in range(1, k-1):
            denom *= (curr_ai - curr_ais[l])
        
        denom = denom % n

        # get the multiplicative inverse of denom in Z_n
        inv = extended_euclid(n,denom)[2]

        # multiply each coefficient with the current b_i and inv (+ normalize)
        p_coeffs[i] = [(j * curr_bi * inv) % n for j in p_coeffs[i]]

    # add all corresponding coefficients
    # the '*' unpacks p_coeffs (iterates over all elements within p_coeffs)
    final_coeffs = [sum(x) for x in zip(*p_coeffs)]

    # normalize
    final_coeffs = [j % n for j in final_coeffs]

    return list(reversed(final_coeffs))
##}}}

##{{{ main
def main():
    
    # check if arguments are of numeric type
    for val in sys.argv[1:]:
        if not is_number(val):
            error_str = "Argument '" + val + "' is not valid."
            usage(error_str)

    num_of_pairs = int(sys.argv[1])

    # check if enough arguments are given
    if len(sys.argv) != (2 * num_of_pairs) + 3:
        error_str = "Incorrect number of arguments."
        usage(error_str);

    # check whether n is prime
    if not fermat_test(int(sys.argv[2]), NUM_TESTS_FERMAT):
        error_str = "n = " + sys.argv[2] + " is not prime."
        usage(error_str)

    # get the pairs
    # map(f, lst) calls the functions f for all elements of lst
    value_pairs = list(map(int, sys.argv[3:]))
    
    # check whether all values a_i are distinct
    # get all elements from argv[3:] at odd positions (all a_i's)
    # some_list[start:stop:step]
    inputs = value_pairs[::2]
    # a 'set' does not allow double entries
    if len(set(inputs)) != num_of_pairs:
        error_str  = "The inputs a_i are not distinct."
        usage(error_str)

    k = int(sys.argv[1])
    n = int(sys.argv[2])

    print("---------------------------------------------------")
    print("Computing Lagrange interpolation")
    print("---------------------------------------------------")
    print("Number of pairs (k) = " + str(k))
    print("Coefficients in the field Z_" + "{" + str(n) + "}")
    print("------------------")
    print("Pairs:")
    for i in range(0, len(value_pairs), 2):
        print("p(" + str(value_pairs[i]) + ") = " + str(value_pairs[i+1]))
    print("------------------")

    print("p(x) satisfying p(a_i) = b_i for all i in {1,...," + str(k) + "}:")

    result = lagrange_generic(k,n,value_pairs)

    print()
    #print_pol(list(reversed(result)))
    print_pol(result)
##}}}

if __name__ == '__main__':
    main()
