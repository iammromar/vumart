from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

from django.contrib.auth.forms import SetPasswordForm

class SetPasswordForm(SetPasswordForm):
    class Meta:
        model = User
        fields = ['new_password1', 'new_password2']
# Create your forms here.

class NewUserForm(UserCreationForm):
	email = forms.CharField(max_length=100,required=False)
	class Meta:
		model = User
		fields = ("username", "first_name","last_name","password1","email", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		if commit:
			user.save()
		return user