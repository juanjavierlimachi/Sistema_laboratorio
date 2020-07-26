from django.shortcuts import render, redirect,HttpResponse,HttpResponseRedirect, get_object_or_404
from sistema_laboratorio.app.cliente.forms import *
import calendar
from datetime import datetime, date, time, timedelta
from django.views.generic import View
from io import StringIO
import os
import io
from xhtml2pdf import pisa
from django.template.loader import render_to_string

#de reporlab
from reportlab.pdfgen import canvas
from django.http import FileResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

# Create your views here.
def RegistrarCli(request):
	datos = Cliente.objects.all().order_by('-id')
	#request.session['id_producto'] = []#CREO UNA VARIABLE DE SESSION
	return render(request, 'cliente/RegistrarCli.html',{'datos':datos})


def NewPersona(request):
	if request.method=='POST':
		forms=FormCliente(request.POST)
		if forms.is_valid():
			datos = forms.save(commit=False)
			datos.id
			datos.save()
			""" 
			request.session['sesion'] = []#CREO UNA VARIABLE DE SESSION
			id_persona = request.session['sesion']
			id_persona.append(cod.id)
			request.session['sesion'] = id_persona """
			return redirect('DetalleCliente/'+str(datos.id)+'/')
	else:
		forms=FormCliente()

	return render(request,'cliente/NewPersona.html',{'forms':forms})

def updateClient(request, id_cliente):
	dato=Cliente.objects.get(id=int(id_cliente))
	if request.method=='POST':
		forms=FormCliente(request.POST, instance=dato)
		if forms.is_valid():
			forms.save()
			return HttpResponse("El registro se actualizó correctamente.")
	else:
		forms=FormCliente(instance=dato)
	return render(request,'cliente/updateClient.html',{'forms':forms,'dato':dato})

def DetalleCliente(request,id):#id cliente
	cliente = get_object_or_404(Cliente, pk=id)
	productos=Producto.objects.filter(Cliente_id=id).order_by('-id')

	try:
		precio = Precio.objects.get(Cliente_id = id)
	except Precio.DoesNotExist:
		precio = False
	Usuario=Producto(Usuario=request.user)
	if request.method == 'POST':
		forms=FormProducto(request.POST,instance=Usuario)
		formR=FormResultado(request.POST)

		if forms.is_valid() and formR.is_valid():
			
			ingreso_id = saveCodeEnten(request,id)#id del cliente
			
			datos = forms.save(commit=False)
			datos.Cliente_id = int(id)
			datos.codigo_ingreso_id = int(ingreso_id)
			datos.save()#Guardo el Formulario Producto

			Dato = formR.save(commit=False)
			Dato.producto_id = int(datos.id)
			Dato.save()#Guardo el Formulario resultado

			return HttpResponseRedirect("/detalle-ingreso-cliente/"+str(ingreso_id)+"/")#retorna a la funcion DetalleCliente
	else:
		forms=FormProducto(instance=Usuario)
		formR=FormResultado()
	dic={
		'cliente':cliente,
		'productos':productos,
		'forms':forms,
		'formR':formR,
		'precio':precio
	}
	return render(request,'cliente/Detalle_persona.html',dic)

def DetalleIngresoCliente(request ,ingreso_id):
	ingreso = get_object_or_404(Codigo, pk=ingreso_id)
	productos=Producto.objects.filter(codigo_ingreso=ingreso_id).order_by('-id')
	Usuario=Producto(Usuario=request.user)
	if request.method == 'POST':
		forms=FormProducto(request.POST,instance=Usuario)
		formR=FormResultado(request.POST)

		if forms.is_valid() and formR.is_valid():
			
			datos = forms.save(commit=False)
			datos.Cliente_id = int(ingreso.cliente.id)
			datos.codigo_ingreso_id = int(ingreso_id)
			datos.save()#Guardo el Formulario Producto

			Dato = formR.save(commit=False)
			Dato.producto_id = int(datos.id)
			Dato.save()#Guardo el Formulario resultado

			return HttpResponseRedirect("/detalle-ingreso-cliente/"+str(ingreso_id)+"/")#retorna a la funcion DetalleCliente
	else:
		forms=FormProducto(instance=Usuario)
		formR=FormResultado()
	dic={
		'ingreso':ingreso,
		'productos':productos,
		'results':getResult(),
		'forms':forms,
		'formR':formR
	}
	return render(request,'cliente/DetalleIngresoCliente.html',dic)


