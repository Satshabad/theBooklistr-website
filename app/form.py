from django import forms


class SellBookForm(forms.Form):
  isbn = forms.CharField()
  email = forms.EmailField()
