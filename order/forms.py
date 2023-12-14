from django import forms

class CheckoutForm(forms.Form):
    address = forms.IntegerField()  # Adjust this field based on your model or requirements
    checkout_payment_method = forms.ChoiceField(choices=[("1", "Payment Method 1"), ("2", "Payment Method 2")])


