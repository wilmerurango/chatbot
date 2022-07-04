from itertools import count
from traceback import print_tb
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import  CreateView
from django.http import  HttpResponseRedirect
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

from datetime import datetime

from .forms import *
from .models import *
# Create your views here.


def chat(request, id_):
    conversacion = Conversacion.objects.filter(Q(user__username = "Bot")|Q(user__username=request.user.username), curso_id = id_)
    cont_msj_conversacion = conversacion.count()

    # inicio --- enviar mensaje de inicio
    if cont_msj_conversacion == 0:
        msj_welcome = Conversacion()
        msj_welcome.user = User.objects.get(username = "Bot")
        msj_welcome.curso = Curso.objects.get(id = id_)
        msj_welcome.mensaje = "Bienvenido "+str(request.user)+", mi nombre es TIBO y te ayudare a cumplir con exito el plan de estudio del curso: "+str(msj_welcome.curso.nombre_curso)
        msj_welcome.fecha = datetime.today()
        msj_welcome.save()

        msj_pregun_ini = Conversacion()
        msj_pregun_ini.user = User.objects.get(username = "Bot")
        msj_pregun_ini.curso = Curso.objects.get(id = id_)
        msj_pregun_ini.mensaje = "¿ Quieres Iniciar ya ?"
        msj_pregun_ini.fecha = datetime.today()
        msj_pregun_ini.save()
    # fin --- enviar mensaje de inicio
    # inicio --- continuar con la conversacion
    else: 
        pass
    # inicio --- continuar con la conversacion

    conversacion = Conversacion.objects.filter(Q(user__username = "Bot")| Q(user__username =request.user.username), curso_id = id_)
 
    contex = {'conversacions':conversacion}
    
    return render(request, 'base/chat.html',contex)



def index(request):
    curso = Curso.objects.all()
    inscripcion = Inscripcion.objects.filter(user__username = request.user)
    lista_curso_user_actual = [ inscripc.curso.nombre_curso for inscripc in  inscripcion ]

    contexto = {'cursos':curso, 'inscripciones':lista_curso_user_actual}
    return render(request, 'base/index.html',contexto)



class Register(CreateView): #crear usuario
    model = settings.AUTH_USER_MODEL
    template_name = 'base/register.html'
    form_class = UserForm
    success_url = reverse_lazy('index')

    def post(self, request, *args, **kwargs):

        self.object = self.get_object
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit =False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return render(request,'base/register.html')



# @method_decorator(csrf_exempt)
# def Create_Curso(request):
#     # if request.method == 'POST' :
#     form = CursoForm(request.POST)
#     #     if form.is_valid(): 
#     #         form.save()
#     #     return redirect('Curso')
#     # else:
#     #     form = CursoForm()
#     return render(request, 'vistas/curso_form.html', {'form':form})

# @csrf_exempt
class Create_Curso(CreateView): #crear usuario
    model = Curso
    template_name = 'vistas/curso_form.html'
    form_class = CursoForm
    success_url = reverse_lazy('Create_Curso')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cursos'] = Curso.objects.all()
        print(context['cursos'])
        return context
        


class Create_TipoActividad(CreateView): #crear usuario
    model = TipoActividad
    template_name = 'vistas/tipoActividad_form.html'
    form_class = TipoActividadForm
    success_url = reverse_lazy('Create_TipoActividad')


class Create_Tema(CreateView): #crear usuario
    model = Tema
    template_name = 'vistas/tema_form.html'
    form_class = TemaForm
    success_url = reverse_lazy('Create_Tema')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['temas'] = Tema.objects.all()
        return context


class Create_Subtema(CreateView): #crear usuario
    model = Subtema
    template_name = 'vistas/subtema_form.html'
    form_class = SubtemaForm
    success_url = reverse_lazy('Create_Subtema')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subtemas'] = Subtema.objects.all()
        return context


class Create_CurTemStem(CreateView): #crear usuario
    model = CurTemStem
    template_name = 'vistas/curTemStem_form.html'
    form_class = CurTemStemForm
    success_url = reverse_lazy('Create_CurTemStem')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['curtemstems'] = CurTemStem.objects.all()
        return context


class Create_Actividad(CreateView): #crear usuario
    model = Actividad
    template_name = 'vistas/actividad_form.html'
    form_class = ActividadForm
    success_url = reverse_lazy('Create_Actividad')


class Create_ActividadDet(CreateView): #crear usuario
    model = ActividadDet
    template_name = 'vistas/actividadDet_form.html'
    form_class = ActividadDetForm
    success_url = reverse_lazy('Create_ActividadDet')


class Create_ActDetOpt(CreateView): #crear usuario
    model = ActDetOpt
    template_name = 'vistas/ActDetOpt_form.html'
    form_class = ActDetOptForm
    success_url = reverse_lazy('Create_ActDetOpt')


def Create_Inscripcion(request, id_):
    usuario = User.objects.get(username = request.user.username)
    curso = Curso.objects.get(id = id_)
    instancia = Inscripcion()
    instancia.user = usuario
    instancia.curso = curso
    instancia.estado = 1

    # print(instancia)
    if request.method == 'POST' :
        form = InscripcionForm(request.POST)
        if form.is_valid(): 
            form.save()
        return redirect('/chat/'+str(id_)+'/')
    else:
        form = InscripcionForm(instance = instancia)
    return render(request, 'vistas/inscripcion_form.html', {'form':form})

class Create_Inscripcion_Admin(CreateView): #crear usuario
    model = Inscripcion
    template_name = 'vistas/inscripcion_admin_form.html'
    form_class = InscripcionForm
    success_url = reverse_lazy('Create_Inscripcion_Admin')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['inscipcions'] = Inscripcion.objects.all()
        return context




class Create_Progreso(CreateView): #crear usuario
    model = Progreso
    template_name = 'vistas/progreso_form.html'
    form_class = ProgresoForm
    success_url = reverse_lazy('Create_Progreso')


class Create_ProgresoDet(CreateView): #crear usuario
    model = ProgresoDet
    template_name = 'vistas/progresoDet_form.html'
    form_class = ProgresoForm
    success_url = reverse_lazy('Create_ProgresoDet')