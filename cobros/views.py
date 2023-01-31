from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from django.db.models import Q
from django.views.generic import View
from clientes.models import Cliente
from cifras.models import Cifras 
from .models import Cobros
from configuraciones.models import ValoresBase
from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import get_template
from decimal import Decimal
import datetime
#pdf
from cobros.utils import render_to_pdf

# Create your views here.
def mostrar_clientes(request):
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
        if str(busqueda) and (str(filtro)=='1' or str(filtro)=='2'):
            if str(filtro) == '1':
                    clientes = Cliente.objects.filter(
                        Q(deuda__icontains = 's')).filter(
                        Q(nombres__icontains = busqueda) |
                        Q(apellidos__icontains = busqueda)|
                        Q(medidor__icontains = busqueda) | 
                        Q(cedula__icontains = busqueda) 
                    ).distinct()
                    messages.success(request, "Los resultados para la busqueda '"+busqueda+"' y el filtro 'Deudas pendientes' son:")
            if str(filtro) == '2':
                clientes = Cliente.objects.filter(
                    Q(deuda__icontains = 'n')).filter(
                    Q(nombres__icontains = busqueda) |
                    Q(apellidos__icontains = busqueda)|
                    Q(medidor__icontains = busqueda) | 
                    Q(cedula__icontains = busqueda) 
                ).distinct()
                messages.success(request, "Los resultados para la busqueda '"+busqueda+"' y el filtro 'Usuarios cancelados' son:")
        else:
            if filtro:
                if str(filtro) == '1':
                    clientes = Cliente.objects.filter(
                        Q(deuda__icontains = 's')).distinct()
                    messages.success(request, "Los usuarios con deudas pendientes son: ")
                if str(filtro) == '2':
                    clientes = Cliente.objects.filter(
                        Q(deuda__icontains = 'n')).distinct()
                    messages.success(request, "Los usuarios que han cancelado son: ")
        
            if busqueda:
                messages.success(request, " Los resultados encontrados para la busqueda '"+busqueda+"' son:")
                clientes = Cliente.objects.filter(
                    Q(nombres__icontains = busqueda) |
                    Q(apellidos__icontains = busqueda)|
                    Q(medidor__icontains = busqueda) | 
                    Q(cedula__icontains = busqueda) 
                ).distinct()
    except Cliente.DoesNotExist:
        raise Http404
    return render(request, "cobros.html", {"clientes": clientes,"fecha":fecha})

def calcular_cobro(request, id):
    try:
        cliente = Cliente.objects.get(id=id)
    except Cliente.DoesNotExist:
        raise Http404
    try:
        cifras = Cifras.objects.filter(id_usuario = cliente).distinct()
    except Cifras.DoesNotExist:
        raise Http404
    print('**************************************************')
    print(cifras)
    print('**************************************************')
    auxcifra =0
    #para obtener el año y mes
    date = datetime.date.today()
    año = date.strftime("%Y")
    mes = date.strftime("%B")
    fecha = mes+año
    total =0
    mora = 0
    pendiente = 0
    fechamora = ""
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
            metrosadicionales = 0
            print("----------------------")
            print(cifra.mes+" "+cifra.anio)
            print("cifra consumida: ")
            print(cifr)
            print("Valor de la base: ")
            print(valor)
            
            if cifr > valoresbase.base:#para calcular el adicional si se psa de la base
                metrosadicionales = (cifr-valoresbase.base)#solo para mostrar en factura
                adicional = (cifr-valoresbase.base)*valoresbase.valor_adicional
                auxcifra =cifr#actualizo cifra base
            else:
                adicional = 0
                subtotal = valor + adicional
                auxcifra =cifr#actualizo cifra base
            
            subtotal = valor + adicional

            if fecha != cifra.mes+cifra.anio:#compruebo si hay deudas por mora
                mora = valoresbase.porcentaje_mora*subtotal/100
                pendiente = pendiente + subtotal# solo para imprimir en factuta
                subtotal = subtotal + mora#sumo el valor adicional por pasarce al otro mes
                fechamora = fechamora +cifra.mes+" "
                auxmora = auxmora+mora    
            
            total = total + subtotal 
            print("Adicional por metros pasados: ")
            print(adicional)
            print("Subtotal: ")
            print(subtotal)
            print("Adicional por mora")
            print(mora)
            print(fechamora)
            print("Total:")
            print(total)
            print(estado)
    if cifras:#cifras no esta vacia
        if estado =='n':#no a pagado
            context = {
                "mes_actual":mes,
                "año_actual":año,
                "mes":cifra.mes,
                "año":cifra.anio,
                "valoresbase":valoresbase,
                "cifraconsumida":cifr,
                "metrosadicionales":metrosadicionales,
                "adicional":adicional,
                "subtotal":subtotal,
                "fechamora":fechamora,
                "pendiente":pendiente,
                "mora":auxmora,
                "total":total,
                "cliente":cliente,
                "estado":estado,
            }
        else:
            try:
                registrocobros = Cobros.objects.filter(id_usuario = cliente).distinct()
            except Cobros.DoesNotExist:
                raise Http404
            
            context ={"cliente":cliente,"estado":estado,"ultimopago":ultimopago,"registrocobros":reversed(registrocobros)}
    else:#vacia
        context ={"cliente":cliente,}
    return render(request, "generarpago.html", context)

