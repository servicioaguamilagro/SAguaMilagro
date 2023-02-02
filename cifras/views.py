from django.shortcuts import render
from django.shortcuts import redirect
from django.http import Http404
from django.contrib import messages
from django.utils.translation import gettext as _
from django.db.models import Q
from clientes.models import Cliente
from configuraciones.models import ValoresBase
from .models import Cifras
import datetime

# Create your views here.
def seleccion_clientes(request):
    busqueda = request.GET.get("buscar")
    filtro = request.GET.get("filtro")
    try:
        clientes = Cliente.objects.all()
    except Cliente.DoesNotExist:
        raise Http404
    #para obtener el año y mes
    date = datetime.date.today()
    año = date.strftime("%Y")
    mes = date.strftime("%B")
    fecha = mes+año
    try:
        if busqueda and (str(filtro)=='1' or str(filtro)=='2'):
            if str(filtro) == '2':
                    clientes = Cliente.objects.filter(
                        Q(ultima_cifra__icontains = fecha)).filter(
                        Q(nombres__icontains = busqueda) |
                        Q(apellidos__icontains = busqueda)|
                        Q(medidor__icontains = busqueda) | 
                        Q(cedula__icontains = busqueda) 
                    ).distinct()
                    messages.success(request, "los resultados para la busqueda "+busqueda+" y el filto 'cifras ingresadas' son:")
            if str(filtro) == '1':
                clientes = Cliente.objects.filter(
                    Q(nombres__icontains = busqueda) |
                    Q(apellidos__icontains = busqueda)|
                    Q(medidor__icontains = busqueda) | 
                    Q(cedula__icontains = busqueda) 
                ).exclude(
                    Q(ultima_cifra__icontains = fecha)).distinct()
                messages.success(request, "los resultados para la busqueda "+busqueda+" y el filto 'cifras por ingresar' son:")
        else:
            if busqueda:
                messages.success(request, " Los resultados encontrados para la busqueda '"+busqueda+"' son:")
                clientes = Cliente.objects.filter(
                    Q(nombres__icontains = busqueda) |
                    Q(apellidos__icontains = busqueda)|
                    Q(medidor__icontains = busqueda) | 
                    Q(cedula__icontains = busqueda) 
                ).distinct()
                
            if filtro:
                if str(filtro) == '2':
                    clientes = Cliente.objects.filter(
                        Q(ultima_cifra__icontains = fecha)).distinct()
                    messages.success(request, "Los usuarios con cifras actualizadas son:")
                if str(filtro) == '1':
                    clientes = Cliente.objects.exclude(
                        Q(ultima_cifra__icontains = fecha)).distinct()
                    messages.success(request, "Los usuarios con cifras sin ingresar son:")
    except Cliente.DoesNotExist:
                raise Http404
    return render(request, "cifras.html", {"clientes": clientes,"filtro":filtro,"fecha":fecha,"mes":mes, "año":año})

def ingresar_cifra(request, id):
    try:
        cliente = Cliente.objects.get(id=id)
    except Cliente.DoesNotExist:
                raise Http404
    #para obtener el año y mes
    date = datetime.date.today()
    año = date.strftime("%Y")
    mes = date.strftime("%B")
    fecha_ucifra = mes+año
    #para filtar y mostrar las cifras de cada usuario    
    tcifras = Cifras.objects.filter(id_usuario = cliente).distinct()
    #para obtener el ultimo mes ingresado
    for cifras in tcifras.iterator():
        ultimomes = cifras.mes
    if len(tcifras) == 0: #ayuda a combertir el dato si no hay elementos en la tupla
        ultimomes=""
    #para obtener el ultimo registro de los valores base
    try:
        idv = ValoresBase.objects.latest('id')
        valores = ValoresBase.objects.get(id=idv.id)
    except ValoresBase.DoesNotExist:
        messages.success(request, "Asegurese que esten ingresados los valores base, lo puede realizar en configuraciones!")
        return redirect("/cifras/")
    #agregar una nueva cifra
    if request.method == 'POST':
        #obtengo cifra ingresada en pantalla
        cifra = request.POST.get("cifra")
        # obtener la ultima cifra
        longitud = len(tcifras)
        if longitud != 0:
            utimacifra = tcifras[longitud-1]
            auxcifra = int(utimacifra.cifra)
        else:
            auxcifra = 0
        print(auxcifra)
        print(cifra)
        if auxcifra < int(cifra):
            #guardo valores
            c =Cifras()
            c.id_usuario = cliente
            c.mes = mes
            c.anio = año
            c.cifra = cifra
            c.id_valores = valores.id   
            c.estado = 'n'
            if cifra != "":
                if c.save() != True:
                    messages.success(request, "La cifra '"+cifra+"' del mes de "+_(mes)+" - "+año+" del usuario "+cliente.nombres+ " a sido agregada correctamente!")
                    #actualizo el campo del mes ingresado a la bd clientes
                    cliente.ultima_cifra = fecha_ucifra
                    cliente.deuda = 's'
                    cliente.save()
                    return redirect("/cifras/")
            else:
                messages.success(request, "A ocurrido un error! El campo esta vacio.")
        else:
            messages.success(request, "La cifra actual debe ser mayor a la anterior ingresada, o a 0.")
    
    context = {
        "cliente":cliente,
        "año":año,
        "mes":mes,
        "umes":ultimomes,
        "tcifras":reversed(tcifras),
    }
    return render(request, "ingresarCifra.html", context)

def editar_cifras(request, id):
    cifra = Cifras.objects.get(id=id)
    cliente = Cliente.objects.get(medidor=cifra.id_usuario)
    return render(request, "editarCifra.html", {"cliente": cliente,"cifra":cifra})

def actualizar_cifra(request, id):
    try:
        c = Cifras.objects.get(id=id)
    except Cifras.DoesNotExist:
        raise Http404
    try:
        cliente = Cliente.objects.get(medidor=c.id_usuario)
    except Cliente.DoesNotExist:
        raise Http404
    
    ruta = '/ingresarcifra/'
    ruta = ruta+str(cliente.id)
    print (ruta)
    if request.method == 'POST':
        #para comprobar que no se ingresen cifras menores a la anterior
        tcifras = Cifras.objects.filter(id_usuario = cliente).distinct()
        longitud = len(tcifras)
        if longitud != 0:
            utimacifra = tcifras[longitud-1]
            auxcifra = int(utimacifra.cifra)
        else:
            auxcifra = 0
        #obtengo cifra ingresada
        cifra = request.POST.get("cifra")
        if auxcifra < int(cifra):
            
            if cifra != "":
                c.cifra = int(cifra)
                if c.save() != True:
                    messages.success(request, "La cifra '"+cifra+"' del mes de "+_(c.mes)+" - "+c.anio+" del usuario "+cliente.nombres+ " a sido actualizada correctamente!")
            else:
                messages.success(request, "A ocurrido un error! El campo esta vacio.")
        else:
            messages.success(request, "La cifra actual debe ser mayor a la anterior ingresada, o a 0.")
            r = '/editarcifra/'
            r = r+str(c.id)
            return redirect(r)
    
    return redirect(ruta)

