from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpRequest
from app.models import PaintingRequest

from .forms import LoginAuthenticationForm, RegistrationForm

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
    if request.method=="POST":
        var = PaintingRequest(
        nameRequest=request.POST["nameRequest"],
        username="mayrasho",
        dateRequest=datetime.now().date(),
        description=request.POST["description"],
        image=request.FILES["image"],
        status='O',
        )
        var.save()
    print (request.FILES)
    return render(request,'app/newOrder.html',
        {
        'title':'New Request',
        'year':datetime.now().year,
        }
    )

def welcome(request):
    return render(request,'app/mainClient.html',
        {
        'title':'welcome',
        'year':datetime.now().year,
        }
    )