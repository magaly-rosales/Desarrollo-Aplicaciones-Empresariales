from django.urls import path
from . import views

urlpatterns = [
    path('', views.listado_productos, name='listado_productos'),
    path('crear/', views.crear_producto, name='crear_producto'),
]