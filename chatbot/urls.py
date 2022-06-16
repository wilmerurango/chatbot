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


    path('chat/<int:id_>/', login_required(chat), name="chat"),
    path('index', login_required(index), name="index"),

    path('',LoginView.as_view(), name ='login'),
    path('logout/',LogoutView.as_view(), name ='logout'),
    path('register', Register.as_view(), name="register"),

    path('Create_Curso/', Create_Curso.as_view(), name="Create_Curso"),
    path('Create_TipoActividad/', Create_TipoActividad.as_view(), name="Create_TipoActividad"),
    path('Create_Tema/', Create_Tema.as_view(), name="Create_Tema"),
    path('Create_Subtema/', Create_Subtema.as_view(), name="Create_Subtema"),
    path('Create_CurTemStem/', Create_CurTemStem.as_view(), name="Create_CurTemStem"),
    path('Create_Actividad/', Create_Actividad.as_view(), name="Create_Actividad"),
    path('Create_ActividadDet/', Create_ActividadDet.as_view(), name="Create_ActividadDet"),
    path('Create_ActDetOpt/', Create_ActDetOpt.as_view(), name="Create_ActDetOpt"),
    path('Create_Inscripcion/<int:id_>/', Create_Inscripcion, name="Create_Inscripcion"),
    path('Create_Inscripcion_Admin/', Create_Inscripcion_Admin.as_view(), name="Create_Inscripcion_Admin"),
    path('Create_Progreso/', Create_Progreso.as_view(), name="Create_Progreso"),
    path('Create_ProgresoDet/', Create_ProgresoDet.as_view(), name="Create_ProgresoDet"),


    path('accounts/',include('django.contrib.auth.urls')),


]
if settings.DEBUG: urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 