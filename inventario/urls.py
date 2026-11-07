from django.urls import path
from . import views

urlpatterns=[
    path('', views.dashboard, name='dashboard'),

    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),

    path('productos/', views.catalogoProducto, name='catalogoProducto'),
    path('producto/agregar/', views.agregarProducto, name='agregarProducto'),
    path('producto/editar/<int:id_producto>/', views.editarProducto, name='editarProducto'),
    path('producto/eliminar/<int:id_producto>/', views.eliminarProducto, name='eliminarProducto'),

    path('categorias/', views.catalogoCategoria, name='catalogoCategoria'),
    path('categorias/agregar/', views.agregarCategoria, name='agregarCategoria'),
    path('categorias/editar/<int:id_categoria>/', views.editarCategoria, name='editarCategoria'),
    path('categorias/eliminar/<int:id_categoria>/', views.eliminarCategoria, name='eliminarCategoria'),

    path('historial/', views.historial, name='historial'),
    path('entrada/', views.registroEntrada, name='registroEntrada'),
    path('salida/', views.registroSalida, name='registroSalida'),
    path('movimiento/editar/<int:id_movimiento>/', views.editarMovimiento, name='editarMovimiento'),
    path('movimiento/eliminar/<int:id_movimiento>/', views.eliminarMovimiento, name='eliminarMovimiento'),

]