import base64
import os
import app.views
import random
 
from app.views import encrypt_image, decrypt_image

from io import BytesIO

from app.models import PaintingRequest

from datetime import timedelta,datetime

from django.shortcuts import render,redirect
from django.conf import settings
from django.http import HttpResponse
from django.views.generic import View
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test

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
        getOrder(order.id)
        messages.add_message(request, messages.SUCCESS,'The painting has been successfully.')
        return redirect("painter:deliversPainter")
        
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


def getOrder(orderid):
    order = PaintingRequest.objects.filter(id=orderid).values()
    encrypt_image(order[0]["id"], BASE_DIR+"\\CryptoProject\\app\\static\\images\\"+order[0]["imageD"].replace("/","\\"),"portraits")
    #delete the original image after encryption
    os.remove(BASE_DIR+"\\CryptoProject\\app\\static\\images\\"+order[0]["imageD"].replace("/","\\"))
    #signing_process(order[0]["username"],order[0]["id"])