"""chatbot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
 

from appbot.views import *

urlpatterns = [
    path('admin/', admin.site.urls),

    # Start enlaces del chat
    path('chat/<int:id_>/', login_required(chat), name="chat"),
    path('msj_user/', login_required(msj_user), name="msj_user"),
    path('ConsulTema/<int:id_>/', login_required(ConsulTema), name="ConsulTema"),
    path('ConsulSubTema/<int:id_>/', login_required(ConsulSubTema), name="ConsulSubTema"),
    path('ConsulDetSubtema/<int:pk>/', login_required(ConsulDetSubtema), name='ConsulDetSubtema'),
    # End  enlaces del chat



    path('index/', login_required(index), name="index"),

    path('',LoginView.as_view(), name ='login'),
    path('logout/',LogoutView.as_view(), name ='logout'),
    path('register', Register.as_view(), name="register"),

    path('Create_Curso/', Create_Curso.as_view(), name="Create_Curso"),
    path('Update_Curso/<int:pk>/', Update_Curso.as_view(), name="Update_Curso"),

    path('Create_TipoActividad/', Create_TipoActividad.as_view(), name="Create_TipoActividad"),
    path('Update_TipoActividad/<int:pk>/', Update_TipoActividad.as_view(), name="Update_TipoActividad"),

    path('Create_Tema/', Create_Tema.as_view(), name="Create_Tema"),
    path('Update_Tema/<int:pk>/', Update_Tema.as_view(), name="Update_Tema"),

    path('Create_Subtema/', Create_Subtema.as_view(), name="Create_Subtema"),
    path('Update_Subtema/<int:pk>/', Update_Subtema.as_view(), name="Update_Subtema"),

    path('Create_SubSubtema/', Create_SubSubtema.as_view(), name="Create_SubSubtema"),
    path('Update_SubSubtema/<int:pk>/', Update_SubSubtema.as_view(), name="Update_SubSubtema"),

    path('Create_CurTemStem/', Create_CurTemStem.as_view(), name="Create_CurTemStem"),
    path('Update_CurTemStem/<int:pk>/', Update_CurTemStem.as_view(), name="Update_CurTemStem"),

    path('Create_Actividad/', Create_Actividad.as_view(), name="Create_Actividad"),
    path('Update_Actividad/<int:pk>/', Update_Actividad.as_view(), name="Update_Actividad"),

    path('Create_Act_Pregunta/', Create_Act_Pregunta.as_view(), name="Create_Act_Pregunta"),
    path('Update_Act_Pregunta/<int:pk>/', Update_Act_Pregunta.as_view(), name="Update_Act_Pregunta"),

    path('Create_Act_Pregunta_Opt/', Create_Act_Pregunta_Opt.as_view(), name="Create_Act_Pregunta_Opt"),
    path('Update_Act_Pregunta_Opt/<int:pk>/', Update_Act_Pregunta_Opt.as_view(), name="Update_Act_Pregunta_Opt"),

    path('Create_Inscripcion/<int:id_>/', Create_Inscripcion, name="Create_Inscripcion"),
    path('Create_Inscripcion_Admin/', Create_Inscripcion_Admin.as_view(), name="Create_Inscripcion_Admin"),
    path('Update_Inscripcion_Admin/<int:pk>/', Update_Inscripcion_Admin.as_view(), name="Update_Inscripcion_Admin"),
    
    path('Create_Progreso/', Create_Prog_Acti.as_view(), name="Create_Progreso"),
    path('Update_Progreso/<int:pk>/', Update_Prog_Acti.as_view(), name="Update_Progreso"),

    path('Create_ProgresoDet/', Create_Prog_Preg.as_view(), name="Create_ProgresoDet"),
    path('Update_ProgresoDet/<int:pk>/', Update_Prog_Preg.as_view(), name="Update_ProgresoDet"),

    path('Create_Cts/', Create_Cts.as_view(), name="Create_Cts"),
    path('Update_Cts/<int:pk>/', Update_Cts.as_view(), name="Update_Cts"),
    
    
    path('Create_Ctsd/', Create_Ctsd.as_view(), name="Create_Ctsd"),
    path('Update_Ctsd/<int:pk>/', Update_Ctsd.as_view(), name="Update_Ctsd"),

    path('send_save_respuesta/', send_save_respuesta, name="send_save_respuesta"),

    # path('Create_Prog_Tem/', Create_Prog_Tem.as_view(), name="Create_Prog_Tem"),
    # path('Update_Prog_Tem/<int:pk>/', Update_Prog_Tem.as_view(), name="Update_Prog_Tem"),

    # path('Create_Prog_Stem/', Create_Prog_Stem.as_view(), name="Create_Prog_Stem"),
    # path('Update_Prog_Stem/<int:pk>/', Update_Prog_Stem.as_view(), name="Update_Prog_Stem"),

    # path('Create_Prog_Sstem/', Create_Prog_Sstem.as_view(), name="Create_Prog_Sstem"),
    # path('Update_Prog_Sstem/<int:pk>/', Update_Prog_Sstem.as_view(), name="Update_Prog_Sstem"),

    # listas dependientes
    path('list_subtema/', list_subtema, name="list_subtema"),
    path('list_subSubtema/', list_subSubtema, name="list_subSubtema"),
    path('list_cts/', list_cts, name="list_cts"),
    path('list_ctsd/', list_ctsd, name="list_ctsd"),

    path('accounts/',include('django.contrib.auth.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 