def saveCodeEnten(request,id_cliente):
	ingreso = Codigo()
	ingreso.cliente_id = int(id_cliente)
	ingreso.usuario = request.user
	ingreso.save()
	return ingreso.id


def NewProductIngreso(request, ingreso_id):
	codigo = Codigo.objects.get(id = ingreso_id)
	Usuario=Producto(Usuario=request.user)
	if request.method == 'POST':
		forms=FormProducto(request.POST,instance=Usuario)
		formR=FormResultado(request.POST)

		if forms.is_valid() and formR.is_valid():
			
			datos = forms.save(commit=False)
			datos.Cliente_id = int(codigo.cliente.id)
			datos.codigo_ingreso_id = int(codigo.id)
			datos.save()#Guardo el Formulario Producto

			Dato = formR.save(commit=False)
			Dato.producto_id = int(datos.id)
			Dato.save()#Guardo el Formulario resultado

			return HttpResponseRedirect("/detalle-ingreso-cliente/"+str(codigo.id)+"/")#retorna a la funcion DetalleCliente
	else:
		forms=FormProducto(instance=Usuario)
		formR=FormResultado()
	return render(request,'cliente/NewProductIngreso.html',{'forms':forms,'formR':formR,'codigo':codigo})
	
def RegisterNewProductAndResult(request, id):#(id_cliente)
	cliente = Cliente.objects.get(id = id)
	Usuario=Producto(Usuario=request.user)
	if request.method == 'POST':
		forms=FormProducto(request.POST,instance=Usuario)
		formR=FormResultado(request.POST)

		if forms.is_valid() and formR.is_valid():
			
			ingreso_id = saveCodeEnten(request,id)#id del cliente
			
			datos = forms.save(commit=False)
			datos.Cliente_id = int(id)
			datos.codigo_ingreso_id = int(ingreso_id)
			datos.save()#Guardo el Formulario Producto

			Dato = formR.save(commit=False)
			Dato.producto_id = int(datos.id)
			Dato.save()#Guardo el Formulario resultado

			return HttpResponseRedirect("/detalle-ingreso-cliente/"+str(ingreso_id)+"/")#retorna a la funcion DetalleCliente
	else:
		forms=FormProducto(instance=Usuario)
		formR=FormResultado()
	return render(request,'cliente/RegistrarMuestra.html',{'forms':forms,'formR':formR,'cliente':cliente})


def UpdateProduct(request, id_producto):
	dato = Producto.objects.get(id=int(id_producto))
	result = Resultado.objects.get(producto_id=int(dato.id))
	if request.method == 'POST':
		forms = FormProductoUpdate(request.POST, instance=dato)
		formR = FormResultUpdate(request.POST, instance=result)
		if forms.is_valid() and formR.is_valid():
			forms.save()
			formR.save()
			return HttpResponseRedirect('/detalle-ingreso-cliente/'+str(dato.codigo_ingreso.id))
	else:
		forms = FormProductoUpdate(instance=dato)
		formR = FormResultUpdate(instance=result)
	return render(request, 'cliente/UpdateProduct.html', {'forms': forms,'formR':formR,'dato': dato})

def RestoreProduct(request, id_producto):
	producto = Producto.objects.get(id=int(id_producto))
	producto.estado=True
	producto.save()
	return HttpResponseRedirect('/DetalleCliente/'+str(producto.Cliente_id)+'/')
	#return HttpResponse("Registro Exitoso.")

def LitarElementos(request):
	datos = Elemento.objects.all().order_by('-id')
	dic={
		'datos':datos
	}
	return render(request,'cliente/LitarElementos.html',dic)


