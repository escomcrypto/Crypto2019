"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _

class LoginAuthenticationForm(forms.Form):
    email = forms.CharField(max_length=80,
                            label='',
                            required=True,
                            widget=forms.EmailInput({
                                'id': 'email',
                                'type': 'email',
                                'class': 'form-registration-input',
                                'placeholder': 'Email',
                                }))

    password = forms.CharField(label='',
                               required=True,
                               widget=forms.PasswordInput({
                                    'id': 'password',
                                'type': 'password',
                                'class': 'form-registration-input',
                                'placeholder': 'Password',
                                'aria-describedby': "passwordField",
                                'required': 'True',
                                    }))
