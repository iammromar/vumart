from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from account.models import Address

User = get_user_model()

from django.contrib.auth.forms import SetPasswordForm

class SetPasswordForm(SetPasswordForm):
    class Meta:
        model = User
        fields = ['new_password1', 'new_password2']
# Create your forms here.


from django import forms


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = "__all__"


class NewUserForm(UserCreationForm):
	email = forms.CharField(max_length=100,required=False)
	class Meta:
		model = User
		fields = ("username", "first_name","name","telephone","password1","email", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		if commit:
			user.save()
		return user