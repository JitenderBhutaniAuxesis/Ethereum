from django.contrib.auth.models import User
from django import forms
from .models import Transaction


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username','password']


class TransactionForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = Transaction
        fields = ['from_address','to_address','amount','password']