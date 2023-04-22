"""AppAguaMilagro URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from home.views import home, cerrar_sesion, info_correo, superUser, calcular_valores
from clientes.views import crear_cliente, listar_clientes, editar_cliente, actualizar_cliente, ver_cliente, eliminar_cliente, confirmar_eliminar_cliente
from cifras.views import seleccion_clientes,ingresar_cifra, editar_cifras, actualizar_cifra
from cobros.views import mostrar_clientes, calcular_cobro, GeneratePdf
from notificaciones.views import notificaciones, notificar_usuario, notificar_todos
from configuraciones.views import configuraciones, nuevo_administrador, nuevos_valores, actualizar_usuario,eliminar_usuario, listar_clienteseliminados, restablecer
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    #Para la app home
    path('', home, name="home"),
    path('infocorreo/', info_correo),
    path('logout/', cerrar_sesion, name="logout"),
    path('buscardeuda/', calcular_valores),
    #Para la app clientes
    path('crearcliente/', crear_cliente, name="crearcliente"),
    path('clientes/', listar_clientes, name="listarclientes"),
    path('editarcliente/<int:id>',editar_cliente),
    path('actualizarcliente/<int:id>',actualizar_cliente),
    path('vercliente/<int:id>',ver_cliente),
    path('eliminarcliente/<int:id>',eliminar_cliente),
    path('confirmareliminarcliente/<int:id>',confirmar_eliminar_cliente),
    #Para la app cifras
    path('cifras/', seleccion_clientes),
    path('ingresarcifra/<int:id>',ingresar_cifra),
    path('editarcifra/<int:id>',editar_cifras),
    path('actualizarcifra/<int:id>',actualizar_cifra),
    #Para la app cobros
    path('cobros/',mostrar_clientes),
    path('calcularcobro/<int:id>',calcular_cobro),
    path('generarpdf/<int:id>',GeneratePdf.as_view(),name='pdf'),
    #para las notificaciones
    path('notificaciones/',notificaciones),
    path('notificarusuario/<int:id>',notificar_usuario),
    path('notificartodos/',notificar_todos),
    #configuraciones
    path('configuraciones/',configuraciones),
    path('nuevoadministrador/',nuevo_administrador),
    path('valoresbase/',nuevos_valores),
    path('actualizarusuario/<int:id>',actualizar_usuario),
    path('eliminarusuario/',eliminar_usuario),
    path('superuser/',superUser),
    path('recuperarusuario/',listar_clienteseliminados),
    path('restablecerusuario/<int:id>',restablecer),
    #reseteo contraseñas
    path('reset_password/',auth_views.PasswordResetView.as_view(template_name="contraseñaResetear.html"), name='password_reset'),
    path('reset_password_send/',auth_views.PasswordResetDoneView.as_view(template_name="contraseñaEnvio.html"), name='password_reset_done'),
    path('reset/<uidb64>/<token>',auth_views.PasswordResetConfirmView.as_view(template_name="contraseñaNueva.html"),name='password_reset_confirm'),
    path('reset_password_complete',auth_views.PasswordResetCompleteView.as_view(template_name="contraseñaCompletado.html"),name='password_reset_complete'),
]
