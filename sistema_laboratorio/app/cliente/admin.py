from django.contrib import admin
from sistema_laboratorio.app.cliente.models import *
# Register your models here.
admin.site.register(Cliente)
admin.site.register(Elemento)
admin.site.register(Producto)
admin.site.register(Resultado)