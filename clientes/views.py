from django.http import Http404
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from django.db.models import Q
from .models import Cliente
from .forms import formulario_cliente
# Create your views here.

def crear_cliente(request):
    f = formulario_cliente(request.POST or None) #f es un objeto de la Pe:ción POST
    if request.method == 'POST':
        if f.is_valid():
            datos = f.cleaned_data
            c = Cliente()
            c.nombres = datos.get("nombres")
            c.apellidos = datos.get("apellidos")
            c.detalle = datos.get("detalle")
            c.medidor = datos.get("medidor")
            c.cedula = datos.get("cedula")
            c.email = datos.get("email")
            c.direccion = datos.get("direccion")
            c.celular = datos.get("celular")
            #c.deuda = datos.get("deuda")
            if c.save() != True:
                messages.success(request, "El usuario '"+ c.nombres +"' con número de medidor '"+c.medidor+"' a sido registrado correctamente!")
                return redirect("listarclientes")
        else:
           messages.success(request, "A ocurrido un error! Puede que el número de medidor ya este registrado.")
    context = {
        "form":f,
    }
    return render(request,"crearCliente.html",context)

#metodo para listar clientes
def listar_clientes(request):
    busqueda = request.GET.get("buscar")
    try:
        clientes = Cliente.objects.all()
    except Cliente.DoesNotExist:
                raise Http404
    if busqueda:
        messages.success(request, " Los resultados encontrados para la busqueda '"+busqueda+"' son:")
        try:
            clientes = Cliente.objects.filter(
                Q(nombres__icontains = busqueda) |
                Q(apellidos__icontains = busqueda)|
                Q(medidor__icontains = busqueda) | 
                Q(cedula__icontains = busqueda) 
            ).distinct()
        except Cliente.DoesNotExist:
            raise Http404
    return render(request, "clientes.html", {"clientes": clientes})

def editar_cliente(request, id):
    try:
        cliente = Cliente.objects.get(id=id)
    except Cliente.DoesNotExist:
        raise Http404
    f = formulario_cliente(initial={'nombres':cliente.nombres,
                            'apellidos':cliente.apellidos,
                            'detalle':cliente.detalle,
                            'medidor':cliente.medidor,
                            'cedula':cliente.cedula,
                            'email':cliente.email,
                            'direccion':cliente.direccion,
                            'celular':cliente.celular})
    context = {
        "form":f,
        "cliente":cliente,
    }
    return render(request, "editarCliente.html", context)

def actualizar_cliente(request, id):
    try:
        cliente = Cliente.objects.get(pk=id)
    except Cliente.DoesNotExist:
        raise Http404
    form = formulario_cliente(request.POST, instance=cliente)
    if form.is_valid():
        try:
            form.save()
        except:
            raise Http404
        messages.success(request, "Usuario '"+ cliente.nombres + " " + str(cliente.apellidos) + " medidor numero: "+ cliente.medidor +"' a sido actualizado correctamente.")
        return redirect('/clientes')
    else:
           messages.success(request, "A ocurrido un error! Puede que el número de medidor ya este registrado.")
    context = {
        "form":form,
        "cliente":cliente,
    }
    return render(request, "editarCliente.html", context)

def ver_cliente(request, id):
    try:
        cliente = Cliente.objects.get(id=id)
    except Cliente.DoesNotExist:
        raise Http404
    f = formulario_cliente(initial={'nombres':cliente.nombres,
                            'apellidos':cliente.apellidos,
                            'detalle':cliente.detalle,
                            'medidor':cliente.medidor,
                            'cedula':cliente.cedula,
                            'email':cliente.email,
                            'direccion':cliente.direccion,
                            'celular':cliente.celular})
    context = {
        "form":f,
        "cliente":cliente,
    }
    return render(request, "verCliente.html", context)

#metodo para alertar la eliminacion de un cliente
def eliminar_cliente(request, id):
    try:
        cliente = Cliente.objects.get(id=id)
    except Cliente.DoesNotExist:
        raise Http404
    context = {
        "cliente":cliente,
    }
    return render(request, "eliminarCliente.html", context)

#metodo para conformar la eliminacion
def confirmar_eliminar_cliente(request, id):
    try:
        cliente = Cliente.objects.get(id=id)
        cliente.delete()
    except Cliente.DoesNotExist:
        raise Http404
    messages.success(request, "El usuario "+ cliente.nombres + " medidor número: "+ cliente.medidor +" a sido eliminado corectamente")
    return redirect('/clientes')