def CrearElemento(request):
	if request.method == 'POST':
		forms=FormElemento(request.POST)
		if forms.is_valid():
			forms.save()
			return LitarElementos(request)
	else:
		forms=FormElemento()
	return render(request,'cliente/CrearElemento.html',{'forms':forms})


def updateElemento(request, id_elemento):
	dato = Elemento.objects.get(id=int(id_elemento))
	if request.method == 'POST':
		forms = FormElementoUdate(request.POST, instance=dato)
		if forms.is_valid():
			forms.save()
	else:
		forms = FormElementoUdate(instance=dato)
	return render(request, 'cliente/updateElemento.html', {'forms': forms, 'dato': dato})


def restoreElemento(request,id_elemento):
	Elemento.objects.filter(id=int(id_elemento)).update(estado=True)
	return LitarElementos(request)


def RegisterResultados(request, id_producto):#product id (LOTE - product)
	getProduct = Producto.objects.get(id = int(id_producto))
	results=Resultado.objects.filter(producto_id=getProduct.id)
	if request.method == 'POST':
		forms=FormResultado(request.POST)
		if forms.is_valid():
			datos = forms.save(commit=False)
			datos.producto_id = int(id_producto)
			datos.save()
			cod=Resultado.objects.latest('id')
			return HttpResponse(id_producto)
	else:
		forms=FormResultado()
	return render(request,'cliente/RegisterResultado.html',{'forms':forms,'getProduct':getProduct,'results':results})

def deleteResult(request, id_result):
	result = Resultado.objects.get(id = id_result)
	id_product = result.producto_id
	result.delete()
	return RegisterResultados(request, id_product)

def printCertify(request ,ingreso_id):
	ingreso = get_object_or_404(Codigo, pk=ingreso_id)
	productos=Producto.objects.filter(codigo_ingreso=ingreso_id)
	results = getResult()
	getTotal = getTotales(productos, results)
	dic={
		'ingreso':ingreso,
		'productos':productos,
		'results':results,
		'getTotal':getTotal,
		'date_today':datetime.now(),
		'usuario':User.objects.get(id=int(request.user.id))
	}
	html=render_to_string('cliente/printCertify.html',dic)
	return generar_pdf(html)

def getResult():
	result=Resultado.objects.all()
	return result

def generar_pdf(html):
	resultado=io.BytesIO()
	pdf=pisa.pisaDocument(io.BytesIO(html.encode("UTF:8")),resultado)
	if not pdf.err:
		return HttpResponse(resultado.getvalue(),'application/pdf')
	return HttpResponse("Error al generar el reporte")

def detailReport(request):
	clients=Cliente.objects.filter(estado=True)
	return render(request,'cliente/detailReport.html',{'clients':clients})


def printReportGeneral(request, clients_id, fecha_inicio, fecha_fin):
	fecha_inicio = datetime.strptime(fecha_inicio,"%d-%m-%Y")
	fecha_fin = datetime.strptime(fecha_fin,"%d-%m-%Y")
	fecha_fin = fecha_fin + timedelta(days=1)
	if str(fecha_inicio) > str(fecha_fin):
		return HttpResponse("Error: La Fecha Inicio No pueder ser Mayor a la Fecha Final.")
	if int(clients_id) == 0:# if you don't choose any customer
		cliente = False
		products = Producto.objects.filter(fecha_registro__range=(fecha_inicio,fecha_fin),estado = True).order_by('fecha')
	else:
		cliente = Cliente.objects.get(id=int(clients_id))
		products = Producto.objects.filter(fecha_registro__range=(fecha_inicio,fecha_fin),estado = True, Cliente_id=int(clients_id)).order_by('fecha')	
	results = Resultado.objects.filter(fecha_registro__range=(fecha_inicio,fecha_fin),estado = True)
	total_general = getTotalGeneral(products, results)
	getTotal = getTotales(products, results)
	dic={
		'cliente':cliente,
		'products':products,
		'total_general':total_general,
		'getTotal':getTotal,
		'results':results,
		'fecha_inicio':fecha_inicio.date(),
		'fecha_fin':fecha_fin.date() - timedelta(days=1),
		'date_today':datetime.now(),
		'usuario':User.objects.get(id=int(request.user.id)),
		'pagesize':'letter'
	}
	html = render_to_string('cliente/printReportGeneral.html',dic)
	return generar_pdf(html)

