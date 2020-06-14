from django.contrib import admin
from django.urls import path
from sistema_laboratorio.app.cliente import views

urlpatterns = [
#Elememtos
	path('LitarElementos/',views.LitarElementos, name='list-element'),
	path('CrearElemento',views.CrearElemento),
	path('update-elemento/<int:id_elemento>',views.updateElemento),
	path('restore-elemento/<int:id_elemento>',views.restoreElemento),
#Productos

	path('RegisterNewProductAndResult/<int:id>/',views.RegisterNewProductAndResult),
#clientes
	path('RegistrarCli',views.RegistrarCli),
	path('update-client/<int:id_cliente>/',views.updateClient),
	path('NewPersona',views.NewPersona),
	path('DetalleCliente/<int:id>/',views.DetalleCliente),
	path('Detalle_persona',views.Detalle_persona),
#resultados
	path('RegisterResultados/<int:id_producto>/',views.RegisterResultados),
	path('delite-result/<int:id_result>/',views.deleteResult),
]