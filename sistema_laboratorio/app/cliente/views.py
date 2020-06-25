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
	datos = get_object_or_404(Cliente, pk=id)
	productos=Producto.objects.filter(Cliente_id=id).order_by('-id')
	dic={
		'cliente':datos,
		'productos':productos
	}
	return render(request,'cliente/Detalle_persona.html',dic)
def Detalle_persona(request):
	#del request.session['id_producto']
	id_persona = request.session['sesion']
	id_cliente = id_persona[0]
	datos=Cliente.objects.get(id=int(id_cliente))
	muestras=Producto.objects.filter(Cliente_id=id_cliente)
	dic={
		'cliente':datos,
		'muestras':muestras
	}
	#del request.session['sesion']   
	return render(request,'cliente/Detalle_persona.html',dic)
def RegisterNewProductAndResult(request, id):#(id_cliente)
	cliente = Cliente.objects.get(id = id)
	Usuario=Producto(Usuario=request.user)
	if request.method == 'POST':
		forms=FormProducto(request.POST,instance=Usuario)
		formR=FormResultado(request.POST)

		if forms.is_valid() and formR.is_valid():
			datos = forms.save(commit=False)
			datos.Cliente_id = int(id)
			datos.save()#Guardo en el Formulario Prducto

			Dato = formR.save(commit=False)
			Dato.producto_id = int(datos.id)
			Dato.save()#Guardo en el Formulario Prducto
			return HttpResponseRedirect("/DetalleCliente/"+str(id)+"/")#retorna a la funcion DetalleCliente
	else:
		forms=FormProducto(instance=Usuario)
		formR=FormResultado()
	return render(request,'cliente/RegistrarMuestra.html',{'forms':forms,'formR':formR,'cliente':cliente})


def UpdateProduct(request, id_producto):
	dato = Producto.objects.get(id=int(id_producto))
	if request.method == 'POST':
		forms = FormProductoUpdate(request.POST, instance=dato)
		if forms.is_valid():
			forms.save()
			return HttpResponseRedirect('/DetalleCliente/'+str(dato.Cliente_id))
	else:
		forms = FormProductoUpdate(instance=dato)
	return render(request, 'cliente/UpdateProduct.html', {'forms': forms, 'dato': dato})

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

def printCertify(request, idProductos):
	idProductos = idProductos.split(',')
	idProductos = list(map(int,idProductos))
	productos = Producto.objects.filter(estado = True)
	resultados = Resultado.objects.filter(estado = True).order_by('Elemento')
	for id_producto in idProductos:
		getProduct = Producto.objects.get(id = int(id_producto))
		break
	date_today = datetime.now().strftime("%d/%m/%Y")
	print(request.user.first_name)
	dic = {
			'pagesize':'letter',
			'idProductos':idProductos, 
			'productos':productos,
			'resultados':resultados,
			'getProduct':getProduct,
			'date_today':date_today,
			'usuario':request.user.first_name.title()
		 }
	html=render_to_string('cliente/printCertify.html',dic)
	return generar_pdf(html)

def generar_pdf(html):
	resultado=io.BytesIO()
	pdf=pisa.pisaDocument(io.BytesIO(html.encode("UTF:8")),resultado)
	if not pdf.err:
		return HttpResponse(resultado.getvalue(),'application/pdf')
	return HttpResponse("Error al generar el reporte")

def detailReport(request):
	clients=Cliente.objects.filter(estado=True)
	return render(request,'cliente/detailReport.html',{'clients':clients})

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