def printReportTotal(request, clients_id, fecha_inicio, fecha_fin):
	fecha_inicio = datetime.strptime(fecha_inicio,"%d-%m-%Y")
	fecha_fin = datetime.strptime(fecha_fin,"%d-%m-%Y")
	fecha_fin = fecha_fin + timedelta(days=1)
	if str(fecha_inicio) > str(fecha_fin):
		return HttpResponse("Error: La Fecha Inicio No pueder ser Mayor a la Fecha Final.")
	if int(clients_id) == 0:# if you don't choose any customer
		cliente = False
		precio = False
		products = Producto.objects.filter(fecha_registro__range=(fecha_inicio,fecha_fin),estado = True)
	else:
		cliente = Cliente.objects.get(id=int(clients_id))
		try:
			precio = Precio.objects.get(Cliente_id = clients_id)
		except Precio.DoesNotExist:
			return HttpResponse('<h1>Por favor registre los precios del cliente %s para poder generar el reporte.</h1>'%(cliente.Nombre.upper()))
		
		products = Producto.objects.filter(fecha_registro__range=(fecha_inicio,fecha_fin),estado = True, Cliente_id=int(clients_id))	
	results = Resultado.objects.filter(fecha_registro__range=(fecha_inicio,fecha_fin),estado = True)
	getTotal = getTotales(products, results)
	total_general = getTotalGeneral(products, results)
	calcularPrecios = {}
	if precio:	
		calcularPrecios = calcularPreciosTotales(clients_id, getTotal)
	else:
		return HttpResponse('<h1>Selecione un cliente para generar el resumen</h1>')

	totalPrecio = getTotalPrecio(calcularPrecios)
	dic={
		'cliente':cliente,
		'products':products,
		'results':results,
		'precio':precio,
		'getTotal':getTotal,
		'totalPrecio':totalPrecio,
		'total_general':total_general,
		'calcularPrecios':calcularPrecios,
		'fecha_inicio':fecha_inicio.date(),
		'fecha_fin':fecha_fin.date() - timedelta(days=1),
		'date_today':datetime.now(),
		'usuario':User.objects.get(id=int(request.user.id)),
		'pagesize':'letter'
	}
	html = render_to_string('cliente/printReportTotal.html',dic)
	return generar_pdf(html)

def getTotalPrecio(calcularPrecios):
	total = 0
	for key, value in calcularPrecios.items():
		total = total + value
	return total 

def calcularPreciosTotales(clients_id, getTotal):
	calcularPrecios = {}
	precio = Precio.objects.get(Cliente_id = clients_id)
	zinc = precio.Zinc * getTotal['Zn']
	plata = precio.Plata * getTotal['DM.Ag']
	plomo = precio.Plomo * getTotal['Pb']
	estanio = precio.Estanio * getTotal['Sn']
	cobre = precio.Cobre * getTotal['Cu']
	h2o = precio.H2O * getTotal['H2O']

	antimonio = precio.Antimonio * getTotal['Sb']
	arsenico = precio.Arsenico * getTotal['As']
	hierro = precio.Hierro * getTotal['Fe']

	calcularPrecios['Zn'] = zinc
	calcularPrecios['DM.Ag'] = plata
	calcularPrecios['Pb'] = plomo
	calcularPrecios['Sn'] = estanio
	calcularPrecios['Cu'] = cobre
	calcularPrecios['H2O'] = h2o

	calcularPrecios['Sb'] = antimonio
	calcularPrecios['As'] = arsenico
	calcularPrecios['Fe'] = hierro

	return calcularPrecios

