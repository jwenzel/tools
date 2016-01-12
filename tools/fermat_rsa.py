#!/usr/bin/python3
# -*- coding: utf-8 -*-

""" fermat_rsa.py

    Implementieren Sie den Fermat-Test und den RSA-Algorithmus aus der Vorlesung
    (Folien 134 und 123) in Python. Das Programm soll dabei vier Werte p, q, m
    und k als Kommandozeilen- parameter entgegennehmen und folgende
    Funktionalitaet bieten:

    - Behandlung fehlerhafter Eingaben, z. B.: falsche Anzahl oder falscher Typ
    von Kom- mandozeilenparametern.
    - Testen mittels des Fermat-Tests, ob p und q prim sind. Die Anzahl an
    verwendeten Zufallszahlen soll dabei k entsprechen. Wenn p und/oder q keine
    Primzahlen sind, soll ihr Programm 'p and/or q not prime' ausgeben.
    - Berechnen des RSA Modulus n = p · q und der Euler'schen phi--Funktion
    phi(n) = (p − 1) · (q − 1).
    - Auswahl des kleinsten oeffentlichen Schluessels e \in N * phi(n) mit
    ggT(phi(n), e) = 1. Sie können die Implementierung des Euklidischen
    Algorithmus' aus dem Tutorium dafür verwenden.
    - Berechnen des geheimen Schluessels d mit e·d \equiv 1 (mod phi(n)).
    Hierfuer muessten Sie ihren Code um die Berechnung des Erweiterten
    Euklidischen Algorithmus' (Berechnung des multiplikativen Inversen, Folie
    112) erweitern.
    - Verschluesseln der Nachricht m unter dem oeffentlichen Schluessel (e, n)
    mit c = m e mod n.
    - Entschluesseln des Chiffretextes c unter dem privaten Schluessel (d, n)
    mit m ′ = c d mod n.
    - Aussgabe von c, d, e, m, m ′ .

    Hinweis: Funktioniert der Algorithmus korrekt, muss gelten m \equiv m' mod
    n.
    
    Beispielaufruf:
    #./fermat_rsa_<xxxxx>.py 73 67 507 10
    c = 3321, d = 2977, e = 3649, m = 507, m’ = 507
    #./fermat_rsa_<xxxxx>.py 73 66 507 10
    p and/or q not prime
"""

__author__  = 'Jakob Wenzel'
__email__   = 'jakob.wenzel at uni-weimar dot de'
__date__    = '2015-11-24'
__version__ = 1.0

import sys
# random generator is seeded with urandom() if avaiablel; and else with the
# current system time
# one can use os.urandom() if cryptographc random numbers are required
import random

##{{{ doctests
"""
>>> import fermat_rsa
>>> fermat_rsa.fermat_test(15485867,1000)
True
>>> fermat_rsa.fermat_test(101208,250)
False
>>> fermat_rsa.fermat_test(19,10)
True
>>> fermat_rsa.fermat_test(0,10)
False
>>> fermat_rsa.fermat_test(3,20)
False
>>> fermat_rsa.extended_euclid(19,154)
(1, -9, 73)
>>> fermat_rsa.extended_euclid(20,71)
(1, -9, 32)
>>> fermat_rsa.extended_euclid(497,131)
(1, -34, 129)
>>> fermat_rsa.extended_euclid(22,77)
(11, 1, -3)
>>> fermat_rsa.rsa(17,19,100)
(104, 173, 5, 100, 100)
>>> fermat_rsa.rsa(23,71,375)
(1539, 1027, 3, 375, 375)
>>> fermat_rsa.rsa(13093,11587,1234567)
(7767762, 60673565, 5, 1234567, 1234567)
>>>
"""
##}}}

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
    usage_str = "Usage: " + sys.argv[0] + " <p> <q> <m> <k>"
    error(usage_str)
    print
    print("---------------------------------------------------")
    print("p,q - prime numbers to compute the RSA modulus n")
    print("m   - message to be encrypted using RSA")
    print("k   - number of iterations for the Fermat Test")
    print("---------------------------------------------------")
    exit(1)
##}}}

##{{{ fermat_test
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

##{{{ extended_euclid
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
        z = a / b
        return (d,y,x - (z * y))
##}}}

##{{{ rsa
def rsa(p,q,m):
    """
    Computes the RSA modulus n = p * q
    Computes the phi function phi(n) = (p-1)(q-1)
    Choose the smallest possible value e (pub key) with gcd(phi(n),e) = 1
    Compute the multiplicative inverse d (priv key) of e <- extended euclid
    Encrypt m: c = m^d mod n
    Decrypt c: m' = c^e mod n
    Check whether m' == m
    """
    
    n = p * q
    phi_n = (p - 1) * (q - 1)


    # choose the smallest possible value for e (pub key)
    for i in range(2,phi_n):
        if extended_euclid(phi_n,i)[0] == 1:
            e = i
            break

    # computing the secret key d with e \equiv d^{-1} mod phi(n)
    # the '% phi_n' is required since the inverse can be negative
    d = extended_euclid(phi_n,e)[2] % phi_n
    
    c = pow(m,e,n)

    m_new = pow(c,d,n)

    return(c,d,e,m,m_new)
##}}}

##{{{ print result
def print_result(n,c,d,e,m,m_new):
    print("----------------------------------------------")
    print'{:>8}{:>22}'.format("Message m", str(m))
    print'{:>12}{:>18}'.format("RSA modulus n", str(n))
    print'{:>12}{:>19}'.format("Public key e", str(e))
    print'{:>12}{:>18}'.format("Private key d", str(d))
    print'{:>12}{:>14}'.format("Encrypting m to c", str(c))
    print'{:>12}{:>13}'.format("Decrypting c to m'", str(m_new))
    print("----------------------------------------------")
##}}}

##{{{ main
def main():

    if len(sys.argv) != 5:
        usage("")

    # check type of command line parameters (numeric type and positive)
    for val in sys.argv[1:]:
        if not unicode(val, 'utf-8').isnumeric() or int(val) < 0:
            error_str = "Argument '" + val + "' is not valid"
            usage(error_str)

    p = int(sys.argv[1])
    q = int(sys.argv[2])
    m = int(sys.argv[3])
    k = int(sys.argv[4])

    # check whether p and q are primes
    if not (fermat_test(p,k) and fermat_test(q,k)):
        error_str = "p and/or q not prime"
        usage(error_str)

    # encrypt message
    (c,d,e,m,m_new) = rsa(p,q,m)

    if m == m_new:
        print_result(p*q,c,d,e,m,m_new)
    else:
        error_str = "Something went wrong with the decryption"
        error(error_str)
        exit(1)
##}}}

if __name__ == '__main__':
    main()
