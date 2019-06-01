import base64
import os
import app.views
import random
 
from app.views import encrypt_image, decrypt_image

from io import BytesIO

from app.models import PaintingRequest

from datetime import timedelta,datetime

from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

from django.shortcuts import render,redirect
from django.conf import settings
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views.generic import View
from django.contrib import messages

from django.contrib.auth import decorators
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, user_passes_test

from django.contrib.auth import logout

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath("views.py")))

pnt_login_required = user_passes_test(lambda u: True if (not(u.is_superuser) and u.is_staff and u.is_active) else False, login_url='/')

"""===================================="""
"""Roles and Permissions CBV decorators"""
"""===================================="""
def paintor_login_required(view_func):
    decorated_view_func = login_required(pnt_login_required(view_func), login_url='/')
    return decorated_view_func

def cbv_decorator(decorator):
    """
    Turns a normal view decorator into a class-based-view decorator.
    
    Usage:
    
    @cbv_decorator(login_required)
    class MyClassBasedView(View):
        pass
    """
    def _decorator(cls):
        cls.dispatch = method_decorator(decorator)(cls.dispatch)
        return cls
    return _decorator

# Create your views here.

@cbv_decorator(paintor_login_required)
class LogoutView(View):
    def get(self, request, format=None):
        logout(request)
        return HttpResponseRedirect('/')

@cbv_decorator(paintor_login_required)
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

@cbv_decorator(paintor_login_required)
class OrdersPainter(View):
    template_name='ordersPainter.html'
    context_object_name='Orders'

    def get(self, request, format=None):
        orders = PaintingRequest.objects.filter(status="C").values()
        return render(request, 
            self.template_name, 
            {
                'result':orders,
                'title':self.context_object_name,
                'year':datetime.now().year,
            })

@cbv_decorator(paintor_login_required)
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
        order.signatureP = request.POST["signature"]
        order.imageD=request.FILES["image"]
        order.dateDelivery=datetime.now().date()
        order.save()
        getOrder(order.id)
        if(verify_signature(order)):
            order.status="D"
            order.save()
            messages.success(request,'Your delivery has been sent successfully.')
        else:
            messages.error(request,'The verification has failed: delivery not valid')
        return redirect("painter:deliversPainter")

@cbv_decorator(paintor_login_required)  
class DeliversPainter(View):
    template_name='deliversPainter.html'
    context_object_name='Deliveries'

    def get(self, request, format=None):
        orders = PaintingRequest.objects.filter(status="D").values()
        return render(request, 
            self.template_name, 
            {
                'result':orders,
                'title':self.context_object_name,
                'year':datetime.now().year,
            })

@cbv_decorator(paintor_login_required)
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

@cbv_decorator(paintor_login_required)
class ViewOrder(View):
    context_object_name="View Deliver"
    template_name="viewOrder.html"

    def get(self, request, format=None):
        order_id = request.GET.get('orderid')
        order = PaintingRequest.objects.get(id=int(order_id))
        name = str(order.image.name)
        nameD = str(order.imageD.name)
        extension = name[(name.rfind('.')+1):]
        extensionD = nameD[(name.rfind('.')+1):]
        original_image = decrypt_image(order_id, extension, "originals")
        original=base64.b64encode(original_image).decode()
        portrait_image = decrypt_image(order_id, extension, "portraits")
        portrait=base64.b64encode(portrait_image).decode()
        return render(request, 
            self.template_name, 
            {
                'mime':extension,
                'original':original,
                'mime2':extensionD,
                'portrait':portrait,
                'title':self.context_object_name,
                'year':datetime.now().year,
            })

def base64_2_bytes(base64string):
    """Decode base64 string to bytes object"""
    return base64.b64decode(base64string)

def verify_signature(order):
    """verifying"""
    public_key = RSA.import_key(open(BASE_DIR+'\\CryptoProject\\keys\\users\\'+'Salvador Dali'+'_public.pem').read())
    signature = base64_2_bytes(order.signatureP)

    name = str(order.imageD.name)
    extension = name[(name.rfind('.')+1):]
    deliver_image = decrypt_image(order.id, extension, "portraits")

    h = SHA256.new(deliver_image)
    try:
        pkcs1_15.new(public_key).verify(h, signature)
        return True
    except (ValueError, TypeError):
        return False

def getOrder(orderid):
    order = PaintingRequest.objects.filter(id=orderid).values()
    encrypt_image(order[0]["id"], BASE_DIR+"\\CryptoProject\\app\\static\\images\\"+order[0]["imageD"].replace("/","\\"),"portraits")
    #delete the original image after encryption
    os.remove(BASE_DIR+"\\CryptoProject\\app\\static\\images\\"+order[0]["imageD"].replace("/","\\"))