class GeneratePdf(View):
    def get(self, request, *args, **kwargs):
        for key, id in kwargs.items():
            print(id)
        try:
            cliente = Cliente.objects.get(id=id)
        except Cliente.DoesNotExist:
                raise Http404
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
        fechamora = ""
        auxmora = 0
        for cifra in cifras:#recorre cifra por cifra del usuario
            if cifra.estado == 's':#comprueba si la cifra a sido pagada  
                auxcifra =cifra.cifra#almacena la ultima cifra pagada
            else:
                cifr = cifra.cifra-auxcifra#calcula la cifra para realizar mas calculos
                valoresbase = ValoresBase.objects.get(id=cifra.id_valores)
                valor = valoresbase.valor_cifra_base
                subtotal = 0.0
                metrosadicionales = 0

                if cifr > valoresbase.base:#para calcular el adicional si se psa de la base
                    metrosadicionales = (cifr-valoresbase.base)#solo para mostrar en factura
                    adicional = (cifr-valoresbase.base)*valoresbase.valor_adicional
                    auxcifra =cifr#actualizo cifra base
                else:
                    adicional = 0
                    subtotal = valor + adicional
                    auxcifra =cifr#actualizo cifra base
                
                subtotal = valor + adicional

                if fecha != cifra.mes+cifra.anio:#compruebo si hay deudas por mora
                    mora = valoresbase.porcentaje_mora*subtotal/100
                    pendiente = pendiente + subtotal# solo para imprimir en factuta
                    subtotal = subtotal + mora#sumo el valor adicional por pasarce al otro mes
                    fechamora = fechamora +cifra.mes+" "
                    auxmora = auxmora+mora    
                
                total = total + subtotal 
                print("Adicional por metros pasados: ")
                print(adicional)
                print("Subtotal: ")
                print(subtotal)
                print("Adicional por mora")
                print(mora)
                print(fechamora)
                print("Total:")
                print(total)
        try:
            context = {
                "tiempo":date,
                "mes_actual":mes,
                "año_actual":año,
                "mes":cifra.mes,
                "año":cifra.anio,
                "valoresbase":valoresbase,
                "cifraconsumida":cifr,
                "metrosadicionales":metrosadicionales,
                "adicional":adicional,
                "subtotal":subtotal,
                "fechamora":fechamora,
                "pendiente":pendiente,
                "mora":auxmora,
                "total":total,
                "cliente":cliente,
            }
        except:
            raise Http404
        template_name="recibo.html"
        pdf = render_to_pdf(template_name,context)
        
        #enviar correo electronico
        template2 = get_template('recibo.html')
        content = template2.render(context)
        mail = EmailMultiAlternatives(
        subject='Recibo de Pago del Servicio de Agua del GADPR Milagro - '+cifra.mes,
        body='',
        from_email=settings.EMAIL_HOST_USER,
        to=[
            cliente.email
        ],
        cc=[]
        )
        mail.attach_alternative(content,'text/html')
        mail.send(fail_silently=False)

        #actualizar BD
        for cifra in cifras:#recorre cifra por cifra del usuario
            if cifra.estado == 'n':#comprueba si la cifra no a sido pagada  
                cifra.estado = 's'#cambia el estado de la cifra
                try:
                    cifra.save()
                except:
                    raise Http404
        cliente.deuda = 'n'
        try:
            cliente.save()
        except:
                raise Http404
        #Registrar cobro
        cobro = Cobros()
        cobro.id_usuario = cliente
        cobro.registro = date
        cobro.fechacifra = cifra.mes+cifra.anio
        cobro.total = total
        if cobro.save() != True:
            messages.success(request, "El pago de "+cifra.mes+" del "+cifra.anio+" a sido registrado correctamente! Se a enviado el recibo de pago al correo "+cliente.email+" y lo puede descargar en la nueva pestaña generada.")
        else:
            messages.success(request,"Ha ocurrido un error inesperado!")
        return HttpResponse(pdf,content_type='application/pdf')

