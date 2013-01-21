"""
Makes a request to a server and sends output of certain commands to it.
"""

from Crypto.Cipher import AES
import base64
import hashlib
import requests
import subprocess


request_address = 'http://kimmobrunfeldt.com/t/6ced86ba-63b8-11e2-a12b-705681c24ac3.php'

# Cyrpt key for sended text
crypt_key = 'b794aefd-63bb-11e2-9592-705681c24ac3'

# Each command is subprocess.Popen's list format.
commands = [['/sbin/ifconfig']]


def run_command(command):
    """Runs an command and returns the stdout and stderr as a string.

    Args:
        command: Command to execute in Popen's list format.
                 E.g. ['ls', '..']

    Returns:
        tuple. (return_value, stdout, stderr), where return_value is the
        numerical exit code of process and stdout/err are strings containing
        the output. stdout/err is None if nothing has been output.
    """
    p = subprocess.Popen(command, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    return_value = p.wait()
    return return_value, stdout, stderr


def dec2hex(n):
    """Return the hexadecimal string representation of integer n"""
    return "%X" % n


def hash_key(key):
    """Return sha256 hash digest"""
    return hashlib.sha256(key).digest()


def encrypt_text(text, key):
    """Encrypt given text with AES algorithm -> CBC=Cipher-block chaining
    LMore information:
    http://en.wikipedia.org/wiki/Block_cipher_modes_of_operation

    Key must be 8, 16 or 32 bits,
    so sha256 hash is made from given key.
    Text can be a unicode object or encoded text
    """
    if isinstance(text, unicode):
        text = text.encode('utf-8')

    BLOCK_SIZE = 16  # Size of block that algorithm uses. MAX IS 16!!!

    # http://www.di-mgt.com.au/cryptopad.html
    # Pad with spaces. If the text length is equal to blocksize,
    # padding is added, The padded text's final char is always the same as the
    # length of padding. Final char is a number in HEX 0-F(0-15). 0 means that
    # length of padding is 1.
    spacepad = (BLOCK_SIZE - len(text) % BLOCK_SIZE)

    # Text length is same as BLOCK_SIZE, we have to add padding so decrypter
    # knows how much padding to remove.
    if spacepad == 0:
        spacepad = BLOCK_SIZE

    # Add padding and padding's length to text
    text = text + ' ' * (spacepad - 1) + dec2hex(spacepad - 1)

    # Get sha256 digest from key.
    key = hash_key(key)

    mode = AES.MODE_CBC
    encryptor = AES.new(key, mode, chr(0) * 16)

    return encryptor.encrypt(text)  # Encrypt text.


def main():
    message = ''
    for command in commands:
        message += '%s:\n' % command
        return_value, stdout, stderr = run_command(command)
        message += 'stdout:\n%s\n' % stdout
        message += 'stderr:\n%s\n' % stderr

    encrypted_message = encrypt_text(message, crypt_key)

    base66_message = base64.b64encode(encrypted_message)
    data = {'message': base66_message}
    requests.post(request_address, data=data)


if __name__ == '__main__':
    main()
