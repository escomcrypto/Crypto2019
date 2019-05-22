import base64
import os
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA384
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpRequest
from app.models import PaintingRequest

from .forms import LoginAuthenticationForm, RegistrationForm

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath("views.py")))

def home(request):
    if request.method == 'POST':
        print('reading method post')
        # Create a form instance and populated with data from request:
        authentication_form = LoginAuthenticationForm(request.POST)
        # Check whether it's valid:
        if authentication_form.is_valid():
            return HttpResponseRedirect('register')

    form = LoginAuthenticationForm()

    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(request,
        'app/signin.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
            'form':form
        })

def register(request):
    if request.method == 'POST':
        print('reading method post')
        # Create a form instance and populated with data from request:
        authentication_form = RegistrationForm(request.POST)
        # Check whether it's valid:
        if authentication_form.is_valid():
            return HttpResponseRedirect('home')

    form = RegistrationForm()

    """Renders the register page """
    assert isinstance(request, HttpRequest)
    return render(request,
          'app/signup.html',
          {
              'title':'Sign Up - Art',
              'year':datetime.now().year,
              'form':form
          })
    
#In this view a list of requests that the user has made will be shown
def ordersList(request):
    orders = []
    #result = PaintingRequest.objects.filter(username=request.user.id).values()
    result = PaintingRequest.objects.filter(username="mayrasho").values()
    if(len(result) != 0):
        for r in range(0,len(result)):
            orders.append(result[r]['nameRequest'])
    else:
        print("No hay pedidos")
    return render(request, 
        'app/requestsClient.html', 
        {
            'orders':orders,
            'title':'Orders',
            'year':datetime.now().year,
        })

def addRequest(request):
    '''PaintingRequest.objects.create(
        nameRequest=request.POST["nameRequest"],
        username="mayrasho",
        dateRequest=datetime.now().date,
        description=request.POST["description"],
        image=request.POST["image"],
        status="O"
    )'''
    print(request.FILES)
    return render(request,'orders',
        {
        'title':'Orders',
        'year':datetime.now().year,
        }
    )

def newOrder(request):
    dt=""
    if request.method=="POST":
        dt = datetime.now()
        var = PaintingRequest(
        nameRequest=request.POST["nameRequest"],
        username="mayrasho",
        dateRequest=dt,
        description=request.POST["description"],
        image=request.FILES["image"],
        status='O',
        )
        var.save()
        getOrder(dt)
    return render(request,'app/newOrder.html',
        {
        'title':'New Request',
        'year':datetime.now().year,
        }
    )

def getOrder(dateTime):
    order = PaintingRequest.objects.filter(dateRequest=dateTime, username="mayrasho").values()
    generate_iv(order[0]["id"])
    generate_key(order[0]["id"])
    encrypt_image(order[0]["id"], BASE_DIR+"\\CryptoProject\\app\\static\\images\\"+order[0]["image"].replace("/","\\"))
    
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
    writeBinFile(key, BASE_DIR+'\\CryptoProject\\keys\\orders\\'+str(id)+'_key.bin')
    
def generate_iv(id):
    """generate a random iv of 128 bits and store it in a file in base64"""
    iv = get_random_bytes(16)
    print(BASE_DIR)
    writeBinFile(iv, BASE_DIR+'\\CryptoProject\\keys\\orders\\'+str(id)+'_iv.bin')
    

def encrypt_image(id, image_file_name):
    """encrypt and store the client photo"""
    image_bytes = get_image_bytes(image_file_name)
    key = readBinFile(BASE_DIR+'\\CryptoProject\\keys\\orders\\'+str(id)+'_key.bin')
    iv = readBinFile(BASE_DIR+'\\CryptoProject\\keys\\orders\\'+str(id)+'_iv.bin')
    
    #build an AES cipher using OFB mode
    cipher = AES.new(key, AES.MODE_OFB, iv)
    #encrypt the images bytes
    cipher_image_bytes = cipher.encrypt(image_bytes)
    writeBinFile(cipher_image_bytes, BASE_DIR+'\\CryptoProject\\app\\static\\images\\originals\\'+str(id)+'.bin')

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
def welcome(request):
    return render(request,'app/mainClient.html',
        {
        'title':'welcome',
        'year':datetime.now().year,
        }
    )
