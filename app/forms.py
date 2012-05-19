from django import forms


class SellBookForm(forms.Form):
    isbn = forms.CharField(required=True, label="Enter the ISBN:", max_length=25, min_length=10)
    email = forms.EmailField(required=True, label="Enter your email:")
    price = forms.IntegerField(required=True, label="Enter your price:")
    condition = forms.CharField(required=True, label="Condition of the book:",max_length=15)

    def clean_isbn(self):
       isbn = self.cleaned_data['isbn']
       isbn = isbn.strip('-')
       if len(isbn) < 10 or len(isbn) > 13:
           raise forms.ValidationError("Not a valid ISBN.")
       return isbn
