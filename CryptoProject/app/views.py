import base64
import os

from io import BytesIO
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle
from reportlab.platypus import Table
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from app.models import PaintingRequest

import random
from datetime import timedelta

from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA384
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.http import HttpRequest
from django.views.generic import View

from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.utils.datastructures import MultiValueDictKeyError

from .forms import LoginAuthenticationForm, RegistrationForm

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath("views.py")))

"""==============================="""
"""Roles and Permissions functions"""
"""==============================="""

# Paintor role tag
pnt_login_required = user_passes_test(lambda u: True if (not(u.is_superuser) and u.is_staff and u.is_active) else False, login_url='/')

def paintor_login_required(view_func):
    decorated_view_func = login_required(pnt_login_required(view_func), login_url='/')
    return decorated_view_func

# Client role tag
clt_login_required = user_passes_test(lambda u: True if (not(u.is_superuser) and not(u.is_staff) and u.is_active) else False, login_url='/')

def client_login_required(view_func):
    decorated_view_func = login_required(clt_login_required(view_func), login_url='/')
    return decorated_view_func

"""==============================="""
"""         Systems Views         """
"""==============================="""

def home(request):
    if request.method == 'POST':
        print('reading method post')
        # Create a form instance and populated with data from request:
        authentication_form = LoginAuthenticationForm(request.POST)
        # Check whether it's valid:
        if authentication_form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
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
        # Create a form instance and populated with data from request:
        authentication_form = RegistrationForm(request.POST)
        # Check whether it's valid:
        if authentication_form.is_valid():
            email = request.POST.get('email')
            email_confirmation = request.POST.get('email_confirmation')
            username = request.POST.get('username')
            password = request.POST.get('password')

            if email == email_confirmation:
                try:
                    user = User.objects.get(username=username)
                except User.DoesNotExist:
                    user = None
                if user is None:
                    new_user = User.objects.create_user(username=username, email=email, password=password)
                    new_user.is_superuser = False
                    new_user.is_staff = False
                    new_user.save()
                    return HttpResponseRedirect('/')
              
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
@client_login_required
@login_required(login_url='/')
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

def newOrder(request):
    dt = ""
    if request.method == "POST":
        dt = datetime.now()
        var = PaintingRequest(nameRequest=request.POST["nameRequest"],
        username="mayrasho",
        dateRequest=dt,
        description=request.POST["description"],
        image=request.FILES["image"],
        status='O',
        cost=random.randint(150,250))
        dateDelevery = dt.date() + timedelta(days=30)
        print(dateDelevery)
        var.save()
        getOrder(dt)

    return render(request,'app/newOrder.html',
        {
        'title':'New Request',
        'year':datetime.now().year,
        })

@paintor_login_required
@login_required(login_url='/')
def welcome(request):
    return render(request,'app/mainClient.html',
        {
        'title':'welcome',
        'year':datetime.now().year,
        })

def getOrder(dateTime):
    order = PaintingRequest.objects.filter(dateRequest=dateTime, username="mayrasho").values()
    generate_iv(order[0]["id"])
    generate_key(order[0]["id"])
    encrypt_image(order[0]["id"], BASE_DIR + "\\CryptoProject\\app\\static\\images\\" + order[0]["image"].replace("/","\\"))
    
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
    writeBinFile(key, BASE_DIR + '\\CryptoProject\\keys\\orders\\' + str(id) + '_key.bin')
    
def generate_iv(id):
    """generate a random iv of 128 bits and store it in a file in base64"""
    iv = get_random_bytes(16)
    writeBinFile(iv, BASE_DIR + '\\CryptoProject\\keys\\orders\\' + str(id) + '_iv.bin')

def encrypt_image(id, image_file_name):
    """encrypt and store the client photo"""
    image_bytes = get_image_bytes(image_file_name)
    key = readBinFile(BASE_DIR + '\\CryptoProject\\keys\\orders\\' + str(id) + '_key.bin')
    iv = readBinFile(BASE_DIR + '\\CryptoProject\\keys\\orders\\' + str(id) + '_iv.bin')
    
    #build an AES cipher using OFB mode
    cipher = AES.new(key, AES.MODE_OFB, iv)
    #encrypt the images bytes
    cipher_image_bytes = cipher.encrypt(image_bytes)
    writeBinFile(cipher_image_bytes, BASE_DIR + '\\CryptoProject\\app\\static\\images\\originals\\' + str(id) + '.bin')

def decrypt_image(id):
    """read and decrypt the client photo"""
    cipher_image = readBinFile(BASE_DIR + '\\CryptoProject\\app\\static\\images\\originals\\' + str(id) + '.bin')
    key = readBinFile(BASE_DIR + '\\CryptoProject\\keys\\orders\\' + str(id) + '_key.bin')
    iv = readBinFile(BASE_DIR + '\\CryptoProject\\keys\\orders\\' + str(id) + '_iv.bin')
    
    #build an AES cipher using OFB mode
    cipher = AES.new(key, AES.MODE_OFB, iv)
    #decrypt the cipher images bytes
    plain_image_bytes = cipher.decrypt(cipher_image)
    build_image(BASE_DIR + '\\CryptoProject\\app\\static\\images\\originals\\' + str(id) + '_decrypted.jpg', plain_image_bytes)

def generate_RSA_keys(id):
    """generate a RSA key pair and stored in .pem files"""
    key = RSA.generate(1024)
    private_key = key.export_key()
    prikey_file = open(BASE_DIR + '\\CryptoProject\\keys\\users\\' + id + '_private.pem', 'wb')
    prikey_file.write(private_key)
    public_key = key.publickey().export_key()
    pubkey_file = open(BASE_DIR + '\\keys\\users\\' + id + '_public.pem', 'wb')
    pubkey_file.write(public_key)

"""==============================="""
"""         PDF Generation        """
"""==============================="""

def generar_orden(request):
    response = HttpResponse(content_type='application/pdf')
    pdf_name = "orders.pdf"
    #response['Content-Disposition'] = 'attachment; filename=%s' % pdf_name
    buffer = BytesIO()

    '''Drawing pdf logo'''
    pdf = canvas.Canvas(buffer)
    logo_image = BASE_DIR + '\\CryptoProject\\app\\static\\images\\art.PNG'
    pdf.drawImage(logo_image, 40, 680, 240, 180,preserveAspectRatio=True)
    '''Order Content '''
    #Establecemos el tamaño de letra en 16 y el tipo de letra Helvetica
    pdf.setFont("Helvetica-Bold", 16)
    #Dibujamos una cadena en la ubicación X,Y especificada
    pdf.drawString(320, 760, u"Confirmación de Pedido")

    order = open(BASE_DIR + '\\CryptoProject\\app\\static\\orders\\123_OrderConfirmation.txt', "r")
    height = 660
    width = 40
    pdf.setFont("Helvetica", 14)

    for line in order:
        pdf.drawString(width, height, line.strip().encode())
        height = height - 20

    shopping_image = BASE_DIR + '\\CryptoProject\\app\\static\\images\\shopping.jpg'
    pdf.drawImage(shopping_image, 330, 320, 250, 350, preserveAspectRatio=True)

    pdf.showPage()
    pdf.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response