import base64
import os
import random

from io import BytesIO

from app.models import PaintingRequest

from datetime import timedelta,datetime

from app.views import encrypt_image, generate_iv, generate_key, decrypt_image

from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle
from reportlab.platypus import Table
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views.generic import View
from django.contrib import messages

from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

from django.contrib.auth import decorators
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, user_passes_test

from django.contrib.auth import logout

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath("views.py")))

"""===================================="""
"""Roles and Permissions CBV decorators"""
"""===================================="""
# Client role tag
clt_login_required = user_passes_test(lambda u: True if (not(u.is_superuser) and not(u.is_staff) and u.is_active) else False, login_url='/')

def client_login_required(view_func):
    decorated_view_func = login_required(clt_login_required(view_func), login_url='/')
    return decorated_view_func

from django.utils.decorators import method_decorator

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

@cbv_decorator(client_login_required)
class LogoutView(View):
    def get(self, request, format=None):
        logout(request)
        return HttpResponseRedirect('/')

@cbv_decorator(client_login_required)
class Welcome(View):
    template_name='mainClient.html'
    context_object_name='Welcome'

    def get(self, request, format=None):
        return render(request,
            self.template_name,
            {
                'title':self.context_object_name,
                'year':datetime.now().year,
            })

#@cbv_decorator(client_login_required)
class GenerateKeys(View):
    template_name='generateKeysClient.html'
    context_object_name='Keys Generation'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(GenerateKeys, self).dispatch(request, *args, **kwargs)

    def get(self, request, format=None):
        return render(request,
            self.template_name,
            {
                'title':self.context_object_name,
                'year':datetime.now().year,
            })

    def post(self, request, format=None):
        key = request.POST["publickey"]
        public_key = str.encode(key)
        pubkey_file = open(BASE_DIR+'\\CryptoProject\\keys\\users\\'+request.user.username+'_public.pem', 'wb')
        pubkey_file.write(public_key)
        return HttpResponse(request.user.username)

@cbv_decorator(client_login_required)
class OrdersList(View):
    template_name='requestsClient.html'
    context_object_name='Orders'
    def get(self, request, format=None):
        result = PaintingRequest.objects.filter(username=request.user.username, status="C").values()
        return render(request, 
            self.template_name, 
            {
                'result':result,
                'title':self.context_object_name,
                'year':datetime.now().year,
            })

@cbv_decorator(client_login_required)
class DeliversClient(View):
    template_name='deliversClient.html'
    context_object_name='Delivers'
    def get(self, request, format=None):
        result = PaintingRequest.objects.filter(username=request.user.username, status="D").values()
        return render(request, 
            self.template_name, 
            {
                'result':result,
                'title':self.context_object_name,
                'year':datetime.now().year,
            })

@cbv_decorator(client_login_required)
class NewOrder(View):
    template_name='newOrder.html'
    context_object_name='New Order'
    def get(self, request, format=None):
        return render(request,self.template_name,
        {
        'title':self.context_object_name,
        'year':datetime.now().year,
        })

    def post(self, request, format=None):
        dt = datetime.now()
        var = PaintingRequest(nameRequest=request.POST["nameRequest"],
            username=request.user.username,
            dateRequest=dt,
            description=request.POST["description"],
            image=request.FILES["image"],
            signature=request.POST["signature"],
            status='C',
            cost=random.randint(150,250),
            dateDelivery=dt.date() + timedelta(days=30)
            )
        var.save()
        getOrder(dt,request)

        if(verify_signature(var)):
            messages.success(request,'Your order has been sent successfully.')
        else:
            var.delete()
            messages.error(request,'The verification has failed: order not valid')
        return redirect("client:ordersList")

@cbv_decorator(client_login_required)
class DownloadImage(View):
    def get(self, request, format=None):
        order_id = request.GET.get('orderid')

        order = PaintingRequest.objects.get(id=int(order_id))
        nameD = str(order.imageD.name)
        extension = nameD[(nameD.rfind('.')+1):]

        portrait_image = decrypt_image(order_id, extension, "portraits")
        response = HttpResponse(portrait_image, content_type='image/'+extension)
        response['Content-Disposition'] = 'attachment; filename=%s' % nameD[(nameD.rfind('/')+1):]

        return response

@cbv_decorator(client_login_required)
class ViewOrderC(View):
    context_object_name="View Deliver"
    template_name="viewOrderC.html"

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

"""==============================="""
"""         IMAGE ORDER           """
"""==============================="""

def getOrder(dateTime,request):
    order = PaintingRequest.objects.filter(dateRequest=dateTime, username=request.user.username).values()
    generate_iv(order[0]["id"])
    generate_key(order[0]["id"])
    encrypt_image(order[0]["id"], BASE_DIR+"\\CryptoProject\\app\\static\\images\\"+order[0]["image"].replace("/","\\"),"originals")
    #delete the original image after encryption
    os.remove(BASE_DIR+"\\CryptoProject\\app\\static\\images\\"+order[0]["image"].replace("/","\\"))
    build_order_confirmation(order[0]["id"],order[0]["username"],
    order[0]["nameRequest"],order[0]["description"],order[0]["dateRequest"],
    order[0]["dateDelivery"],order[0]["cost"])

def build_order_confirmation(order_id, user_name, order_name, description, order_date, delivery_date, cost):
    oc = '' #text for the order confirmation
    oc = oc + str(datetime.now().date()) + '\n\n'
    oc = oc + 'Order Numbers: ' + str(order_id) + '\n\n'
    oc = oc + 'Order Details \n'
    oc = oc + '\tOrder Date: ' + str(order_date.date()) + '\n'
    oc = oc + '\tUser: ' + user_name + '\n'
    oc = oc + '\tOrder Name: ' + order_name + '\n'
    oc = oc + '\tDescription: ' + description + '\n\n'
    oc = oc + '\tDelivery Date: ' + str(delivery_date) + '\n\n'
    oc = oc + '\tTotal Cost: $'+ str(cost) + '.00 \n'
    
    order_confirmation_file = open(BASE_DIR+'\\CryptoProject\\app\\static\\orders\\'+str(order_id)+'_OrderConfirmation.txt','w')
    order_confirmation_file.write(oc)

"""==============================="""
"""         PDF Generation        """
"""==============================="""

def generar_orden(request):
    if request.method == 'GET':
        order_id = request.GET.get('orderid')
        username = request.GET.get('username')

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
        pdf.drawString(320, 760, u"Order Confirmation")

        order = open(BASE_DIR + '\\CryptoProject\\app\\static\\orders\\' + str(order_id) + '_OrderConfirmation.txt', "r")
        height = 660
        width = 40
        pdf.setFont("Helvetica-Bold", 12)

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

def base64_2_bytes(base64string):
    """Decode base64 string to bytes object"""
    return base64.b64decode(base64string)

def verify_signature(order):
    """verifying"""
    public_key = RSA.import_key(open(BASE_DIR+'\\CryptoProject\\keys\\users\\'+str(order.username)+'_public.pem').read())
    signature = base64_2_bytes(order.signature)

    name = str(order.image.name)
    extension = name[(name.rfind('.')+1):]
    original_image = decrypt_image(order.id, extension, "originals")

    h = SHA256.new(original_image)
    try:
        pkcs1_15.new(public_key).verify(h, signature)
        return True
    except (ValueError, TypeError):
        return False