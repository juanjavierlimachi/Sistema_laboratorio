#encoding:utf-8
from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import User
from sistema_laboratorio.app.cliente.models import *


class FormCliente(ModelForm):
	class Meta():
		model = Cliente
		exclude=('estado',)


class FormProducto(ModelForm):
	class Meta():
		model = Producto
		exclude=('estado','Usuario','Cliente','codigo_ingreso')


class FormProductoUpdate(ModelForm):
	class Meta():
		model = Producto
		exclude=('Usuario','Cliente')


class FormElemento(forms.ModelForm):
	class Meta():
		model = Elemento
		exclude=('estado',)


class FormElementoUdate(forms.ModelForm):
	class Meta():
		model = Elemento
		fields=('Nombre_del_Elemento','Abreviatura','estado',)

class FormResultado(ModelForm):
	class Meta():
		model = Resultado
		exclude=('estado','producto')
	def __init__(self, *args, **kwargs):
		super(FormResultado, self).__init__(*args, **kwargs)
		self.fields['Elemento'].queryset = Elemento.objects.filter(estado=True)