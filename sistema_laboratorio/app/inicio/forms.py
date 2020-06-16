#encoding:utf-8
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import *
from .forms import *
from django.contrib.auth.forms import User
class UserForm(UserCreationForm):
	username = forms.CharField(max_length=40,help_text="Nombre de usuario (No deve contener espacios) *",label="Nombre de Usuario")
	password1 = forms.CharField(help_text="Recuerde este dato para proporcionar al personal *", label="Contraseña")
	password2 = forms.CharField(help_text="Confirme la contraseña anterior *", label="Confirmar")
	first_name = forms.CharField(max_length=140, label="Nombre y Apellido *")
	email = forms.EmailField(label='Correo Elec.')

	class Meta:
		model=User
		fields=("username","password1","password2","first_name","email")
		widgets = {
			'password1':forms.PasswordInput(),
		}
	def save(self,commit=True):
		user=super(UserForm,self).save(commit=False)
		user.first_name=self.cleaned_data.get("first_name")
		if commit:
			user.is_active = True
			user.is_staff = True
			user.is_superuser = False
			user.save()
		return user


class UserForms(forms.ModelForm):
	class Meta:
		model=User
		fields = ('username','first_name')


class ChangePasswordForm(forms.Form):
	old_password = forms.CharField(max_length=40,label="Antigua Contraseña")
	new_password = forms.CharField(max_length=40,label="Nueva Contraseña")
	confirm_password = forms.CharField(max_length=40,label="Repetir Contraseña")