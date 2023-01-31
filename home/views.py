from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.contrib import messages
from django.core.mail import send_mail
from email.message import EmailMessage
from django.db.models import Q
from clientes.models import Cliente
from cobros.models import Cobros
from configuraciones.models import ValoresBase
import datetime


# Create your views here.

def superUser(request):
    username = str(request.POST["usuario"])
    email = str(request.POST["correo"])
    password = str(request.POST["contraseña"])
    user = User(
        username = username,
        email = email,
    )
    user.set_password(password)
    user.is_superuser = True
    user.is_staff = True
    try:
        user.save()
    except:
        raise Http404
    
    messages.success(request, "Ahora es posible iniciar sesión!")
    return render(request, "infocorreo.html", {})



@csrf_exempt
def home(request,):
    #valores base para la pantalla principal
    try:
        idv = ValoresBase.objects.latest('id')
        valores = ValoresBase.objects.get(id=idv.id)
    except ValoresBase.DoesNotExist:
        raise Http404
    
    #para busqueda de pantalla principal
    busqueda = request.POST.get("buscar")
    if busqueda:
        messages.success(request, " Los resultados encontrados para la busqueda '"+busqueda+"' son:")
        date = datetime.date.today()
        año = date.strftime("%Y")
        mes = date.strftime("%B")
        fecha = mes+año
        try:
            clientes = Cliente.objects.filter(
                Q(nombres__icontains = busqueda) |
                Q(apellidos__icontains = busqueda)|
                Q(medidor__icontains = busqueda) | 
                Q(cedula__icontains = busqueda) 
            ).distinct()
        except Cliente.DoesNotExist:
            raise Http404
        return render(request, "cobros.html", {"clientes": clientes,"fecha":fecha})
    #para obtener recaudaciones
    cobros_actuales=0
    cobros_totales=0
    date = datetime.date.today()
    año = date.strftime("%Y")
    mes = date.strftime("%B")
    try:
        cobros = Cobros.objects.all()
    except Cobros.DoesNotExist:
        raise Http404
    if cobros:
        for cob in cobros:
            cobros_totales = cobros_totales+cob.total
            if cob.fechacifra == mes+año:
                cobros_actuales= cobros_actuales+cob.total
    #para inicio de sesion
    if request.method == 'GET':#cuando ya esta autenticaado
        if valores:
            return render(request, "inicio.html", {'form': AuthenticationForm,"valorbase":valores.valor_cifra_base,"base":valores.base,"adicional":valores.valor_adicional,"porcentaje":valores.porcentaje_mora,"cobros_totales":cobros_totales,"mes":mes,"cobros_actuales":cobros_actuales})
        else:
            return render(request, "inicio.html", {'form': AuthenticationForm,})
    else:
        user = authenticate(
            request, username=request.POST['username'],
            password=request.POST['password'])
        if user is None:
            messages.success(request, "Usuario o contraseña incorrectos!")
            return render(request, "home.html", {
                'form': AuthenticationForm
            })
        else:
            login(request, user)
            if valores:
                return render(request, "inicio.html", {"valorbase":valores.valor_cifra_base,"base":valores.base,"adicional":valores.valor_adicional,"porcentaje":valores.porcentaje_mora,"cobros_totales":cobros_totales,"mes":mes,"cobros_actuales":cobros_actuales})
            else:
                return render(request, "inicio.html", {})
    

def cerrar_sesion(request):
    logout(request)
    return redirect('home')

def info_correo(request,):
    if request.method == 'POST':
        asunto=request.POST['asunto']
        correo=request.POST['correo']
        descripcion=request.POST['descripcion']
        #email = EmailMessage(
        #    asunto,
        #    "De <{}>\n\nEscribió:\n\n{}".format(correo, descripcion),
        #    "servicioaguamilagro@gmail.com",
        #    ['edhisson97sanmartin@gmail.com','servicioaguamilagro@gmail.com']
        #)
        try:
            send_mail(
                asunto,
                'El correo <'+correo+'>, escribió: '+descripcion,
                'servicioaguamilagro@gmail.com',
                ['servicioaguamilagro@gmail.com','edhisson97sanmartin@gmail.com',correo],
                fail_silently=False,
            )
            messages.success(request, "El correo de "+correo+" se a enviado correctamente.")
        except:
            messages.success(request, "A ocurrido un error, vuelva a intenterlo!")
    #crear user ini
    try:
        usuarios = User.objects.all()
    except User.DoesNotExist:
        raise Http404
    if usuarios:
        return render(request, "infocorreo.html", {"usuarios":usuarios})
    return render(request, "infocorreo.html", {})