from django.shortcuts import render, redirect,HttpResponse,HttpResponseRedirect
from django.contrib.auth import logout as do_logout
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as do_login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import User
from sistema_laboratorio.app.inicio.forms import *
from django.contrib.auth.decorators import login_required

# Create your views here.
def welcome(request):
	if request.user.is_authenticated:
		
		return render(request,"inicio/welcome.html")
	return redirect("/login")
def register(request):
	form = UserForm()
	print ("imprimiste el formulalaaaa",form)
	if request.method == "POST":
		form = UserForm(data=request.POST)
		if form.is_valid():
			user = form.save()
			if user is not None:
				#do_login(request, user)
				return HttpResponse("<div class='alert alert-success' role='alert'>REGISTRO EXITOSO.</div>")
	form.fields['username'].help_text = None
	form.fields['password1'].help_text = None
	form.fields['password2'].help_text = None
	return render(request,"inicio/register.html",{'form':form})
def login(request):
	form = AuthenticationForm()
	if request.method == "POST":
		form = AuthenticationForm(data=request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user = authenticate(username=username,password=password)
			if user is not None and user.is_staff:
				do_login(request, user)
				return redirect("/")
			messages.error(request,'Error, Contactese con el administrador, para resolver el problema gracias.')
			return redirect('/')
		else:
			messages.error(request,'Error, datos incorrectos intente nuevamente gracias.')
			return redirect('/')
			#return render(request,'inicio/login.html',{'mej':'Error, datos incorrectos intente nuevamente gracias.'})
	return render(request,"inicio/login.html",{'form':form})
def logout(request):
	do_logout(request)
	return redirect("/")
def VerUsers(request):
	datos = User.objects.all().order_by('-id')
	dic={
		'datos':datos
	}
	return render(request,"inicio/VerUsers.html",dic)


from django.contrib import messages


def updateUser(request):
	if request.method=='POST':
		user_form=UserForms(request.POST,instance=request.user)
		if user_form.is_valid():
			user_form.save()
			messages.success(request, 'Your password was updated successfully!')
			#return render(request,'inicio/updateUser.html')  
			#return redirect('/')
	else:
		user_form=UserForms(instance=request.user)
	return render(request,'inicio/updateUser.html',{'user_form':user_form})


@login_required(login_url='/')
def ChangePassword(request):
	msj = ''
	if request.method=='POST':
		form=ChangePasswordForm(request.POST)
		new_password = request.POST['new_password']
		confirmed = request.POST['confirm_password']
		user = request.user
		print(user.check_password(request.POST['old_password']))
		if new_password == confirmed and user.check_password(request.POST['old_password']):
			user.set_password(new_password)
			user.save()
			print('bien')
			return HttpResponse("success")
		else:
			return HttpResponse("error")
	else:
		form=ChangePasswordForm()
	return render(request,'inicio/changePassword.html',{'form':form})


def showStatusUser(request, id_user):
	get_user = User.objects.get(id = id_user)
	return render(request,'inicio/showStatusUser.html',{'get_user':get_user})

def disableUser(request, id_user):
	if request.method == 'POST':
		get_user = User.objects.get(id = id_user)
		get_user.is_active=True
		get_user.is_staff=False
		get_user.is_superuser=False
		get_user.save()
		return HttpResponse('usuario Inhabilitado')

def changeRolUser(request, id_user):
	if request.method == 'POST':
		get_user = User.objects.get(id = id_user)
		if request.POST['option'] == 'super':
			get_user.is_active=True
			get_user.is_staff=True
			get_user.is_superuser=True
			get_user.save()
			return HttpResponse('superuser')
		if request.POST['option'] == 'user':
			get_user.is_active=True
			get_user.is_staff=True
			get_user.is_superuser=False
			get_user.save()
			return HttpResponse('usuario')
