from django.db import models
from django.contrib.auth.forms import User
from datetime import date
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

class Codigo(models.Model):
	cliente = models.ForeignKey(Cliente, on_delete = models.CASCADE)
	usuario = models.ForeignKey(User, on_delete = models.CASCADE)
	estado=models.BooleanField(default=True)
	fecha_update = models.DateTimeField(auto_now=True)
	fecha_registro = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return "%s"%(self.cliente.Nombre)

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
	codigo_ingreso = models.ForeignKey(Codigo, on_delete = models.CASCADE,blank=True, null=True)
	estado=models.BooleanField(default=True, help_text="Desactive esta casilla para dar de baja este producto")
	fecha = models.DateField(default=date.today)
	fecha_registro = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return self.Lote

class Precio(models.Model):
	Cliente = models.OneToOneField(Cliente, on_delete = models.CASCADE)
	Zinc=models.FloatField()
	Plata=models.FloatField()
	Plomo=models.FloatField()
	Estanio=models.FloatField()
	Cobre=models.FloatField()
	H2O=models.FloatField()
	Antimonio=models.FloatField()
	Arsenico=models.FloatField()
	Hierro=models.FloatField()
	estado=models.BooleanField(default=True)
	fecha_registro = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return self.Cliente.Nombre

class Resultado(models.Model):
	Zinc=models.FloatField(blank=True, null=True)
	Plata=models.FloatField(blank=True, null=True)
	Plomo=models.FloatField(blank=True, null=True)
	Estanio=models.FloatField(blank=True, null=True)
	Cobre=models.FloatField(blank=True, null=True)
	H2O=models.FloatField(blank=True, null=True)
	Antimonio=models.FloatField(blank=True, null=True)
	Arsenico=models.FloatField(blank=True, null=True)
	Hierro=models.FloatField(blank=True, null=True)
	producto=models.ForeignKey(Producto,on_delete = models.CASCADE)
	estado=models.BooleanField(default=True)
	fecha_registro = models.DateTimeField(auto_now_add=True)
	def __unicode__(self):
		return self.producto.Lote