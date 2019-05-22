import base64
import os
from datetime import datetime
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA384
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath("views.py")))

def writeBinFile(file_bytes, file_name):
    """write a binary file in base64"""
    file = open(file_name, 'wb')
    file.write(base64.b64encode(file_bytes)) 
    file.close()
    
def readBinFile(file_name):
    """read a binary file in base64"""
    file = open(file_name, 'rb')
    file_bytes = file.read()
    file.close()
    return base64.b64decode(file_bytes)

def get_image_bytes(image_file_name):
    """get the bytes of an image file in base64"""
    image_file = open(image_file_name,'rb')
    image_bytes = image_file.read()
    return image_bytes

def build_image(image_name, image_bytes):
    """build an image from bytes"""
    file = open(image_name, 'wb')
    file.write(image_bytes) 
    file.close()

def generate_key(id):
    """generate a random key of 128 bits and store it in a file in base64"""
    key = get_random_bytes(16)
    writeBinFile(key, BASE_DIR+'/keys/orders/'+str(id)+'_key.bin')
    
def generate_iv(id):
    """generate a random iv of 128 bits and store it in a file in base64"""
    iv = get_random_bytes(16)
    writeBinFile(iv, BASE_DIR+'/keys/orders/'+str(id)+'_iv.bin')

def encrypt_image(id, image_file_name):
    """encrypt and store the client photo"""
    image_bytes = get_image_bytes(image_file_name)
    key = readBinFile(BASE_DIR+'/keys/orders/'+str(id)+'_key.bin')
    iv = readBinFile(BASE_DIR+'/keys/orders/'+str(id)+'_iv.bin')
    
    #build an AES cipher using OFB mode
    cipher = AES.new(key, AES.MODE_OFB, iv)
    #encrypt the images bytes
    cipher_image_bytes = cipher.encrypt(image_bytes)
    writeBinFile(cipher_image_bytes, BASE_DIR+'/app/static/images/originals/'+str(id)+'.bin')

def decrypt_image(id):
    """read and decrypt the client photo"""
    cipher_image = readBinFile(BASE_DIR+'/app/static/images/originals/'+str(id)+'.bin')
    key = readBinFile(BASE_DIR+'/keys/orders/'+str(id)+'_key.bin')
    iv = readBinFile(BASE_DIR+'/keys/orders/'+str(id)+'_iv.bin')
    
    #build an AES cipher using OFB mode
    cipher = AES.new(key, AES.MODE_OFB, iv)
    #decrypt the cipher images bytes
    plain_image_bytes = cipher.decrypt(cipher_image)
    build_image(BASE_DIR+'/app/static/images/originals/'+str(id)+'_decrypted.jpg', plain_image_bytes)

def generate_RSA_keys(id):
    """generate a RSA key pair and stored in .pem files"""
    key = RSA.generate(1024)
    private_key = key.export_key()
    prikey_file = open(BASE_DIR+'/keys/users/'+str(id)+'_private.pem', 'wb')
    prikey_file.write(private_key)
    public_key = key.publickey().export_key()
    pubkey_file = open(BASE_DIR+'/keys/users/'+str(id)+'_public.pem', 'wb')
    pubkey_file.write(public_key)

def signing_process(user_id, order_id):
    """sign the order_confirmation"""
    order_file = open(BASE_DIR+'/app/static/orders/'+str(order_id)+'_order.txt', 'r')
    order = order_file.read().encode()  #encode cast string to bytes
    private_key = RSA.import_key(open(BASE_DIR+'/keys/users/'+str(user_id)+'_private.pem').read())
    h = SHA384.new(order)
    signature = pkcs1_15.new(private_key).sign(h)
    writeBinFile(signature, BASE_DIR+'/app/static/orders/'+str(order_id)+'_signature.bin')

def verifying_process(user_id, order_id):
    """verifying"""
    public_key = RSA.import_key(open(BASE_DIR+'/keys/users/'+str(user_id)+'_public.pem').read())
    order_file = open(BASE_DIR+'/app/static/orders/'+str(order_id)+'_order.txt', 'r')
    order = order_file.read().encode() #encode cast string to bytes
    signature = readBinFile(BASE_DIR+'/app/static/orders/'+str(order_id)+'_signature.bin')
    h = SHA384.new(order)
    try:
        pkcs1_15.new(public_key).verify(h, signature)
        print("The signature is valid")
    except (ValueError, TypeError):
        print("The signature is not valid")

def build_order_confirmation(order_id, user_name, order_name, description, order_date, delivery_date, cost):
    oc = '' #text for the order confirmation
    oc = oc + str(datetime.now().date()) + '\n\n'
    oc = oc + 'ORDEN CONFIRMATION \n\n'
    oc = oc + 'ORDER NUMBER: ' + str(order_id) + '\n\n'
    oc = oc + 'ORDER DETAILS \n'
    oc = oc + '\tORDER DATE: ' + str(order_date) + '\n'
    oc = oc + '\tUSER: ' + user_name + '\n'
    oc = oc + '\tORDER NAME: ' + order_name + '\n'
    oc = oc + '\tDESCRIPTION: ' + description + '\n\n'
    oc = oc + 'DELIVERY \n'
    oc = oc + '\tDELIVERY DATE: ' + str(delivery_date) + '\n\n'
    oc = oc + 'COST \n'
    oc = oc + '\tTOTAL COST: $'+ str(cost) + '.00 \n'
    
    order_confirmation_file = open(BASE_DIR+'/app/static/orders/'+str(order_id)+'_OrderConfirmation.txt','w')
    order_confirmation_file.write(oc)

if __name__ == '__main__':
    """
    generate_key(1)
    generate_iv(1)
    encrypt_image(1,BASE_DIR+'/app/static/images/originals/mensaje.jpg')
    decrypt_image(1)
    generate_RSA_keys(2)
    #signing_process(2, 2)
    verifying_process(2, 2)
    """
    build_order_confirmation(123, 'Victor Nolasco', 'My first portrait', 'I want a colorfull portrait', 543, 543, 250)