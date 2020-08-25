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
		fields=('Lote','fecha',)
		exclude=('Usuario','Cliente','codigo_ingreso')

class FormResultUpdate(ModelForm):
	class Meta():
		model = Resultado
		fields=('Zinc','Plata','Plomo','Estanio','Cobre','H2O','Antimonio','Arsenico','Hierro',)


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
	
class FormPrecio(ModelForm):
	class Meta():
		model = Precio
		exclude=('estado','Cliente')

class FormEmail(forms.Form):
	Descripcion = forms.CharField(required=True, label="Descripción", help_text="Escriba un breve comentario.",widget=forms.Textarea())
	Archivo = forms.FileField(required=True, label="Adjuntar Archivo", help_text="Seleccione un archivo a enviar.")