from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

def encrypt_key(plain_key):
    """encrypt the AES key with the hardcoded key"""
    key = b'\x9a\xb8\xcf*f\x94\xe8c\x98\r\xd4J\\ }$'
    iv = b'\x19\xa3B(\xe4\xeb\xdb3c\x1f\x17\xad\x01P\x04\xf8'
    #build an AES cipher using OFB mode
    cipher = AES.new(key, AES.MODE_OFB, iv)
    #encrypt the AES_key
    cipher_key = cipher.encrypt(plain_key)
    return cipher_key

def decrypt_key(cipher_key):
    """decrypt the AES key with the hardcoded key"""
    key = b'\x9a\xb8\xcf*f\x94\xe8c\x98\r\xd4J\\ }$'
    iv = b'\x19\xa3B(\xe4\xeb\xdb3c\x1f\x17\xad\x01P\x04\xf8'
    #build an AES cipher using OFB mode
    cipher = AES.new(key, AES.MODE_OFB, iv)
    #decrypt the AES_key
    plain_key = cipher.decrypt(cipher_key)
    return plain_key