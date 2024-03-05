from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('adicionar_usuario/', views.adicionar_usuario, name='adicionar_usuario'),
    path('excluir_usuario/', views.excluir_usuario, name='excluir_usuario'),
    path('editar_usuario/', views.editar_usuario, name='editar_usuario')
]

