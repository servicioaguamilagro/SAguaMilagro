from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib import messages
from clientes.models import Cliente
from django.db.models import Q
import datetime
from .models import Notificaciones
from cifras.models import Cifras
from django.conf import settings
from django.core.mail import send_mail

# Create your views here.
def notificaciones(request,):
    busqueda = request.GET.get("buscar")
    filtro = request.GET.get("filtro")
    date = datetime.date.today()
    año = date.strftime("%Y")
    mes = date.strftime("%B")
    fecha = mes+año
    try:
        notificacion = Notificaciones.objects.all()
        clientes = Cliente.objects.filter(
                Q(deuda__icontains = 's') 
            ).distinct()
    except:
        raise Http404
    try:
        if (str(filtro)=='1' or str(filtro)=='2') and busqueda:
            if str(filtro) == '1':
                clientes = Cliente.objects.filter(deuda = 's').filter(detalle = fecha).filter(
                    Q(nombres__icontains = busqueda) |
                    Q(apellidos__icontains = busqueda)|
                    Q(medidor__icontains = busqueda) | 
                    Q(cedula__icontains = busqueda) 
                ).distinct()
                messages.success(request, "Los resultados para la busqueda '"+busqueda+"' y el filtro 'Notificados' son:")
            if str(filtro) == '2':
                clientes = Cliente.objects.filter(deuda = 's').exclude(detalle__icontains = fecha).filter(
                        Q(nombres__icontains = busqueda) |
                        Q(apellidos__icontains = busqueda)|
                        Q(medidor__icontains = busqueda) | 
                        Q(cedula__icontains = busqueda) 
                    ).distinct()
                messages.success(request, "Los resultados para la busqueda '"+busqueda+"' y el filtro 'Sin notificar' son:")
        else:
            if filtro:
                if str(filtro) == '1':
                    clientes = Cliente.objects.filter(deuda = 's').filter(detalle = fecha).distinct()
                    messages.success(request, "Los usuarios que se han notificado son:")
                if str(filtro) == '2':
                    clientes = Cliente.objects.filter(deuda = 's').exclude(detalle__icontains = fecha).distinct()
                    messages.success(request, "Los usuarios por notificar son:")
            if busqueda:
                messages.success(request, " Los resultados encontrados para la busqueda '"+busqueda+"' son:")
                clientes = Cliente.objects.filter(deuda = 's').filter(
                    Q(nombres__icontains = busqueda) |
                    Q(apellidos__icontains = busqueda)|
                    Q(medidor__icontains = busqueda) | 
                    Q(cedula__icontains = busqueda) 
                ).distinct()
    except Cliente.DoesNotExist:
        raise Http404            
    try:
        cifras = Cifras.objects.filter(
                Q(estado__icontains = 'n') 
            ).distinct()
        notificart = ''
    except Cifras.DoesNotExist:
        raise Http404
    for c in clientes:#para desabilitar el boton enviar
        if c.detalle != fecha:
            notificart = notificart+str(c.detalle)
    return render(request, "notificaciones.html", {"clientes":clientes,"cifras":cifras, "fecha":fecha,"notificacion":notificacion,"notificart":notificart})

def notificar_usuario(request, id):
    try:
        cliente = Cliente.objects.get(id=id)
    except Cliente.DoesNotExist:
        raise Http404
    notificacion = Notificaciones()
    date = datetime.date.today()
    notificacion.id_usuario = cliente
    notificacion.fecha = date
    año = date.strftime("%Y")
    mes = date.strftime("%B")
    fecha = mes+año
    cliente.detalle = fecha
    #correo
    cifras = Cifras.objects.filter(
            Q(estado__icontains = 'n') 
        ).distinct()
    mesesdeuda = ''
    for c in cifras:
        if cliente == c.id_usuario:
            mesesdeuda = mesesdeuda + " " + c.mes
    #para llenar apellidos vacios
    if cliente.apellidos is None:
        apellido = ""
    else:
        apellido = str(cliente.apellidos)
    subject = "Pago pendiente por el servicio de Agua Potable - GAD Parroquial de Milagro"
    message = "Estimado usuario "+cliente.nombres+" "+ apellido +" - medidor: "+str(cliente.medidor)+", acercarse a cancelar los valores pendientes por el servicio de Agua Potable. Los valores pendientes repercuten en suspención del servicio."
    from_email=settings.EMAIL_HOST_USER
    recipient_list=[cliente.email]
    send_mail(subject, message, from_email, recipient_list)
    notificacion.id_usuario = cliente
    notificacion.fecha = date
    if notificacion.save() != True:
        if cliente.save() != True:
            messages.success(request, "Se ha notificado la deuda pendiente al correo "+cliente.email+" de "+cliente.nombres+"")
    
    return redirect('/notificaciones/')

def notificar_todos(request,):
    date = datetime.date.today()
    año = date.strftime("%Y")
    mes = date.strftime("%B")
    fecha = mes+año
    try:
        clientes = Cliente.objects.filter(
                Q(deuda__icontains = 's') 
            ).distinct()
        cifras = Cifras.objects.filter(
                Q(estado__icontains = 'n') 
            ).distinct()
    except:
        raise Http404
    notificacion = Notificaciones()
    for cliente in clientes:
        if cliente.detalle != fecha:
            cliente.detalle = fecha#actualizo la variable de control
            mesesdeuda = ''#reinicio la variable para los meses pendientes
            for c in cifras:
                if cliente == c.id_usuario:
                    mesesdeuda = mesesdeuda + " " + c.mes
            #para llenar apellidos vacios
            if cliente.apellidos is None:
                apellido = ""
            else:
                apellido = str(cliente.apellidos)
            #correo
            subject = "Pago pendiente por el servicio de Agua Potable - GAD Parroquial de Milagro"
            message = "Estimado usuario "+cliente.nombres+" "+ apellido +" - medidor: "+str(cliente.medidor)+", acercarse a cancelar los valores pendientes por el servicio de Agua Potable. Las deudas pendientes repercuten en suspención del servicio."
            from_email=settings.EMAIL_HOST_USER
            recipient_list=[cliente.email]
            send_mail(subject, message, from_email, recipient_list)
            notificacion.id_usuario = cliente
            notificacion.fecha = date
            if notificacion.save() != True:
                if cliente.save() != True:
                    print(notificacion)
    
    messages.success(request, "Se ha notificado al correo de cada uno de los usuarios su deuda pendiente.")                
    
    return redirect('/notificaciones/')
