from django.shortcuts import render, redirect
from .models import productos
from .forms import ProductoForm


def listado_productos(request):
    mensaje = request.GET.get('ok')
    productos_ordenados = sorted(productos, key=lambda p: p['categoria'])
    return render(request, 'tienda/listado.html', {'productos': productos_ordenados, 'mensaje': mensaje})
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            nuevo_id = len(productos) + 1
            productos.append({
                'id': nuevo_id,
                'nombre': form.cleaned_data['nombre'],
                'precio': form.cleaned_data['precio'],
                'stock': form.cleaned_data['stock'],
                'categoria': form.cleaned_data['categoria'],
            })
            return redirect('/tienda/?ok=1')
    else:
        form = ProductoForm()
    return render(request, 'tienda/crear.html', {'form': form})