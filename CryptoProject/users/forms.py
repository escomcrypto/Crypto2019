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
                                'class': 'input is-info',
                                'placeholder': 'Username',
                                }))
 
    password = forms.CharField(label='',
                               required=True,
                               widget=forms.PasswordInput({
                                    'id': 'signinPwd',
                                'type': 'password',
                                'class': 'input is-info',
                                'placeholder': 'Password',
                                    }))

class RegistrationForm(forms.Form):
    email = forms.CharField(max_length=80,
                            label='',
                            required=True,
                            widget=forms.EmailInput({
                                'id': 'signupId',
                                'type': 'email',
                                'class': 'input is-info',
                                'placeholder': 'Email',
                                }))

    password = forms.CharField(label='',
                               required=True,
                               widget=forms.PasswordInput({
                                    'id': 'signupPwd',
                                'type': 'password',
                                'class': 'input is-info',
                                'placeholder': 'Password',
                                    }))

    username = forms.CharField(label='',
            required=True,
            widget=forms.TextInput({
                'id': 'signupUsr',
                                'type': 'text',
                                'class': 'input is-info',
                                'placeholder': 'What\'s your name?',
                }))

    phone = forms.CharField(max_length=80,
                            label='',
                            required=True,
                            widget=forms.TextInput({
                                'id': 'phoneId',
                                'type': 'tel',
                                'pattern': '+[0-9]{12}',
                                'class': 'input is-info',
                                'placeholder': 'Phone Number',
                                }))

class VerifyRCodeForm():
    code = forms.CharField(max_length=80,
                            label='',
                            required=True,
                            widget=forms.TextInput({
                                'id': 'codeId',
                                'type': 'number',
                                'class': 'form-registration-input',
                                'placeholder': 'Insert your code',
                                }))



