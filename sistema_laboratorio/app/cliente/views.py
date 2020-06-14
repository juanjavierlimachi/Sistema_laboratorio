from django.shortcuts import render, redirect,HttpResponse,HttpResponseRedirect
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
			forms.save()
			cod=Cliente.objects.latest('id')#ultimo regitro
			request.session['sesion'] = []#CREO UNA VARIABLE DE SESSION
			id_persona = request.session['sesion']
			id_persona.append(cod.id)
			request.session['sesion'] = id_persona
			return HttpResponse("Registro Exitoso.")
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
	#del request.session['id_producto']
	datos=Cliente.objects.get(id=int(id))
	try:
		productos=Producto.objects.filter(Cliente_id=id).order_by('-id')
	except :
		productos = {}
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
	return render(request,'cliente/RegistrarMuestra.html',{'forms':forms,'formR':formR,'id':int(id)})

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

