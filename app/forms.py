from django import forms


class SellBookForm(forms.Form):
    isbn = forms.CharField(required=True, label="Enter the ISBN:")
    email = forms.EmailField(required=True, label="Enter your email:")
    
