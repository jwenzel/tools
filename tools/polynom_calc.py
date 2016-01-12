#!/usr/bin/python3
# -*- coding: utf-8 -*-

# written for Python2
# for Python3: adjust print functions to enable fancy look :-)

"""
    Schreiben Sie ein Programm in Python, welches zwei Polynome f(x), g(x) in
    Z_2[X] (Polynomring Z_2[x]) als Kommandozeilenparameter engegennimmt und die
    folgenden Werte als Ausgabe liefert:

    - f(x) + g(x) (Summe)
    - f(x) - g(x) (Differenz)
    - f(x) * g(x) (Multiplikation)
    - f(x) / g(x) (Polynomdivision)

    Die Polynome können Sie dabei als Binärstrings dem Programm übergeben. Die
    Ausgabe soll in der Form
        
            f(x) o g(x) = a_ix^i + a_{i-1}x^{i-1} + ... + a_1x + a_0

    erfolgen mit o \in {+,-,*,/}.
"""

__author__  = 'Jakob Wenzel'
__email__   = 'jakob.wenzel at uni-weimar dot de'
__date__    = '2015-01-06'
__version__ = 1.0

import sys

##{{{ error and usage
def error(message):
    """ Prints error message. """
    sys.stderr.write(message)

def usage(message):
    """ Prints message and quits the program. """
    if message:
        print("---------------------------------------------------")
        error(message)
        print
        print("---------------------------------------------------")

    print
    usage_str = "Usage: " + sys.argv[0] + " <pol_a> <pol_b>"
    error(usage_str)
    print
    print("--------------------------------------------------------")
    print("pol_a, pol_b - two polynomials as binary string (Z_2[X])")
    print("--------------------------------------------------------")
    exit(1)
##}}}

##{{{ print
def print_pol(message, x, y):
    """ 
        Gets a bitstring as input, where the bits denote the coefficients of a
        polynomial in Z_2[X]. Outputs the polynomial in a readable format:

        a_ix^i + a_{i-1}x^{i-1} + ... + a_1x + a_0
    """
    
    ctr_x = len(x) - 1
    ctr_y = len(y) - 1

    if x == '0':
        output_str = '0'
    else:
        output_str = ""


        if x[0] == '1':
            output_str += "x^" + str(ctr_x)

        ctr_x -= 1

        for i in x[1:]:
            if (i == '1') and ctr_x != 0:
                output_str += " + " + "x^" + str(ctr_x)
            if (i == '1') and ctr_x == 0:
                output_str += " + 1"
            ctr_x -= 1

    # if second argument is not empty
    # should only be the case for division (remainder)
    if y:
        output_str += "   Remainder: "
        if y[0] == '1':
            output_str += "x^" + str(ctr_y)

        ctr_y -= 1

        for i in y[1:]:
            if (i == '1') and ctr_y != 0:
                output_str += " + " + "x^" + str(ctr_y)
            if (i == '1') and ctr_y == 0:
                output_str += " + 1"
            ctr_y -= 1

    if not output_str:
        print(message + '0')
    else:
        print(message + output_str)
##}}}

##{{{ degree of polynomials
def get_degree(a):
    return (len(a) - 1)

def get_degree_int(a):
    return (get_degree(bin(a)[2:]))
##}}}

##{{{ sum
def poly_sum(a,b):
    """ Returns the sum of two polynomials a and b as integer. """
    return (int(a,2)^int(b,2))
##}}}

##{{{ difference
def poly_diff(a,b):
    """ Returns the difference of two polynomials a and b as integer. """
    return (int(a,2)^int(b,2))
##}}}

##{{{ multiplication
def poly_mul(a,b):
    """ Returns the product of two polynomials a and b as integer. """
    
    tmp = ""
    result = 0

    # always guarantee that the bigger value is multiplied with the smaller
    # value (smallest possible number of SHIFT and ADD operations)
    if (len(a) < len(b)):
        tmp = a
        a = b
        b = tmp

    left = int(a, 2)
    right = int(b, 2)
    
    for i in range(0, len(b)):
        if (right & 1):
            result = result^(left << (i))
        right = right >> 1

    return result
##}}}

##{{{ division
def poly_div(a,b):
    """
        Returns (division result, remainder) of two polynomials a and b as
        integers
    """
    result = 0
    remainder = 0
    right_current = 0
    
    left = int(a, 2)
    right = int(b, 2)

    # if deg(a) is smaller than deg(b): return 0 + remainder b
    if (get_degree_int(left) < get_degree_int(right)):
        return (0, left)

    # else: polynomial division
    deg_a = get_degree(a)
    deg_b = get_degree(b)

    deg_diff = deg_a - deg_b

    # compute polynomial division until the potential remainder (left) is of
    # same degree as the divisor (right)
    for i in range(deg_diff, 0, -1):
        right_current = right << i

        if (get_degree_int(left) >= get_degree_int(right_current)):
            left = left^right_current
            result = result^(1 << i)

    # if the potential remainder (left) is of same degree as the divisor (right)
    # => result is increased by 1 and remainder is computed by XORing left and
    # right
    if (get_degree_int(left) == get_degree_int(right)):
        left = left^right
        result = result^1

    remainder = left

    return (result, remainder)
##}}}

##{{{ main
def main():
    """
        Takes two polynomials as binary string as input and outputs
        their sum, difference, product, and division
    """

    # check if enough arguments are given
    if len(sys.argv) != 3:
        usage("");
    
    # check if arguments are of numeric type
    for val in sys.argv[1:]:
    #    if not val.isdigit: # Python2
         if not unicode(val, 'utf-8').isnumeric(): # Python3
            error_str = "Argument '" + val + "' is not valid."
            usage(error_str)
    
    # remove leading zeroes
    pol_a = sys.argv[1].lstrip('0')
    pol_b = sys.argv[2].lstrip('0')

    # second polynom g(x) must not be 0
    if not pol_b:
        error_str = "Second argument g(x) must not be '0'."
        usage(error_str)

    # check if inputs are binary strings
    for val in sys.argv[1:]:
        try:
            int(val, 2)
        except ValueError:
            error_str = "Argument '" + val + "' is not a binary string."
            usage(error_str)

    # doing the actual computation
    p_sum          = poly_sum(pol_a, pol_b)
    p_diff         = poly_diff(pol_a, pol_b)
    p_mul          = poly_mul(pol_a, pol_b)
    (p_div, p_rem) = poly_div(pol_a, pol_b)

    print_sum              = bin(p_sum)[2:]
    print_diff             = bin(p_diff)[2:]
    print_mul              = bin(p_mul)[2:]
    (print_div, print_rem) = (bin(p_div)[2:], bin(p_rem)[2:])

    # print results
    print("----------------------------------------------")
    print_pol("Input polynomial f(x) = ", pol_a, "")
    print_pol("Input polynomial g(x) = ", pol_b, "")
    print_pol("SUM       f(x) + g(x) = ", print_sum, "")
    print_pol("DIFF      f(x) - g(x) = ", print_diff, "")
    print_pol("MUL       f(x) * g(x) = ", print_mul, "")
    print_pol("DIV       f(x) / g(x) = ", print_div, print_rem)
    print("----------------------------------------------")

##}}}

if __name__ == '__main__':
    main()
