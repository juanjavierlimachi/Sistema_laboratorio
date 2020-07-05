from django.contrib import admin
from django.urls import path
from sistema_laboratorio.app.cliente import views
from django.conf.urls import url
from . import views
urlpatterns = [
#Elememtos
	path('LitarElementos/',views.LitarElementos, name='list-element'),
	path('CrearElemento',views.CrearElemento),
	path('update-elemento/<int:id_elemento>',views.updateElemento),
	path('restore-elemento/<int:id_elemento>',views.restoreElemento),
#Productos
	path('update-product/<int:id_producto>/',views.UpdateProduct),
	path('RegisterNewProductAndResult/<int:id>/',views.RegisterNewProductAndResult),
	path('restore-producto/<int:id_producto>',views.RestoreProduct),
#clientes
	path('RegistrarCli',views.RegistrarCli),
	path('update-client/<int:id_cliente>/',views.updateClient),
	path('NewPersona',views.NewPersona),
	path('DetalleCliente/<int:id>/',views.DetalleCliente),
#resultados
	path('RegisterResultados/<int:id_producto>/',views.RegisterResultados),
	path('delite-result/<int:id_result>/',views.deleteResult),
#reportes
	path('detailReport',views.detailReport),
	path('print-certify/<int:ingreso_id>/',views.printCertify),
	url(r'^print-report-general/(?P<clients_id>\d+)/(?P<fecha_inicio>[^/]+)/(?P<fecha_fin>[^/]+)/$',views.printReportGeneral),
	url(r'^print-report-total/(?P<clients_id>\d+)/(?P<fecha_inicio>[^/]+)/(?P<fecha_fin>[^/]+)/$',views.printReportTotal),
	#Under Review
	url(r'^report-analisis/(?P<idProductos>[^/]+)/',views.ReportAnalisis.as_view(), name='reporteAnalisis'),
	url(r'^report-general/(?P<clients_id>\d+)/(?P<fecha_inicio>[^/]+)/(?P<fecha_fin>[^/]+)/$',views.reportGeneral),
#ingresos
	path('detalle-ingreso-cliente/<int:ingreso_id>/',views.DetalleIngresoCliente),
	path('new-producto-a-ingreso/<int:ingreso_id>/',views.NewProductIngreso),
	
	path('search-code',views.searchCode),
]