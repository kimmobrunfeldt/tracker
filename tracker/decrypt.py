"""
Decrypts text file.

Usage:
    python decrypt.py filename [key]
"""

from Crypto.Cipher import AES
import hashlib
import sys


crypt_key = 'b794aefd-63bb-11e2-9592-705681c24ac3'


def hex2dec(s):
    """Return the integer value of a hexadecimal string s"""
    return int(s, 16)


def hash_key(key):
    """Return sha256 hash digest"""
    return hashlib.sha256(key).digest()


def decrypt_text(ciphertext, key):
    """Decrypts given ciphertext with given key. Ciphertext is excepted to be
    encrypted with AES.MODE_CBC
    Plain text is always padded.
    If unicode object was given to encrypt function, the returned plaintext
    is encoded with utf-8.

    Key must be 8, 16 or 32 bits,
    so sha256 hash is made from given key.
    """
    # Get sha256 digest from key.
    key = hash_key(key)

    # Use AES and Cipher-block chaining mode
    mode = AES.MODE_CBC
    decryptor = AES.new(key, mode, chr(0) * 16)

    plain = decryptor.decrypt(ciphertext)  # Get padded plaintext

    try:
        firstpad = -(hex2dec(plain[-1]) + 1)  # Get position of first padding

    except ValueError:  # Last char was not a number
        raise ValueError("Probably wrong key!")

    return plain[:firstpad]  # Return plain text in unicode


def main():
    try:
        filename = sys.argv[1]
    except IndexError:
        print(__doc__.strip())
        sys.exit(1)

    key = crypt_key
    try:
        # Optional
        key = sys.argv[2]
    except IndexError:
        pass

    print(decrypt_text(open(filename, 'rb').read(), key))


if __name__ == '__main__':
    main()
