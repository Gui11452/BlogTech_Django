from django.urls import path
from . import views
	
urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('edit/', views.edit, name='edit'),
    path('login/', views.login, name='login'),
    path('registro/', views.registro, name='registro'),
    path('logout/', views.logout, name='logout'),
]