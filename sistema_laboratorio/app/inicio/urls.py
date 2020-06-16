from django.contrib import admin
from django.urls import path
from sistema_laboratorio.app.inicio import views

urlpatterns = [
	path('', views.welcome),
	path('register', views.register),
	path('login', views.login),
	path('logout', views.logout),
	path('VerUsers',views.VerUsers),
	path('changePassword',views.ChangePassword),
	path('updateUser',views.updateUser),
]