def getTotales(products, results):
	getTotal = {}
	zinc = 0
	plata = 0
	plomo = 0
	estanio = 0
	cobre = 0
	h2o = 0
	antimonio = 0
	arsenico = 0
	hierro = 0
	for product in products:
		for result in results:
			if int(result.producto.id) == int(product.id):
				if not result.Zinc == None:
					zinc = zinc + 1
				if not result.Plata == None:
					plata = plata + 1
				if not result.Plomo == None:
					plomo = plomo + 1
				if not result.Estanio == None:
					estanio = estanio + 1
				if not result.Cobre == None:
					cobre = cobre + 1
				if not result.H2O == None:
					h2o = h2o + 1
				if not result.Antimonio == None:
					antimonio = antimonio + 1
				if not result.Arsenico == None:
					arsenico = arsenico + 1
				if not result.Hierro == None:
					hierro = hierro + 1
	getTotal['Zn'] = zinc
	getTotal['DM.Ag'] = plata
	getTotal['Pb'] = plomo
	getTotal['Sn'] = estanio
	getTotal['Cu'] = cobre
	getTotal['H2O'] = h2o
	getTotal['Sb'] = antimonio
	getTotal['As'] = arsenico
	getTotal['Fe'] = hierro
	print(getTotal)
	return getTotal

def getTotalGeneral(products, results):
	total_general = 0
	for product in products:
		for result in results:
			if int(result.producto.id) == int(product.id):
				if not result.Zinc == None:
					total_general = total_general + 1
				if not result.Plata == None:
					total_general = total_general + 1
				if not result.Plomo == None:
					total_general = total_general + 1
				if not result.Estanio == None:
					total_general = total_general + 1
				if not result.Cobre == None:
					total_general = total_general + 1
				if not result.H2O == None:
					total_general = total_general + 1
				if not result.Antimonio == None:
					total_general = total_general + 1
				if not result.Arsenico == None:
					total_general = total_general + 1
				if not result.Hierro == None:
					total_general = total_general + 1
	return total_general

def reportGeneral(request, clients_id, fecha_inicio, fecha_fin):
	fecha_inicio = datetime.strptime(fecha_inicio,"%d-%m-%Y")
	print('Fecha inicio: ',fecha_inicio)
	fecha_fin = datetime.strptime(fecha_fin,"%d-%m-%Y")
	print('Fecha final: ', fecha_fin)
	fecha_fin = fecha_fin + timedelta(days=1)
	if str(fecha_inicio) > str(fecha_fin):
		return HttpResponse("Error: La Fecha Inicio No pueder ser Mayor a la Fecha Final.")
	if int(clients_id) == 0:# if you don't choose any customer
		cliente = False
		products = Producto.objects.filter(fecha_registro__range=(fecha_inicio,fecha_fin),estado = True)
	else:
		cliente = Cliente.objects.get(id=int(clients_id))
		products = Producto.objects.filter(fecha_registro__range=(fecha_inicio,fecha_fin),estado = True, Cliente_id=int(clients_id))
	results = Resultado.objects.filter(fecha_registro__range=(fecha_inicio,fecha_fin),estado = True)
	total_general = getTotalGeneral(products, results)
	getTotal = getTotales(products, results)
	dic={
			'cliente':cliente,
			'products':products,
			'total_general':total_general,
			'getTotal':getTotal,
			'results':results,
			'fecha_inicio':fecha_inicio.date(),
			'fecha_fin':fecha_fin.date() - timedelta(days=1),
			'date_today':datetime.now(),
			'usuario':request.user.first_name.title()
	}
	return render(request, 'cliente/reportGeneral.html',dic)


def searchCode(request):
	if request.method=='POST':
		codigo = get_object_or_404(Codigo, pk=int(request.POST['search']))
		return HttpResponseRedirect("/detalle-ingreso-cliente/"+str(codigo.id)+"/")


def addPrecios(request, cliente_id):
	if request.method=='POST':
		forms=FormPrecio(request.POST)
		if forms.is_valid():
			datos = forms.save(commit=False)
			datos.Cliente_id = int(cliente_id)
			datos.save()
			return redirect('/DetalleCliente/'+str(cliente_id)+'/')
	else:
		forms=FormPrecio()

	return render(request,'cliente/addPrecios.html',{'forms':forms,'cliente_id':cliente_id})


