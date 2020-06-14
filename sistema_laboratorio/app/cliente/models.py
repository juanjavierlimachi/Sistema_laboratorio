from django.db import models
from django.contrib.auth.forms import User
# Create your models here.
class Cliente(models.Model):
	Nombre=models.CharField(max_length=150)
	Direccion =models.CharField(max_length=100)
	Telefono = models.PositiveIntegerField(blank=True, null=True, help_text="Opcional")
	Nit = models.PositiveIntegerField(blank=True, null=True,help_text="Opcional")
	Particular = models.BooleanField()
	estado=models.BooleanField(default=True)
	fecha_registro = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return self.Nombre

class Elemento(models.Model):
	Nombre_del_Elemento = models.CharField(max_length=100, unique=True)
	Abreviatura = models.CharField(max_length=100, unique=True)
	estado=models.BooleanField(default=True, help_text="Desactive esta casilla para dar de baja este elemento")
	fecha_registro = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return self.Nombre_del_Elemento

class Producto(models.Model):
	Lote = models.CharField(max_length=150)
	Cliente = models.ForeignKey(Cliente, on_delete = models.CASCADE)	
	Usuario=models.ForeignKey(User,on_delete = models.CASCADE)
	estado=models.BooleanField(default=True)
	fecha_registro = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return self.Lote

class Precio(models.Model):
	Precio = models.FloatField()
	Cliente = models.ForeignKey(Cliente, on_delete = models.CASCADE)
	Elemento = models.ForeignKey(Elemento, on_delete = models.CASCADE)
	estado=models.BooleanField(default=True)
	fecha_registro = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return self.Cliente.Nombre

class Resultado(models.Model):
	Resultado=models.FloatField(help_text="Engrese el resultado Ejem. 2.25")
	Elemento = models.ForeignKey(Elemento, on_delete = models.CASCADE)
	producto=models.ForeignKey(Producto,on_delete = models.CASCADE)
	estado=models.BooleanField(default=True)
	fecha_registro = models.DateTimeField(auto_now_add=True)
	def __unicode__(self):
		return self.producto.Lote