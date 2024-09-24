from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator

class ItemForm(forms.Form):
    itemID = forms.HiddenInput()

class PaymentMethodForm(forms.Form):
    fullname = forms.CharField(label="Full name", max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.CharField(label="Email", max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    address = forms.CharField(label="Address", max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    city = forms.CharField(label="City", max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    state = forms.CharField(label="State", max_length=2)
    zip = forms.IntegerField(label="Zip Code", validators=
                              [MaxValueValidator(99999),
                               MinValueValidator(1)])
    cname = forms.CharField(label="Name on Card")
    ccnum = forms.IntegerField(label="Credit card number")
    expmonth = forms.IntegerField(label="Exp month", min_value=1, max_value=12)
    expyear = forms.IntegerField(label="Exp year", min_value=0, max_value=99)
    cvv = forms.IntegerField(label="CVV (security code)")

class SupportTicketForm(forms.Form):
    title = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    message = forms.CharField(max_length=10000, widget=forms.Textarea(attrs={'class': 'form-control'}))