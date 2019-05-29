from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.http import HttpRequest

from django.views.generic import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

import nexmo

from .forms import *
from .models import TwoFactor

# Create your views here.
class LoginView(View):
    template_name = 'app/signin.html'
    context_object_name = 'Sign In - Art'
    form = LoginAuthenticationForm()

    def get(self, request, format=None):
        """Renders the login."""
        assert isinstance(request, HttpRequest)
        return render(request,
            self.template_name,
            {
                'title':self.context_object_name,
                'form':self.form
            })

    def post(self, request, format=None):
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
                    if user.is_staff:
                        return HttpResponseRedirect('welcomePainter')
                    else:
                        return HttpResponseRedirect('welcome')
            else:
                return HttpResponse('User is None')
        else:
            return HttpResponse('Form not valid')

        return render(request,
            self.template_name,
            {
                'title':self.context_object_name,
                'form':self.form
            })

class RegisterView(View):
    template_name = 'app/signup.html'
    context_object_name = 'Sign Up - Art'
    form = RegistrationForm()

    def get(self, request, format=None):
        """Renders the register page."""
        assert isinstance(request, HttpRequest)
        return render(request,
            self.template_name,
            {
                'title':self.context_object_name,
                'form':self.form
            })

    def post(self, request, format=None):
        # Create a form instance and populated with data from request:
        authentication_form = RegistrationForm(request.POST)

        # Check whether it's valid:
        if authentication_form.is_valid():
            email = request.POST.get('email')
            email_confirmation = request.POST.get('email_confirmation')
            username = request.POST.get('username')
            password = request.POST.get('password')
            phone = request.POST.get('phone')

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

                    two_factor = TwoFactor.objects.create(user=new_user)

                    if(not two_factor.number):
                        two_factor.number = phone
                        two_factor.save()

                    number = two_factor.number
                    response = self.send_verification_request(request, number)

                    if (response['status'] == '0'):
                        request.session['verification_id'] = response['request_id']
                        request.session['user'] = new_user.id
                        request.session['two_factor'] = two_factor.id
                        return HttpResponseRedirect('verifyrcode')

                    else:
                        two_factor.delete()
                        new_user.delete()
                        messages.add_message(request, messages.INFO, 'Could not verify your number. Please contact support.')
                        return HttpResponseRedirect('/')

        return render(request,
                self.template_name,
                {
                    'title':self.context_object_name,
                    'form':self.form
                })

    def send_verification_request(self, request, number):
        client = nexmo.Client(key='c459213a', secret='SbP5REYo5vwhxdOD')
        return client.start_verification(number=number, brand='CryptoProject')

class CodeVerifyRView(View):
    template_name = 'app/verifyrcode.html'
    context_object_name = 'Send Code'
    form = VerifyRCodeForm()

    def get(self, request, format=None):
        """Renders the register page."""
        assert isinstance(request, HttpRequest)
        return render(request,
            self.template_name,
            {
                'title':self.context_object_name,
                'form':self.form
            })

    def post(self, request, format=None):
        response = self.check_verification_request(request)
 
        if (response['status'] == '0'):
            request.session['verified'] = True
            return HttpResponseRedirect('login')
        else:
            TwoFactor.objects.filter(id=request.session['two_factor']).delete()
            User.objects.filter(id=request.session['user']).delete()
            messages.add_message(request, messages.INFO, 'Could not verify code. Please try again.')
            return HttpResponseRedirect('/')
 
 
    def check_verification_request(self, request):
        client = nexmo.Client(key='c459213a', secret='SbP5REYo5vwhxdOD')
        return client.check_verification(request.session['verification_id'], code=request.POST.get('code'))

def handler404(request, exception, template_name="404.html"):
    response = render_to_response("404.html")
    response.status_code = 404
    return response

def handler404(request, exception, template_name="500.html"):
    response = render_to_response("500.html")
    response.status_code = 500
    return response