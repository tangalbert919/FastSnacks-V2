from django import forms

class ItemForm(forms.Form):
    itemID = forms.HiddenInput()
