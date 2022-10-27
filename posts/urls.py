from django.urls import path
from . import views
	
urlpatterns = [
    path('', views.index, name='index'),
    path('post/<int:post_id>', views.post, name='post'),
    path('<str:categoria>', views.categoria, name='categoria'),
    path('busca/', views.busca, name='busca'),
]