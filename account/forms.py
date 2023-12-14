from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.core.exceptions import ValidationError

from account.models import Address
from .models import CustomUser

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
        fields = ['name', 'city', 'street', 'building', 'zip', 'note']


class NewUserForm(UserCreationForm):
	email = forms.CharField(max_length=100, required=False)

	class Meta:
		model = User
		fields = ("username", "first_name", "name", "telephone", "password1", "email", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		if commit:
			user.save()
		print("User saved:", user)
		return user



class RegistrationForm(forms.Form):
    username = forms.CharField(label='VÖEN', min_length=4, max_length=150)
    email = forms.EmailField(label='Email address')
    first_name = forms.CharField(label='First Name', max_length=150)
    telephone = forms.CharField(label='Telephone', max_length=20)
    name = forms.CharField(label='Şirkətin adı', max_length=150) 
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        if CustomUser.objects.filter(username=username).exists():
            raise ValidationError("Username already exists")
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        existing_user = CustomUser.objects.filter(email=email).first()

        if existing_user and existing_user.just_registered:
            raise ValidationError("A user with this email is already pending approval.")
        elif existing_user and not existing_user.just_registered:
            raise ValidationError("Email already exists")

        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")

        return password2

    def save(self, commit=True):
        user = CustomUser.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            first_name=self.cleaned_data['first_name'],
            telephone=self.cleaned_data['telephone'],
            name = self.cleaned_data['name'],
            password=self.cleaned_data['password1'],
            just_registered=True,
        )
        return user
    





