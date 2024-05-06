# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os
import hashlib
import binascii

# Inspiration -> https://www.vitoshacademy.com/hashing-passwords-in-python/


def hash_pass(password):
    """Hash a password for storing."""

    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                  salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash)  # return bytes


def verify_pass(provided_password, stored_password):
    #return True
    """Verify a stored password against one provided by user"""
    try:
        stored_password = stored_password.decode('ascii')
        salt = stored_password[:64]
        stored_password = stored_password[64:]
        pwdhash = hashlib.pbkdf2_hmac('sha512',
                                      provided_password.encode('utf-8'),
                                      salt.encode('ascii'),
                                      100000)
        pwdhash = binascii.hexlify(pwdhash).decode('ascii')
        return pwdhash == stored_password
    except:
        return False


if __name__=='__main__':
    password = hash_pass("Passw0rd$")
    print(password)
    ver = verify_pass('Passw0rd$',password)
    print(ver)
#this_is_a_test