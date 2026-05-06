from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProductoListView.as_view(), name='producto_lista'),
    path('crear/', views.ProductoCreateView.as_view(), name='producto_crear'),
    path('editar/<int:pk>/', views.ProductoUpdateView.as_view(), name='producto_editar'),
    path('eliminar/<int:pk>/', views.ProductoDeleteView.as_view(), name='producto_eliminar'),
]