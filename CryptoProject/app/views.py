"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpRequest

from .forms import LoginAuthenticationForm

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
      """Renders the register page """
      assert isinstance(request, HttpRequest)
      return render(request,
          'app/signup.html',
          {
              'title':'Sign Up - Art',
              'year':datetime.now().year,
          })

 def forgotpwd(request):
     """Renders the recover password page """
     assert isisinstance(request, HttpRequest)
     return render(request,
                   'app/')

#def contact(request):
#    """Renders the contact page."""
#    assert isinstance(request, HttpRequest)
#    return render(
#        request,
#        'app/contact.html',
#        {
#            'title':'Contact',
#            'message':'Your contact page.',
#            'year':datetime.now().year,
#        }
#    )

#def about(request):
#    """Renders the about page."""
#    assert isinstance(request, HttpRequest)
#    return render(
#        request,
#        'app/about.html',
#        {
#            'title':'About',
#            'message':'Your application description page.',
#            'year':datetime.now().year,
#        }
#    )