def updatePrecio(request, precio_id):
	dato=Precio.objects.get(id=int(precio_id))
	if request.method=='POST':
		forms=FormPrecio(request.POST, instance=dato)
		if forms.is_valid():
			forms.save()
			return HttpResponse("El registro se actualizó correctamente.")
	else:
		forms=FormPrecio(instance=dato)
	return render(request,'cliente/updatePrecio.html',{'forms':forms,'dato':dato})


class ReportAnalisis(View):
	def cabecera(self,pdf):
		#Utilizamos el archivo logo_django.png que está guardado en la carpeta media/imagenes
		#archivo_imagen = settings.MEDIA_ROOT+'/imagenes/logo_django.png'
		#Definimos el tamaño de la imagen a cargar y las coordenadas correspondientes
		#pdf.drawImage(archivo_imagen, 40, 750, 120, 90,preserveAspectRatio=True)
		#Establecemos el tamaño de letra en 16 y el tipo de letra Helvetica
		pdf.setFont("Helvetica", 18)
		#Dibujamos una cadena en la ubicación X,Y especificada
		pdf.drawString(230, 790, u"REPORTE DE")
		pdf.setFont("Helvetica", 18)
		pdf.drawString(245, 770, u"ANÁLISIS")
	def tabla(self,pdf,y, idProductos):
		idProductos = idProductos.split(',')
		idProductos = list(idProductos)
		#Creamos una tupla de encabezados para neustra tabla
		encabezados = ('Fecha', 'Lote', 'Resultados', '')
		#Creamos una lista de tuplas que van a contener a las personas
		data = []
		#print(idProductos)
		for i in idProductos:
			for producto in Producto.objects.filter(estado = True):
				if int(i) == int(producto.id):
					data.append(producto.fecha_registro)
					data.append(producto.Lote)
					for resultado in Resultado.objects.filter(estado = True).order_by('Elemento'):
						if resultado.producto.id == producto.id:
							data.append(resultado.Elemento.Abreviatura)
							data.append(resultado.Resultado)
		print(data)
		detalles = [(producto.estado, producto.Lote,resultado.Elemento.Abreviatura) 
					for i in idProductos
						for producto in Producto.objects.filter(estado = True)
							if int(i) == int(producto.id)
								for resultado in Resultado.objects.filter(estado = True).order_by('Elemento')
									if int(resultado.producto.id) == int(producto.id)
							]
		#Establecemos el tamaño de cada una de las columnas de la tabla
		detalle_orden = Table([encabezados] + detalles, colWidths=[2 * cm, 5 * cm, 5 * cm, 2 * cm])
		#Aplicamos estilos a las celdas de la tabla
		detalle_orden.setStyle(TableStyle(
			[
				#La primera fila(encabezados) va a estar centrada
				('ALIGN',(0,0),(3,0),'CENTER'),
				#Los bordes de todas las celdas serán de color negro y con un grosor de 1
				('GRID', (0, 0), (-1, -1), 1, colors.black), 
				#El tamaño de las letras de cada una de las celdas será de 10
				('FONTSIZE', (0, 0), (-1, -1), 10),
			]
		))
		#Establecemos el tamaño de la hoja que ocupará la tabla 
		detalle_orden.wrapOn(pdf, 800, 600)
		#Definimos la coordenada donde se dibujará la tabla
		detalle_orden.drawOn(pdf, 60,y)
	def get(self, request, *args, **kwargs):
		idProductos= kwargs.pop('idProductos')
		#Indicamos el tipo de contenido a devolver, en este caso un pdf
		response = HttpResponse(content_type='application/pdf')
		#La clase io.BytesIO permite tratar un array de bytes como un fichero binario, se utiliza como almacenamiento temporal
		buffer = io.BytesIO()
		#Canvas nos permite hacer el reporte con coordenadas X y Y
		pdf = canvas.Canvas(buffer)
		#Llamo al método cabecera donde están definidos los datos que aparecen en la cabecera del reporte.
		self.cabecera(pdf)
		y = 600
		#lla al metodo table
		self.tabla(pdf, y, idProductos)
		#Con show page hacemos un corte de página para pasar a la siguiente
		pdf.showPage()
		pdf.save()
		pdf = buffer.getvalue()
		buffer.close()
		response.write(pdf)
		return response