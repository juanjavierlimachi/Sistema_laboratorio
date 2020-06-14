from django.shortcuts import render, redirect,HttpResponse
from django.contrib.auth import logout as do_logout
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as do_login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import User
from sistema_laboratorio.app.inicio.forms import *
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
			if user is not None:
				do_login(request, user)
				return redirect("/")
		else:
			return render(request,'inicio/login.html',{'mej':'Error, datos incorrectos intente nuevamente gracias.'})
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