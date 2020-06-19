from django.shortcuts import render, redirect,HttpResponse,HttpResponseRedirect, get_object_or_404
from sistema_laboratorio.app.cliente.forms import *
from django.shortcuts import redirect
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

	#consulta = Producto.objects.raw('SELECT * FROM clientes_productos')
	for id_producto in idProductos:
		getProduct = Producto.objects.get(id = int(id_producto))
		print(id_producto)
		results=Resultado.objects.filter(producto_id=getProduct.id)
		#print(results)
		#(getProduct,results)
		
	return render(request,'cliente/printCertify.html',{'idProductos':idProductos, 'productos':productos, 'resultados':resultados,'getProduct':getProduct})


def showCertify(getProduct):
	results=Resultado.objects.filter(producto_id=getProduct.id)
	print('holas')
	return HttpResponse(results)

def detailReport(request):
	return render(request,'cliente/detailReport.html')