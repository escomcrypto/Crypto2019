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
from django.views.generic import View
from django.contrib.auth.decorators import login_required, user_passes_test

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath("views.py")))

# Client role tag
clt_login_required = user_passes_test(lambda u: True if (not(u.is_superuser) and not(u.is_staff) and u.is_active) else False, login_url='/')

def client_login_required(view_func):
    decorated_view_func = login_required(clt_login_required(view_func), login_url='/')
    return decorated_view_func

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

class NewOrder(View):
    template_name='newOrder.html'
    context_object_name='New Order'
    def get(self, request, format=None):
        return render(request,self.template_name,
        {
        'title':self.context_object_name,
        'year':datetime.now().year,
        })

    def post(self, request, fromat=None):
        dt = datetime.now()
        var = PaintingRequest(nameRequest=request.POST["nameRequest"],
            username=request.user.username,
            dateRequest=dt,
            description=request.POST["description"],
            image=request.FILES["image"],
            status='C',
            cost=random.randint(150,250),
            dateDelivery=dt.date() + timedelta(days=30)
            )
        var.save()
        getOrder(dt,request)
        return redirect("client:ordersList")

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
    #signing_process(order[0]["username"],order[0]["id"])

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