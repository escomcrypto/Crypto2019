"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _

class LoginAuthenticationForm(forms.Form):
    username = forms.CharField(max_length=80,
                            label='',
                            required=True,
                            widget=forms.TextInput({
                                'id': 'signinId',
                                'type': 'text',
                                'class': 'form-registration-input',
                                'placeholder': 'Username',
                                }))
 
    password = forms.CharField(label='',
                               required=True,
                               widget=forms.PasswordInput({
                                    'id': 'signinPwd',
                                'type': 'password',
                                'class': 'form-registration-input',
                                'placeholder': 'Password',
                                    }))

class RegistrationForm(forms.Form):
    email = forms.CharField(max_length=80,
                            label='',
                            required=True,
                            widget=forms.EmailInput({
                                'id': 'signupId',
                                'type': 'email',
                                'class': 'form-registration-input',
                                'placeholder': 'Email',
                                }))

    email_confirmation = forms.CharField(max_length=80,
                            label='',
                            required=True,
                            widget=forms.EmailInput({
                                'id': 'signupCId',
                                'type': 'email',
                                'class': 'form-registration-input',
                                'placeholder': 'Email confirmation',
                                }))

    password = forms.CharField(label='',
                               required=True,
                               widget=forms.PasswordInput({
                                    'id': 'signupPwd',
                                'type': 'password',
                                'class': 'form-registration-input',
                                'placeholder': 'Password',
                                    }))

    username = forms.CharField(label='',
            required=True,
            widget=forms.TextInput({
                'id': 'signupUsr',
                                'type': 'text',
                                'class': 'form-registration-input',
                                'placeholder': 'What\'s your name?',
                }))

    phone = forms.CharField(max_length=80,
                            label='',
                            required=True,
                            widget=forms.TextInput({
                                'id': 'phoneId',
                                'type': 'tel',
                                'pattern': '+[0-9]{12}',
                                'class': 'form-registration-input',
                                'placeholder': 'Phone Number',
                                }))

class RPhoneSendForm():
    number = forms.CharField(max_length=80,
                            label='',
                            required=True,
                            widget=forms.TextInput({
                                'id': 'phoneId',
                                'type': 'number',
                                'class': 'form-registration-input',
                                'placeholder': 'Phone Number',
                                }))