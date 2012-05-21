from django import forms


class SellBookForm(forms.Form):
    isbn = forms.CharField(required=True, label="Enter the ISBN:", max_length=25, min_length=10)
    email = forms.EmailField(required=True, label="Enter your email:")
    price = forms.IntegerField(required=True, label="Enter your price:")

    CONDITION_CHOICES = (
        ('new', 'New'), 
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor')
    )
    condition = forms.ChoiceField(choices=CONDITION_CHOICES, required=True)

    def clean_isbn(self):
       isbn = self.cleaned_data['isbn']
       isbn = isbn.strip('-')
       if len(isbn) < 10 or len(isbn) > 13:
           raise forms.ValidationError("Not a valid ISBN.")
       return isbn

class ContactSellerForm(forms.Form):
    email = forms.EmailField(required=True, label="Enter your email:")
    message = forms.CharField (widget=forms.widgets.Textarea(),  label='Send a message to the seller:')
    
