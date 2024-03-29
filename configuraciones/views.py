from django.http import Http404
from django.db.models import Q
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from .models import ValoresBase
from clientes.models import Cliente
from django.contrib.auth.models import User
# Create your views here.

def configuraciones(request):
    idv = ValoresBase.objects.latest('id')
    valores = ValoresBase.objects.get(id=idv.id)
    if valores:
        return render(request, "configuraciones.html",{"valorbase":valores.valor_cifra_base,"base":valores.base,"adicional":valores.valor_adicional,"porcentaje":valores.porcentaje_mora})
    else:
        return render(request, "configuraciones.html")

def nuevo_administrador(request):
    usuarios = User.objects.all()
    if request.method == 'POST':
        pass1 = str(request.POST["contraseña1"])
        pass2 = str(request.POST["contraseña2"])
        if pass1 == pass2:
            try:
                user = User.objects.create_user(username=request.POST['username'], email=request.POST['correo'],password=pass1)
                user.save()
                messages.success(request, "Usurio creado con éxito!")
            except:
                messages.success(request, "El usuario ya existe. Inténtelo nuevamente!")
                return redirect("/nuevoadministrador") 
        else:
            messages.error(request, "Las contraseñas no coinciden. Inténtelo nuevamente!")
            return redirect("/nuevoadministrador")
    if usuarios:
        return render(request, "nuevoAdmin.html",{"usuarios":usuarios})
    else:
        return render(request, "nuevoAdmin.html",)

def nuevos_valores(request):
    valores =ValoresBase.objects.all()
    if request.method == 'POST':
        valor = ValoresBase()
        valor.valor_cifra_base = request.POST["valorbase"]
        valor.base = request.POST["base"]
        valor.valor_adicional = request.POST["valoradicional"]
        valor.porcentaje_mora = request.POST["mora"]
        try:
            valor.save()
            messages.success(request, "Los nuevos valores Base han sido agregados correctamente!")
        except:
            messages.success(request, "Ingrese correctamente los datos e inténtelo nuevamente!")
            return redirect("/valoresbase") 
    if valores:
        return render(request, "valoresBase.html",{"valores":reversed(valores)})
    else:
        return render(request, "valoresBase.html")

def actualizar_usuario(request,id):
    usuarios = User.objects.all()
    actualizar = 's'
    if request.method == 'POST':
        usuario = User.objects.filter(id=request.user.id)
        pass1 = str(request.POST["contraseña1"])
        pass2 = str(request.POST["contraseña2"])
        if pass1 == pass2:
            if usuario.exists():
                try:
                    usuario = usuario.first()
                    usuario.username=request.POST['username']
                    usuario.email=request.POST['correo']
                    usuario.set_password=request.POST["contraseña2"]
                    print(pass1)
                    usuario.save()
                    messages.success(request, "Usurio actualizado con éxito!")
                    return redirect("/nuevoadministrador")
                except:
                    messages.success(request, "El usuario ya existe. Inténtelo nuevamente!")
                    return redirect("/nuevoadministrador") 
        else:
            messages.error(request, "Las contraseñas no coinciden. Inténtelo nuevamente!")
            return redirect("/nuevoadministrador")
    if usuarios:
        return render(request, "nuevoAdmin.html",{"actualizar":actualizar,"usuarios":usuarios})
    else:
        return render(request, "nuevoAdmin.html",{"actualizar":actualizar})

def eliminar_usuario(request):
    if request.method == 'POST':
        usuario = User.objects.filter(id=request.user.id)
        usuario.delete()
        messages.success(request, "Usurio eliminado")
        return redirect("/")
    return render(request, "eliminarAdmin.html")

#metodo para listar clientes
def listar_clienteseliminados(request):
    busqueda = request.GET.get("buscar")
    try:
        clientes = Cliente.objects.filter(
                Q(detalle__icontains = 'eliminado') 
            ).distinct()
    except Cliente.DoesNotExist:
                raise Http404
    print (clientes)
    if busqueda:
        messages.success(request, " Los resultados encontrados para la busqueda '"+busqueda+"' son:")
        try:
            clientes = Cliente.objects.filter(detalle = 'eliminado').filter(
                Q(nombres__icontains = busqueda) |
                Q(apellidos__icontains = busqueda)|
                Q(medidor__icontains = busqueda) | 
                Q(cedula__icontains = busqueda) 
            ).distinct()
        except Cliente.DoesNotExist:
            raise Http404
    return render(request, "restablecerCliente.html", {"clientes": clientes})

#restablecer cliente eliminado
def restablecer(request, id):
    try:
        cliente = Cliente.objects.get(pk=id)
    except Cliente.DoesNotExist:
        raise Http404
    cliente.detalle = ""
    if cliente.save() != True:
        messages.success(request, "El cliente <"+str(cliente.nombres)+" "+str(cliente.apellidos)+">, a sido restablecido correctamente!")
    else:
        messages.success(request, "A ocurrido un error! Vuelva a intentarlo.")
    return render(request, "restablecerCliente.html", )
