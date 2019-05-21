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
            orders.append(result[r]['name'])
    else:
        print("No hay pedidos")
    return render(request, 
        'app/requestsClient.html', 
        {
            'orders':orders,
            'title':'Orders',
            'year':datetime.now().year,
        })
