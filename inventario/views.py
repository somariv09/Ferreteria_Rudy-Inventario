import os
from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from django.conf import settings
from django.core.files.storage import FileSystemStorage

from django.db import transaction
from django.utils import timezone

from decimal import Decimal, InvalidOperation

from .models import Categoria, Producto, Movimiento

#request solicitud del navegador
def login(request):
    #Identificar si hay inicio de sesión abierto
    if request.user.is_authenticated:
        return redirect('dashboard')

    #NO se muestra error ya que no se ha autenticado
    error=None

    #Comprobar si se envio información
    if request.method == 'POST':
        usuario=request.POST.get('usuario','').strip()
        password=request.POST.get('password','')

        #Meotodo para verificar las credenciales. Devuelve credeciales o None
        user= authenticate(
            request,
            username=usuario,
            password=password
        )

        if user is not None:
            auth_login(request, user)
            return redirect('dashboard')

        error="USUARIO O CONTRASEÑA INCORRECTOS"
    #Si no se inicia sesion con exito se redirecciona a login de nuevo
    return render(request, 'login.html', {'error':error})

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

#Requiere el envio de una solicitud
@require_POST
def logout(request):
    #Meotod de django que cierra la sesion
    auth_logout(request)
    return redirect('login')




#Pruebas

def historial(request):
    return render(request, 'historial.html')


def registroEntrada(request):
    error=None

    productos=Producto.objects.all().order_by("nombre")

    if request.method=="POST":
        productoID=request.POST.get('producto', '')
        cantidad=request.POST.get('cantidad', '')

        try:
            productoID= int(productoID)
            cantidad=int(cantidad)

            if cantidad<=0:
                error="El valor debe ser mayor a cero."
        except(ValueError, TypeError):
            error="Seleccione un producto e ingrese la cantidad"

        if not error:
            try:
                with transaction.atomic():
                    productos=Producto.objects.select_for_update().get(id_producto=productoID)

                    ultimoMovimiento=Movimiento.objects.filter(codigo_movimiento__startswith="MOV-").order_by('-id_movimiento').first()

                    if ultimoMovimiento:
                        #Separar el string en 2 y obtener la parte del numero
                        ultimoNumero=int(ultimoMovimiento.codigo_movimiento.rsplit('-',1)[1])
                    else:
                        ultimoNumero=0

                    codigo=f"MOV-{ultimoNumero+1:04d}"

                    productos.cantidad+=cantidad
                    productos.save(update_fields=['cantidad'])

                    Movimiento.objects.create(
                        codigo_movimiento=codigo,
                        tipo_movimiento=Movimiento.ENTRADA,
                        cantidad=cantidad,
                        fecha=timezone.now(),
                        usuario=request.user,
                        producto=productos
                    )
                return redirect('dashboard')
            except Producto.DoesNotExist:
                error="El producto no existe"
    return render(request, 'registroEntrada.html', {'error':error, 'productos':productos})


def registroSalida(request):
    error=None
    
    productos=Producto.objects.all().order_by("nombre")
    
    if request.method=="POST":
        productoID=request.POST.get('producto', '')
        cantidad=request.POST.get('cantidad', '')

        try:
            productoID= int(productoID)
            cantidad=int(cantidad)

            if cantidad<=0:
                error="El valor debe ser mayor a cero."
        except(ValueError, TypeError):
            error="Seleccione un producto e ingrese la cantidad"

        if not error:
            try:
                with transaction.atomic():
                    productos=Producto.objects.select_for_update().get(id_producto=productoID)

                    ultimoMovimiento=Movimiento.objects.filter(codigo_movimiento__startswith="MOV-").order_by('-id_movimiento').first()

                    if ultimoMovimiento:
                        #Separar el string en 2 y obtener la parte del numero
                        ultimoNumero=int(ultimoMovimiento.codigo_movimiento.rsplit('-',1)[1])
                    else:
                        ultimoNumero=0

                    codigo=f"MOV-{ultimoNumero+1:04d}"

                    productos.cantidad-=cantidad
                    productos.save(update_fields=['cantidad'])

                    Movimiento.objects.create(
                        codigo_movimiento=codigo,
                        tipo_movimiento=Movimiento.SALIDA,
                        cantidad=cantidad,
                        fecha=timezone.now(),
                        usuario=request.user,
                        producto=productos
                    )
                return redirect('dashboard')
            except Producto.DoesNotExist:
                error="El producto no existe"
    return render(request, 'registroSalida.html', {'error':error, 'productos':productos})


