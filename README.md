# tools

some helpful tools/scripts for every day situations and also some math tools

**caesar.py**
  Computes the CAESAR encryption algorithm. Can also show all possible
  plaintexts and their corresponding keys for a given ciphertext.

**crackpwds.py**
  Takes a file containing password hashes and cracks all hashes for passwords
  with a user-specific size.

**fermat_rsa.py**
  Computes the RSA algorithm. Primes are tested using the Fermat test.

**lagrange.py**
  Computes the Lagrange interpolation formula for an arbitrary number of value
  pairs.

**lfsr.py**
  Can be used to implement arbitrary Linear Feedback Shift Registers (LFSR).

**polynom_calc**
  Small polynomial calculator for Z_2[X]_{p(x)}

**springer_extractor.py**
  Accepts a SearchResult.csv file from Springer and downloads the corresponding
  books (make sure that you have access to those books before starting).

  Does not cover articles (only books).

  Requires 'springer_download.py' from [tuxor1337](https://github.com/tuxor1337/springerdownload)

**square_and_multiply.py**
  Standard square-and-multiply computation.

**substitution.py**
  Can be used to implement an arbitrary substitution cipher.

**textentropy.py**
  Takes a file (or an ID to a Gutenberg file) and computes the min as well as
  the Shannon entropy of all upper/lower case initials.
