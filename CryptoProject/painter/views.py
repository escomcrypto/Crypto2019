import base64
import os
import app.views

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

from django.shortcuts import render,redirect
from django.conf import settings
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.http import HttpRequest
from django.views.generic import View

from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from django.shortcuts import render

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath("views.py")))

pnt_login_required = user_passes_test(lambda u: True if (not(u.is_superuser) and u.is_staff and u.is_active) else False, login_url='/')

def paintor_login_required(view_func):
    decorated_view_func = login_required(pnt_login_required(view_func), login_url='/')
    return decorated_view_func

# Create your views here.

class WelcomePainter(View):
    template_name='mainPainter.html'
    context_object_name='Welcome'

    def get(self, request, format=None):
        return render(request,
            self.template_name,
            {
                'title':self.context_object_name,
                'year':datetime.now().year,
            })

class OrdersPainter(View):
    template_name='ordersPainter.html'
    context_object_name='Orders'

    def get(self, request, format=None):
        orders = PaintingRequest.objects.filter(status="C").values()
        #orders_set = PaintingRequest.objects.filter().only('id','username')
        #for order in orders_set:
            #order_username = order.username
            #order_id = order.id
            #if not(verifying_process(order_username, order_id)):
                #orders = orders.exclude(id=order_id)
        return render(request, 
            self.template_name, 
            {
                'result':orders,
                'title':self.context_object_name,
                'year':datetime.now().year,
            })

class NewDeliver(View):
    template_name='newDeliver.html'
    context_object_name='New Deliver'

    def get(self, request, format=None):
        orderid=request.GET.get("orderid")
        order=PaintingRequest.objects.filter(id=orderid).values()
        delivery = order[0]["dateRequest"].date() + timedelta(days=30)

        return render(request,self.template_name,
            {
            'order':order,
            'title':self.context_object_name,
            'year':datetime.now().year,
            'delivery':delivery
            })

    def post(self, request, format=None):
        orderid=request.POST.get("orderid")
        print("Valor:",orderid)
        order = PaintingRequest.objects.get(id=orderid)
        order.status="D"
        order.imageD=request.FILES["image"]
        order.dateDelivery=datetime.now().date()
        order.save()
        return redirect("painter:ordersPainter")
        
class DeliversPainter(View):
    template_name='deliversPainter.html'
    context_object_name='Delivers'

    def get(self, request, format=None):
        orders = PaintingRequest.objects.filter(status="D").values()
        return render(request, 
            self.template_name, 
            {
                'result':orders,
                'title':self.context_object_name,
                'year':datetime.now().year,
            })

class DownloadImage(View):
    def get(self, request, format=None):
        order_id = request.GET.get('orderid')
        #response = HttpResponse(content_type='text/plain')

        order = PaintingRequest.objects.get(id=int(order_id))
        name = str(order.image.name)
        extension = name[(name.rfind('.')+1):]

        original_image = decrypt_image(order_id, extension, "originals")
        response = HttpResponse(original_image, content_type='image/'+extension)
        response['Content-Disposition'] = 'attachment; filename=%s' % name[(name.rfind('/')+1):]

        return response

class ViewOrder(View):
    context_object_name="View Deliver"
    template_name="view.html"

    def get(self, request, format=None):
        order_id = request.GET.get('orderid')
        order = PaintingRequest.objects.get(id=int(order_id))
        name = str(order.image.name)
        nameD = str(order.imageD.name)
        extension = name[(name.rfind('.')+1):]
        extensionD = nameD[(name.rfind('.')+1):]
        original_image = decrypt_image(order_id, extension, "originals")
        portrait_image = decrypt_image(order_id, extension, "portraits")
        return render(request, 
            self.template_name, 
            {
                'title':self.context_object_name,
                'year':datetime.now().year,
            })


def getOrder(dateTime,request):
    order = PaintingRequest.objects.filter(dateRequest=dateTime, username=request.user.username).values()
    encrypt_image(order[0]["id"], BASE_DIR+"\\CryptoProject\\app\\static\\images\\"+order[0]["image"].replace("/","\\"))
    #delete the original image after encryption
    os.remove(BASE_DIR+"\\CryptoProject\\app\\static\\images\\"+order[0]["image"].replace("/","\\"))
    #signing_process(order[0]["username"],order[0]["id"])

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

def encrypt_image(id, image_file_name):
    """encrypt and store the client photo"""
    image_bytes = get_image_bytes(image_file_name)
    key = readBinFile(BASE_DIR + '\\CryptoProject\\keys\\orders\\' + str(id) + '_key.bin')
    iv = readBinFile(BASE_DIR + '\\CryptoProject\\keys\\orders\\' + str(id) + '_iv.bin')
    
    #build an AES cipher using OFB mode
    cipher = AES.new(key, AES.MODE_OFB, iv)
    #encrypt the images bytes
    cipher_image_bytes = cipher.encrypt(image_bytes)
    writeBinFile(cipher_image_bytes, BASE_DIR + '\\CryptoProject\\app\\static\\images\\portraits\\' + str(id) + '.bin')

def get_image_bytes(image_file_name):
    """get the bytes of an image file in base64"""
    image_file = open(image_file_name,'rb')
    image_bytes = image_file.read()
    return image_bytes

def decrypt_image(id, extension, directory):
    """read and decrypt the client photo"""
    cipher_image = readBinFile(BASE_DIR + '\\CryptoProject\\app\\static\\images\\'+directory+'\\' + str(id) + '.bin')
    key = readBinFile(BASE_DIR + '\\CryptoProject\\keys\\orders\\' + str(id) + '_key.bin')
    iv = readBinFile(BASE_DIR + '\\CryptoProject\\keys\\orders\\' + str(id) + '_iv.bin')
    
    #build an AES cipher using OFB mode
    cipher = AES.new(key, AES.MODE_OFB, iv)
    #decrypt the cipher images bytes
    plain_image_bytes = cipher.decrypt(cipher_image)
    return plain_image_bytes
     #build_image(BASE_DIR + '\\CryptoProject\\app\\static\\images\\originals\\' + str(id) + '_decrypted.'+ extension, plain_image_bytes)