def editarMovimiento(request):
    return render(request, 'editarMovimiento.html')


def catalogoProducto(request):
    return render(request, 'catalogoProducto.html')


def agregarProducto(request):
    error= None

    categorias= Categoria.objects.all().order_by("nombre")

    if request.method=="POST":
        imagen=request.FILES.get('imagen')
        codigo=request.POST.get('codigo','').strip().upper()
        nombre=request.POST.get('nombre','').strip().upper()
        #Recibe el valor numerico del id
        categoria=request.POST.get('categoria','')
        descripcion=request.POST.get('descripcion','').strip()
        cantidad=request.POST.get('cantidad','')
        precio=request.POST.get('precio','')
        stockMinimo=request.POST.get('stockMinimo','')

        ruta_imagen=None
    
        if not codigo or not nombre or not categoria:
            error="Debe ingresar los campos de código, nombre y categoria."
    
        elif not cantidad or not precio or not stockMinimo:
            error="Ingrese los campos de cantidad, precio y stock mínimo"
    
        elif Producto.objects.filter(nombre=nombre).exists():
            error="El producto ya existe"
    
        else:
            try:
                cantidad=int(cantidad)
                precio=Decimal(precio)
                stockMinimo=int(stockMinimo)
    
                if cantidad < 0 or precio < 0:
                    error="Cantidad y precio no puede ser menor a 0"
    
                elif stockMinimo < 5:
                    error="El stock minimo debe ser mayor o igual a cinco"

            except(ValueError, InvalidOperation):
                error= "La cantidad, precio o stock minimo no tiene un formato válido"
    
        if imagen and os.path.splitext(imagen.name)[1].lower() not in ['.jpg', '.jpeg', '.png']:
                    error = "La imagen debe ser JPG, JPEG, PNG"
        
        elif imagen and imagen.size >2*1024*1024:
                    error="La imagen supera los 2MB"
            
        else:
            ruta_imagen= None

            if imagen:
                almacenamiento=FileSystemStorage(location=settings.MEDIA_ROOT)
                nombre_archivo=os.path.basename(imagen.name)

                ruta_imagen=almacenamiento.save(f'productos/{nombre_archivo}', imagen)
        
        if not error:
            Producto.objects.create(
                imagen=ruta_imagen,
                codigo_producto=codigo,
                nombre=nombre,
                categoria_id=categoria,
                descripcion=descripcion,
                cantidad=cantidad,
                precio_unitario=precio,
                stock_minimo=stockMinimo       
            )
            return redirect('catalogoProducto')
    return render(request, 'agregarProducto.html', {'error':error, "categorias":categorias})

   


def editarProducto(request, id_producto):
    return render(request, 'editarProducto.html')


def catalogoCategoria(request):
    return render(request, 'catalogoCategoria.html')


def agregarCategoria(request):
    error=None

    if request.method == "POST":
        nombre=request.POST.get('nombre', '').strip().upper()
        descripcion=request.POST.get('descripcion', '').strip()
        imagen=request.FILES.get('imagen')

        if not nombre:
            error="Ingrese el nombre de la categoria"

        elif Categoria.objects.filter(nombre=nombre).exists():
            error="Esta categoria ya existe."

        elif imagen and os.path.splitext(imagen.name)[1].lower() not in ['.jpg', '.jpeg', '.png']:
            error = "La imagen debe ser JPG, JPEG, PNG"

        elif imagen and imagen.size >2*1024*1024:
            error="La imagen supera los 2MB"
    
        else:
            ruta_imagen= None

            if imagen:
                almacenamiento=FileSystemStorage(location=settings.MEDIA_ROOT)
                nombre_archivo=os.path.basename(imagen.name)

                ruta_imagen=almacenamiento.save(f'categorias/{nombre_archivo}', imagen)

        if not error:
            Categoria.objects.create(
                nombre=nombre,
                descripcion=descripcion,
                imagen=ruta_imagen
            )
            return redirect('catalogoCategoria')

    return render(request, 'agregarCategoria.html', {'error':error})


def editarCategoria(request, id_categoria):
    return render(request, 'editarCategoria.html')


def eliminarProducto(request, id_producto):
    return render(request, 'catalogoProducto.html')


def eliminarCategoria(request, id_categoria):
    return render(request, 'catalogoCategoria.html')

def eliminarMovimiento(request, id_movimiento):
    return render(request, 'historial.html')

