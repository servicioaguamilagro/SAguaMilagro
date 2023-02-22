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
from django.utils.translation import gettext as _
from django.db.models import Q
from clientes.models import Cliente
from cobros.models import Cobros
from cifras.models import Cifras
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
            cobros_totales = cob.total + cobros_totales
            print(cob.fechacifra)
            print(mes+año)
            if cob.fechacifra == mes+año:
                cobros_actuales= cobros_actuales+cob.total
    print(cobros_actuales)
    print(cobros_totales)
    
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

def calcular_valores(request):
    medidor = request.POST.get("buscar")
    mensaje =""
    try:
        clientes = Cliente.objects.filter(
            Q(medidor = medidor)
        ).distinct()
    except Cliente.DoesNotExist:
        raise Http404
    if clientes:
        for cliente in clientes:
            try:
                cifras = Cifras.objects.filter(id_usuario = cliente).distinct()
            except Cifras.DoesNotExist:
                raise Http404
            auxcifra =0
            #para obtener el año y mes
            date = datetime.date.today()
            año = date.strftime("%Y")
            mes = date.strftime("%B")
            fecha = mes+año
            total =0
            mora = 0
            pendiente = 0
            fechamora =[]
            auxmora = 0
            estado = 's'
            ultimopago =''
            for cifra in cifras:#recorre cifra por cifra del usuario
                estado =cifra.estado#para saber el ultimo estado de la cifra
                if cifra.estado == 's':#comprueba si la cifra a sido pagada  
                    auxcifra =cifra.cifra#almacena la ultima cifra pagada
                    ultimopago = cifra.mes
                else:
                    
                    cifr = cifra.cifra-auxcifra#calcula la cifra para realizar mas calculos
                    try:
                        valoresbase = ValoresBase.objects.get(id=cifra.id_valores)
                    except ValoresBase.DoesNotExist:
                        raise Http404
                    valor = valoresbase.valor_cifra_base
                    subtotal = 0.0
                    
                    if cifr > valoresbase.base:#para calcular el adicional si se psa de la base
                        adicional = (cifr-valoresbase.base)*valoresbase.valor_adicional
                        auxcifra =cifra.cifra#actualizo cifra base
                        
                    else:
                        adicional = 0
                        subtotal = valor + adicional
                        auxcifra =cifra.cifra#actualizo cifra base
                        
                    
                    subtotal = valor + adicional
                    subtotal = round(subtotal,2)

                    if fecha != cifra.mes+cifra.anio:#compruebo si hay deudas por mora
                        mora = valoresbase.porcentaje_mora*subtotal/100
                        pendiente = pendiente + subtotal# solo para imprimir en factuta
                        subtotal = subtotal + mora#sumo el valor adicional por pasarce al otro mes
                        fechamora.append(cifra.mes)
                        auxmora = auxmora+mora    
                    
                    total = total + subtotal
                    total = round(total,2)
        apellido = ""
        if cliente.apellidos != None:
            apellido = cliente.apellidos
        if total == 0:
            mensaje ="El medidor "+str(cliente.medidor)+" correspondiente a "+cliente.nombres+" "+str(apellido)+" no cuenta con deudas pendientes del servicio."
        else:
            mensaje ="El medidor "+str(cliente.medidor)+" tiene una deuda de $"+str(total)+", correspondiente a "+cliente.nombres+" "+str(apellido)+"." 
        return render(request, "buscarDeuda.html",{"mensaje":mensaje})
    else:
        mensaje = "No se encontraron resultados para el medidor "+str(medidor)+". Intente ingresar el número correctamente!"
        return render(request, "buscarDeuda.html",{"mensaje":mensaje}) 