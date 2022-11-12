import json

from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import  CreateView
from django.views.generic.edit import UpdateView
from django.http import  HttpResponseRedirect
from django.conf import settings
from django.http import JsonResponse
from django.core import serializers

from datetime import datetime

from .forms import *
from .models import *

def calculo_progreso(inscripcion_curso):

    tema_prog = Prog_Tem.objects.filter(inscripcion__id = inscripcion_curso.id).order_by('orden')#progreso de temas de la inscripcion actual
    tema_curso = CurTemStem.objects.filter(curso__id = inscripcion_curso.curso.id).order_by('orden')

    try:
        cont_subtema_curso= 0
        for i in tema_curso:
            tem_subtema = Cts.objects.filter(curTemStem__id = i.id)
            for j in tem_subtema:
                tem_sub_subtema = Ctsd.objects.filter(cts__id = j.id)
                for k in tem_sub_subtema:
                    cont_subtema_curso += 1

        print('contador curso',cont_subtema_curso)

        cont_subtema_prog= 0
        for i in tema_prog:
            tem_subtema_prog = Prog_Stem.objects.filter(prog_Tem__id = i.id)
            for j in tem_subtema_prog:
                tem_sub_subtema_prog = Prog_Sstem.objects.filter(prog_Stem__id = j.id)
                for k in tem_sub_subtema_prog:
                    cont_subtema_prog += 1

        print('contador progreso',cont_subtema_prog)
        progreso_avance = int(round((cont_subtema_prog/cont_subtema_curso)*100,0))
    except:
        progreso_avance = int(0)

    return progreso_avance



def chat(request, id_):
    # id_: esta es el id del curso inscrito

    inscripcion_curso = Inscripcion.objects.get(curso__id = id_, user__username=request.user.username)
    # print("inscripcion: ",inscripcion_curso)

    conversacion = Conversacion.objects.filter(inscripcion__id = inscripcion_curso.id)
    cont_msj_conversacion = conversacion.count()

    # inicio --- enviar mensaje de inicio
    if cont_msj_conversacion == 0:
        msj_welcome = Conversacion()
        msj_welcome.user = User.objects.get(username = "Bot")
        msj_welcome.curso = Curso.objects.get(id = id_)
        msj_welcome.mensaje = "Bienvenido "+str(request.user)+", mi nombre es TIBO y te ayudare a cumplir con exito el plan de estudio del curso: "+str(msj_welcome.curso.nombre_curso)
        msj_welcome.fecha = datetime.today()
        msj_welcome.tipo_mensje = "Texto"
        msj_welcome.inscripcion = inscripcion_curso
        msj_welcome.title = ""
        msj_welcome.save()

        msj_welcome2 = Conversacion()
        msj_welcome2.user = User.objects.get(username = "Bot")
        msj_welcome2.curso = Curso.objects.get(id = id_)
        msj_welcome2.mensaje = "¿ Quieres Iniciar ya ?"
        msj_welcome2.fecha = datetime.today()
        msj_welcome2.tipo_mensje = "Texto"
        msj_welcome2.inscripcion = inscripcion_curso
        msj_welcome2.title = ""
        msj_welcome2.save()
    # fin --- enviar mensaje de inicioss

    conversacion = Conversacion.objects.filter(inscripcion__id = inscripcion_curso.id)
    conversacion = serializers.serialize('json',conversacion)
    users = serializers.serialize('json',User.objects.all())
    print('usuarios :',User.objects.all()[0].id )

    tema_prog = Prog_Tem.objects.filter(inscripcion__id = inscripcion_curso.id).order_by('orden')#progreso de temas de la inscripcion actual
    tema_curso = CurTemStem.objects.filter(curso__id = inscripcion_curso.curso.id).order_by('orden')
    paso_sgt = '#'


    if tema_prog.count() != 0: 

        last_tema_prog = 0
        last_subtema_prog = 0
        last_sub_subtema_prog = 0


        last_tema_prog = tema_prog.last()

        subtema_prog = Prog_Stem.objects.filter(prog_Tem__id = last_tema_prog.id).order_by('orden')

        if subtema_prog.count() != 0:
            last_subtema_prog = subtema_prog.last()

            sub_subtema_prog = Prog_Sstem.objects.filter(prog_Stem__id = last_subtema_prog.id).order_by('orden')

            if sub_subtema_prog.count() != 0:
                last_sub_subtema_prog = sub_subtema_prog.last()
                        

        if last_sub_subtema_prog != 0:
            paso_sgt = '/ConsulDetSubtema/'+str(last_sub_subtema_prog.prog_Stem.id)+'/'
        elif last_subtema_prog != 0:
            paso_sgt = '/ConsulDetSubtema/'+str(last_subtema_prog.id)+'/'
        elif last_tema_prog != 0:
            paso_sgt = '/ConsulSubTema/'+str(last_tema_prog.id)+'/'
        else:
            paso_sgt = '/#'

    else:
        # if cont_msj_conversacion == 4:
        paso_sgt = '/ConsulTema/'+str(inscripcion_curso.id)+'/'



    # ----- start curso [aqui se arma un diccionario para armar el curso y mostrarlo en el chat]
    curso_completo = {}
    # tem_tema = CurTemStem.objects.all()

    for i in tema_curso:
        
        subtema = {}
        tem_subtema = Cts.objects.filter(curTemStem__id = i.id)
        for j in tem_subtema:

            tem_sub_subtema = Ctsd.objects.filter(cts__id = j.id)
            
            subtema[j.subtema.nombre] = [k.subSubtema.nombre for k in tem_sub_subtema]

        curso_completo[i.tema.nombre_tema] = subtema
    # ----- end curso

    
    progreso_avance = calculo_progreso(inscripcion_curso)


    contex = {  'conversacions':conversacion, 
                'id_curso':id_, 
                'nombre_curso':inscripcion_curso.curso.nombre_curso, 
                'users':users, 
                'siguiente_paso':paso_sgt,
                'curso_completo':curso_completo, 
                'progreso_avance':progreso_avance
            }
    
    return render(request, 'base/chat.html',contex)


#aqui se envia el mensaje del usuario via ajax, para que tenga el efecto append en la interfaz de usuario
#esta funcion se activa cuando el usuario preciona el boton de enviar mensaje en la interfaz del chat
def msj_user(request):

    #CAPTURAR CONTENIDO DEL MENSAJE DEL USUARIO Y EL ID DEL CURSO
    msj = request.GET.get('msj')
    id_ = request.GET.get('id_')

    # GUARDAR EN DB EL MENSAJE ESCRITO POR EL USUARIO
    inscripcion_curso = Inscripcion.objects.get(curso__id = id_, user__username=request.user.username)
    
    msj_welcome = Conversacion()
    msj_welcome.user = User.objects.get(username = request.user.username)
    msj_welcome.curso = Curso.objects.get(id = id_)
    msj_welcome.mensaje = msj
    msj_welcome.fecha = datetime.today()
    msj_welcome.tipo_mensje = "Texto"
    msj_welcome.inscripcion = inscripcion_curso
    msj_welcome.title = ""
    msj_welcome.save()


    # CAPTURAR EL MENSAJE ACABADO DE GUARDAR EN DB PARA MOSTRAR EN EL FRONT
    conversacion = Conversacion.objects.filter(inscripcion__id = inscripcion_curso.id).last()


    # ULTIMO MENSAJE DEL BOT
    last_msj_bot = Conversacion.objects.filter(inscripcion__id = inscripcion_curso.id, user__username="Bot").last()
    

    if last_msj_bot.mensaje == "¿ Quieres Iniciar ya ?" and msj.upper() in ['SI', 'YES','OK','LISTO','S','Y','SE','SEE','SEEE']:
        
        
        list_tema = CurTemStem.objects.filter(curso__id = inscripcion_curso.curso.id).order_by('orden')
        
        tem = [str(i.tema.nombre_tema)+";"+ str(i.tema.id) for i in list_tema]
        print(tem)

        msj_bot = Conversacion()
        msj_bot.user = User.objects.get(username = 'Bot')
        msj_bot.curso = Curso.objects.get(id = id_)
        msj_bot.mensaje = str(tem).replace("'",'"')
        msj_bot.fecha = datetime.today()
        msj_bot.tipo_mensje = "Lista"
        msj_bot.inscripcion = inscripcion_curso
        msj_bot.title = "Esta es la lista de los temas que veremos durante el curso"
        msj_bot.save()


        # print('lista de temas', tem)
        inscripcion_curso.estado = "En proceso"
        inscripcion_curso.save()

        data = [{'msj':conversacion.mensaje, 'datetime':datetime.today().strftime(" %d de %B %Y a las %I:%M %p"), 'sgt_paso':"ConsulTema/"+str(inscripcion_curso.id)+"/", 'tipo_user':'Estudiante', 'tipo_msj':'Texto'},
                {'msj':tem, 'datetime':datetime.today().strftime(" %d de %B %Y a las %I:%M %p"), 'sgt_paso':"ConsulTema/"+str(inscripcion_curso.id)+"/", 'tipo_user':'Bot', 'tipo_msj':'Lista', 'title':'Esta es la lista de los temas que veremos durante el curso'}
                ]
    else:

        data = [{'msj':conversacion.mensaje, 'datetime':datetime.today().strftime(" %d de %B %Y a las %I:%M %p"), 'btn_temas':"ConsulTema/"+str(inscripcion_curso.id)+"/", 'tipo_user':'Estudiante', 'tipo_msj':'Texto'}
                ]
    return JsonResponse(data, safe=False)



def send_save_respuesta(request):

    #CAPTURAR CONTENIDO DEL MENSAJE DEL USUARIO Y EL ID DEL CURSO
    msj = request.GET.get('msj')
    id_ = request.GET.get('id_')

    # GUARDAR EN DB EL MENSAJE ESCRITO POR EL USUARIO
    inscripcion_curso = Inscripcion.objects.get(curso__id = id_, user__username=request.user.username)
    
    msj_welcome = Conversacion()
    msj_welcome.user = User.objects.get(username = request.user.username)
    msj_welcome.curso = Curso.objects.get(id = id_)
    msj_welcome.mensaje = msj
    msj_welcome.fecha = datetime.today()
    msj_welcome.tipo_mensje = "Texto"
    msj_welcome.inscripcion = inscripcion_curso
    msj_welcome.title = ""
    msj_welcome.save()


    # CAPTURAR EL MENSAJE ACABADO DE GUARDAR EN DB PARA MOSTRAR EN EL FRONT
    # conversacion = Conversacion.objects.filter(inscripcion__id = inscripcion_curso.id).last()

    data = [{'msj':msj_welcome.mensaje, 'datetime':datetime.today().strftime(" %d de %B %Y a las %I:%M %p"), 'tipo_user':'Estudiante', 'tipo_msj':'Texto'}
                ]

    return JsonResponse(data, safe=False)



def crear_inst_prog_tem(inscrip,tema_curso_current):

    recur = tema_curso_current.tema.recurso
    if recur == 'Archivo':
        ruta_recur = '/media/'+ str(tema_curso_current.tema.recurso_archivo)
    elif recur == 'Enlace':
        ruta_recur = tema_curso_current.tema.recurso_link_video
    elif recur == 'Video':
        ruta_recur = tema_curso_current.tema.recurso_link_video
    else:
        ruta_recur = ''


    instance_prog_tem = Prog_Tem()#crear una variable tipo progreso para almacenar el primer tema del progreso
    instance_prog_tem.inscripcion = inscrip
    instance_prog_tem.curTemStem = tema_curso_current
    instance_prog_tem.fecha_i = datetime.today()
    instance_prog_tem.fecha_f = datetime.today()
    instance_prog_tem.orden = tema_curso_current.orden
    instance_prog_tem.save()#guardar registro

    msj_bot_name_tema = tema_curso_current.tema.nombre_tema
    msj_bot_descrip_tema = tema_curso_current.tema.descripcion

    # guardar registro en la conversacion con la lista de subtemas
    msj_bot = Conversacion()
    msj_bot.user = User.objects.get(username = 'Bot')
    msj_bot.curso = Curso.objects.get(id = inscrip.curso.id)
    msj_bot.mensaje = msj_bot_descrip_tema
    msj_bot.fecha = datetime.today()
    msj_bot.tipo_mensje = "Texto"
    msj_bot.inscripcion = inscrip
    msj_bot.title = msj_bot_name_tema
    msj_bot.recurso = recur
    msj_bot.recurso_dir = ruta_recur
    msj_bot.save()

    progre_tema = Prog_Tem.objects.all().last()

    data = [{
                'msj':msj_bot_descrip_tema, 
                'datetime':datetime.today().strftime(" %d de %B %Y a las %I:%M %p"), 
                'sgt_paso':"ConsulSubTema/"+str(progre_tema.id)+"/", 
                'tipo_user':'Bot', 
                'tipo_msj':'Texto',
                'title':msj_bot_name_tema,
                'recurso':msj_bot.recurso,
                'ruta_recurso':msj_bot.recurso_dir
            }]

    return data



def ConsulTema(request, id_):
    #id_ : es el id de la inscripcion 

    progre_tema = Prog_Tem.objects.filter(inscripcion__id = id_).order_by('orden')#prgreso de temas de la inscripcion actual
    inscrip = Inscripcion.objects.get(id = id_)#obtener la inscripcion actual
    temas_curso = CurTemStem.objects.filter(curso__id = inscrip.curso.id).order_by('orden')#obtener todos los temas de la  inscripcion actual segun el oreden establecido por el administrador

    progreso_avance = calculo_progreso(inscrip)

    count_prog_tema = progre_tema.count()
    count_temas_curso = temas_curso.count()


    if  count_prog_tema <  count_temas_curso:
        tema_curso_current = temas_curso[count_prog_tema]
        data = crear_inst_prog_tem(inscrip,tema_curso_current)
    else:

        msj_bot = Conversacion()
        msj_bot.user = User.objects.get(username = 'Bot')
        msj_bot.curso = Curso.objects.get(id = inscrip.curso.id)
        msj_bot.mensaje = "Haz completado con Exito este curso"
        msj_bot.fecha = datetime.today()
        msj_bot.tipo_mensje = "Texto"
        msj_bot.inscripcion = inscrip
        msj_bot.title = "¡FELICIDADES!"
        msj_bot.save()

        data = [{
                'msj':msj_bot.mensaje, 
                'datetime':datetime.today().strftime(" %d de %B %Y a las %I:%M %p"), 
                'sgt_paso':"#", 
                'tipo_user':'Bot', 
                'tipo_msj':'Texto', 
                'title':msj_bot.title,
                'progreso_avance':progreso_avance
            }]

    return JsonResponse(data, safe=False)


def ConsulSubTema(request, id_):
    #id_ : es el id del progreso tema

    tema_prog = Prog_Tem.objects.get(id= id_)#obtener el utimo tema actual
    prog_subtema = Prog_Stem.objects.filter(prog_Tem__id = tema_prog.id).order_by('orden')#progreso de subtemas
    subtemas_curso = Cts.objects.filter(curTemStem__id = tema_prog.curTemStem.id).order_by('orden')#obtener todos los subtemas del tema actual segun el oreden establecido por el administrador

    count_prog_subtema = prog_subtema.count()
    count_subtemas_curso = subtemas_curso.count()



    if  count_prog_subtema <  count_subtemas_curso:

        subtema_curso_current = subtemas_curso[count_prog_subtema]

        recur = subtema_curso_current.subtema.recurso
        if recur == 'Archivo':
            ruta_recur = '/media/'+ str(subtema_curso_current.subtema.recurso_archivo)
        elif recur == 'Enlace':
            ruta_recur = subtema_curso_current.subtema.recurso_link_video
        elif recur == 'Video':
            ruta_recur = subtema_curso_current.subtema.recurso_link_video
        else:
            ruta_recur = ''


        instance_prog_subtem = Prog_Stem()
        instance_prog_subtem.prog_Tem = tema_prog
        instance_prog_subtem.cts = subtema_curso_current
        instance_prog_subtem.fecha_i = datetime.today()
        instance_prog_subtem.fecha_f = datetime.today()
        instance_prog_subtem.orden = subtema_curso_current.orden
        instance_prog_subtem.save()

        msj_bot_name_subtema = subtema_curso_current.subtema.nombre
        msj_bot_descrip_subtema = subtema_curso_current.subtema.descripcion

        # guardar registro en la conversacion con la lista de subtemas
        msj_bot = Conversacion()
        msj_bot.user = User.objects.get(username = 'Bot')
        msj_bot.curso = Curso.objects.get(id = subtema_curso_current.curTemStem.curso.id)
        msj_bot.mensaje = msj_bot_descrip_subtema
        msj_bot.fecha = datetime.today()
        msj_bot.tipo_mensje = "Texto"
        msj_bot.inscripcion = Inscripcion.objects.get(id = tema_prog.inscripcion.id)
        msj_bot.title = msj_bot_name_subtema
        msj_bot.recurso = recur
        msj_bot.recurso_dir = ruta_recur
        msj_bot.save()

        # progre_subtema = Prog_Stem.objects.all().last()

        progreso_avance = calculo_progreso(msj_bot.inscripcion)

        data = [{
                    'msj':msj_bot_descrip_subtema, 
                    'datetime':datetime.today().strftime(" %d de %B %Y a las %I:%M %p"), 
                    'sgt_paso':"ConsulDetSubtema/"+str(instance_prog_subtem.id)+"/", 
                    'tipo_user':'Bot', 
                    'tipo_msj':'Texto', 
                    'title':msj_bot_name_subtema,
                    'progreso_avance':progreso_avance,
                    'recurso':msj_bot.recurso,
                    'ruta_recurso':msj_bot.recurso_dir
                    
                }]

    else:

        #ya se pasaron todos los subtemas de un tema, esta parte de codigo manda el examen antes
        # de pasar al siguiente tema

        subtema_curso_current = subtemas_curso[count_prog_subtema-1]

        # instanciar y registrar el progreso de la actividad
        activ_tema = Actividad.objects.filter(curTemStem__id = tema_prog.curTemStem.id)
        preg_activ_prog = Prog_Acti.objects.filter(inscripcion__id = tema_prog.inscripcion.id, actividad__id = activ_tema.first().id )
        
        count_activ_tema = activ_tema.count()
        count_preg_activ_prog = preg_activ_prog.count()


        #extraer las preguntas de la actividad del tema actual
        preg_activ_curso = Act_Pregunta.objects.filter(actividad__id = activ_tema.first().id)
        #Extraer la cantodad de preguntas de la actividad del tema actual
        count_preg_activ_curso = preg_activ_curso.count()



        if  count_preg_activ_prog < count_activ_tema : #estacondicion es funcional simepre y cuando el tema tenga asignado una sola actividad

            inscripcion = Inscripcion.objects.get(id = tema_prog.inscripcion.id)
            progreso_avance = calculo_progreso(inscripcion)

            inst_prog_act = Prog_Acti()
            inst_prog_act.inscripcion = inscripcion
            inst_prog_act.actividad = activ_tema.first()
            inst_prog_act.estado = 1
            inst_prog_act.nota = 0
            inst_prog_act.porcentaje = 0
            inst_prog_act.save()

            
            msj_bot = Conversacion()
            msj_bot.user = User.objects.get(username = 'Bot')
            msj_bot.curso = Curso.objects.get(id = subtema_curso_current.curTemStem.curso.id)
            msj_bot.mensaje = "Ahora te evaluare el tema visto, por favor contesta las siguientes preguntas sin cerrar sesion"
            msj_bot.fecha = datetime.today()
            msj_bot.tipo_mensje = "Texto"
            msj_bot.inscripcion = Inscripcion.objects.get(id = tema_prog.inscripcion.id)
            msj_bot.title = "EXAMEN"
            msj_bot.save()


            data = [{
                    'msj':msj_bot.mensaje, 
                    'datetime':datetime.today().strftime(" %d de %B %Y a las %I:%M %p"), 
                    'sgt_paso':"ConsulSubTema/"+str(id_)+"/", 
                    'tipo_user':'Bot', 
                    'tipo_msj':'Texto', 
                    'title':msj_bot.title,
                    'progreso_avance':progreso_avance
                }]
        else:#empieza a mandar cada pregunta de la actividad actual

            inscrip_cion = Inscripcion.objects.get(id = tema_prog.inscripcion.id)
            progreso_acti_last = Prog_Acti.objects.filter(inscripcion__id = inscrip_cion.id)

            preg_activ_prog = Prog_Preg.objects.filter(prog_Acti__id = progreso_acti_last.last().id)
            count_preg_activ_prog = preg_activ_prog.count()

            if count_preg_activ_prog < count_preg_activ_curso:# verificar que el numero de preguntas enviadas sea menor a la cantidad de preguntas del curso


                act_pregunta_current = preg_activ_curso[count_preg_activ_prog]
                act_preg_opcion = Act_Pregunta_Opt.objects.filter(act_Pregunta__id = act_pregunta_current.id)

                if count_preg_activ_prog != 0:
                    chat_actual = Conversacion.objects.filter(inscripcion__id = inscrip_cion.id).exclude(user__tipo_user = 'Bot')
                    print('chat actual',chat_actual.last().mensaje)
                
                    act_pregunta_back = preg_activ_curso[count_preg_activ_prog-1]
                    act_preg_opcion_back = Act_Pregunta_Opt.objects.filter(act_Pregunta__id = act_pregunta_back.id)
                    
                    act_preg_opcion_user = act_preg_opcion_back.get(id = int(chat_actual.last().mensaje))
                    print('opcion correcta',act_preg_opcion_user)

                    prog_preg_ = Prog_Preg.objects.get(id = preg_activ_prog.last().id)
                    prog_preg_.act_Pregunta_Opt = act_preg_opcion_user
                    prog_preg_.save()
                else:
                    # activi = Act_Pregunta.objects.filter(actividad__id = progreso_acti_last.last().actividad.id)
                    opcionpregunta = Act_Pregunta_Opt.objects.filter(act_Pregunta__id = act_pregunta_current.id)
                    act_preg_opcion_user = opcionpregunta.filter(opt_correcta = 'Falsa').first()


                if act_preg_opcion_user.opt_correcta == 'Correcta':
                    nota = 5
                else:
                    nota = 0

                instanc_prog_preg = Prog_Preg()
                instanc_prog_preg.prog_Acti = progreso_acti_last.last()
                instanc_prog_preg.act_Pregunta_Opt = act_preg_opcion_user
                instanc_prog_preg.curTemStem = CurTemStem.objects.get(id = tema_prog.curTemStem.id)
                instanc_prog_preg.nota = nota
                instanc_prog_preg.porcentaje = round(((count_preg_activ_prog+1)/count_preg_activ_curso)*100,0)
                instanc_prog_preg.save()

                
                tema_curso_ = CurTemStem.objects.filter(curso__id = inscrip_cion.curso.id).order_by('orden')
                cont_activ = 0
                cont_preguntas = 0
                
                for i in tema_curso_:
                    activ = Actividad.objects.filter(curTemStem__id = i.id)
                    for j in activ:
                        cont_activ += 1
                        pregun = Act_Pregunta.objects.filter(actividad__id = j.id)
                        for k in pregun:
                            cont_preguntas += 1

                # POR AQUI QUED
                preg_activ_prog.filter()
                progreso_acti_last.last().nota
                progreso_acti_last.last().porcentaje

                opcion_respuesta = [str(i.descripcion)+";"+ str(i.id) for i in act_preg_opcion]

                msj_bot = Conversacion()
                msj_bot.user = User.objects.get(username = 'Bot')
                msj_bot.curso = Curso.objects.get(id = act_pregunta_current.actividad.curTemStem.curso.id)
                msj_bot.mensaje = str(opcion_respuesta).replace("'",'"')
                msj_bot.fecha = datetime.today()
                msj_bot.tipo_mensje = 'Lista'
                msj_bot.inscripcion = inscrip_cion
                msj_bot.title = act_pregunta_current.descripcion #"Pregunta número "+str(count_preg_activ_prog+1)
                msj_bot.save()

                progreso_avance = calculo_progreso(msj_bot.inscripcion)

                data = [{
                    'msj':msj_bot.mensaje, 
                    'datetime':datetime.today().strftime(" %d de %B %Y a las %I:%M %p"), 
                    'sgt_paso':"ConsulSubTema/"+str(id_)+"/", 
                    'tipo_user':'Bot', 
                    'tipo_msj':'Lista', 
                    'title':msj_bot.title,
                    'progreso_avance':progreso_avance
                }]
            else:# termino de mandar todas las preguntas entonces continua con el siguiete tema

                chat_actual = Conversacion.objects.filter(inscripcion__id = inscrip_cion.id).exclude(user__tipo_user = 'Bot')
            
                act_pregunta_back = preg_activ_curso.last()
                act_preg_opcion_back = Act_Pregunta_Opt.objects.filter(act_Pregunta__id = act_pregunta_back.id)
                
                act_preg_opcion_user = act_preg_opcion_back.get(id = int(chat_actual.last().mensaje))
                # print('opcion correcta',act_preg_opcion_user)

                prog_preg_ = Prog_Preg.objects.get(id = preg_activ_prog.last().id)
                prog_preg_.act_Pregunta_Opt = act_preg_opcion_user
                prog_preg_.save()



                msj_bot = Conversacion()
                msj_bot.user = User.objects.get(username = 'Bot')
                msj_bot.curso = Curso.objects.get(id = subtema_curso_current.curTemStem.curso.id)
                msj_bot.mensaje = "Da click en el boton siguiente para continuar con el Curso"
                msj_bot.fecha = datetime.today()
                msj_bot.tipo_mensje = "Texto"
                msj_bot.inscripcion = inscrip_cion
                msj_bot.title = "¡Realizaste con exito el examen!"
                msj_bot.save()

                progreso_avance = calculo_progreso(msj_bot.inscripcion)

                data = [{
                        'msj':msj_bot.mensaje, 
                        'datetime':datetime.today().strftime(" %d de %B %Y a las %I:%M %p"), 
                        'sgt_paso':"ConsulTema/"+str(msj_bot.inscripcion.id)+'/', 
                        'tipo_user':'Bot', 
                        'tipo_msj':'Texto', 
                        'title':msj_bot.title,
                        'progreso_avance':progreso_avance
                    }]

    return JsonResponse(data, safe=False)


def ConsulDetSubtema(request, pk):
    # id_: Prog_Stem, es el progreso del subtema
    print('entro en el tener nivel')
    prog_subtema = Prog_Stem.objects.get(id= pk)
    det_subtema_prog = Prog_Sstem.objects.filter(prog_Stem__id = prog_subtema.id).order_by('orden')
    det_subtema_curso = Ctsd.objects.filter(cts__id = prog_subtema.cts.id).order_by('orden')

    count_det_subtema_prog = det_subtema_prog.count()
    count_det_subtema_curso = det_subtema_curso.count()

    print('contador', count_det_subtema_prog, count_det_subtema_curso)
    if  count_det_subtema_prog <  count_det_subtema_curso:

        det_subtema_curso_current = det_subtema_curso[count_det_subtema_prog]


        recur = det_subtema_curso_current.subSubtema.recurso
        if recur == 'Archivo':
            ruta_recur = '/media/'+ str(det_subtema_curso_current.subSubtema.recurso_archivo)
        elif recur == 'Enlace':
            ruta_recur = det_subtema_curso_current.subSubtema.recurso_link_video
        elif recur == 'Video':
            ruta_recur = det_subtema_curso_current.subSubtema.recurso_link_video
        else:
            ruta_recur = ''



        instance_prog_det_subtem = Prog_Sstem()
        instance_prog_det_subtem.prog_Stem = prog_subtema
        instance_prog_det_subtem.ctsd = det_subtema_curso_current
        instance_prog_det_subtem.fecha_i = datetime.today()
        instance_prog_det_subtem.fecha_f = datetime.today()
        instance_prog_det_subtem.orden = det_subtema_curso_current.orden
        instance_prog_det_subtem.save()

        msj_bot_name_det_subtema = det_subtema_curso_current.subSubtema.nombre
        msj_bot_descrip_det_subtema = det_subtema_curso_current.subSubtema.descripcion

        # guardar registro en la conversacion con la lista de subtemas
        msj_bot = Conversacion()
        msj_bot.user = User.objects.get(username = 'Bot')
        msj_bot.curso = Curso.objects.get(id = det_subtema_curso_current.cts.curTemStem.curso.id)
        msj_bot.mensaje = msj_bot_descrip_det_subtema
        msj_bot.fecha = datetime.today()
        msj_bot.tipo_mensje = "Texto"
        msj_bot.inscripcion = Inscripcion.objects.get(id = prog_subtema.prog_Tem.inscripcion.id)
        msj_bot.title = msj_bot_name_det_subtema
        msj_bot.recurso = recur
        msj_bot.recurso_dir = ruta_recur
        msj_bot.save()

        # progre_det_subtema = Prog_Sstem.objects.all().last()
        progreso_avance = calculo_progreso(msj_bot.inscripcion)
        data = [{
                    'msj':msj_bot_descrip_det_subtema, 
                    'datetime':datetime.today().strftime(" %d de %B %Y a las %I:%M %p"), 
                    'sgt_paso':"ConsulDetSubtema/"+str(pk)+"/", 
                    'tipo_user':'Bot', 
                    'tipo_msj':'Texto', 
                    'title':msj_bot_name_det_subtema,
                    'progreso_avance':progreso_avance,
                    'recurso':msj_bot.recurso,
                    'ruta_recurso':msj_bot.recurso_dir
                }]
    else:

        det_subtema_curso_current = det_subtema_curso[count_det_subtema_prog-1]

        msj_bot = Conversacion()
        msj_bot.user = User.objects.get(username = 'Bot')
        msj_bot.curso = Curso.objects.get(id = det_subtema_curso_current.cts.curTemStem.curso.id)
        msj_bot.mensaje = "Haz completado con Exito el detalle del subtema actual"
        msj_bot.fecha = datetime.today()
        msj_bot.tipo_mensje = "Texto"
        msj_bot.inscripcion = Inscripcion.objects.get(id = prog_subtema.prog_Tem.inscripcion.id)
        msj_bot.title = "¡En hora Buena!"
        msj_bot.save()

        progreso_avance = calculo_progreso(msj_bot.inscripcion)

        data = [{
                    'msj':msj_bot.mensaje,
                    'datetime':datetime.today().strftime(" %d de %B %Y a las %I:%M %p"), 
                    'sgt_paso':"ConsulSubTema/"+str(prog_subtema.prog_Tem.id)+'/', 
                    'tipo_user':'Bot', 
                    'tipo_msj':'Texto', 
                    'title':msj_bot.title,
                    'progreso_avance':progreso_avance
                }]

    return JsonResponse(data, safe=False)













def index(request):
    userr = User.objects.get(username = request.user.username)
    curso = Curso.objects.all()
    inscripcion = Inscripcion.objects.filter(user__username = request.user.username)
    lista_curso_user_actual = [ inscripc.curso.nombre_curso for inscripc in  inscripcion ]

    print(userr.username)

    contexto = {'cursos':curso, 'inscripciones':lista_curso_user_actual, 'users':userr}
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
        context['accion'] = "crear"
        context['users'] = User.objects.get(username = self.request.user.username)
        # print(context['cursos'])
        return context
        
class Update_Curso(UpdateView): #crear usuario
    model = Curso
    template_name = 'vistas/curso_form.html'
    form_class = CursoForm
    success_url = reverse_lazy('Create_Curso')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cursos'] = Curso.objects.all()
        context['accion'] = "editar"
        context['users'] = User.objects.get(username = self.request.user.username)
        return context

# def Del_Curso(request, id_):
#     curso_ = Curso.objects.get(id = id_)
#     curso_.delete()
#     return render(request, 'vistas/curso_form.html',{})


class Create_TipoActividad(CreateView): #crear usuario
    model = TipoActividad
    template_name = 'vistas/tipoActividad_form.html'
    form_class = TipoActividadForm
    success_url = reverse_lazy('Create_TipoActividad')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tipoActividads'] = TipoActividad.objects.all()
        context['accion'] = "crear"
        context['users'] = User.objects.get(username = self.request.user.username)
        return context
    

class Update_TipoActividad(UpdateView): #crear usuario
    model = TipoActividad
    template_name = 'vistas/tipoActividad_form.html'
    form_class = TipoActividadForm
    success_url = reverse_lazy('Create_TipoActividad')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tipoActividads'] = TipoActividad.objects.all()
        context['accion'] = "editar"
        context['users'] = User.objects.get(username = self.request.user.username)
        return context



class Create_Tema(CreateView): #crear usuario
    model = Tema
    template_name = 'vistas/tema_form.html'
    form_class = TemaForm
    success_url = reverse_lazy('Create_Tema')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['temas'] = Tema.objects.all()
        context['accion'] = "crear"
        context['users'] = User.objects.get(username = self.request.user.username)

        return context

class Update_Tema(UpdateView): #crear usuario
    model = Tema
    template_name = 'vistas/tema_form.html'
    form_class = TemaForm
    success_url = reverse_lazy('Create_Tema')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['accion'] = "editar"
        context['users'] = User.objects.get(username = self.request.user.username)
        return context



class Create_Subtema(CreateView): #crear usuario
    model = Subtema
    template_name = 'vistas/subtema_form.html'
    form_class = SubtemaForm
    success_url = reverse_lazy('Create_Subtema')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subtemas'] = Subtema.objects.all()
        context['accion'] = "crear"
        context['users'] = User.objects.get(username = self.request.user.username)
        return context

class Update_Subtema(UpdateView): #crear usuario
    model = Subtema
    template_name = 'vistas/subtema_form.html'
    form_class = SubtemaForm
    success_url = reverse_lazy('Create_Subtema')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subtemas'] = Subtema.objects.all()
        context['accion'] = "editar"
        context['users'] = User.objects.get(username = self.request.user.username)
        return context

#listas para los selects deendientes
def list_subtema(request):
    tema = request.GET.get('tema')
    subtema1 = Subtema.objects.filter(tema=tema).order_by('nombre')
    return render(request,'vistas/dependent_list/list_subtema.html',{'subtemas':subtema1})

#listas para los selects deendientes
def list_subSubtema(request):
    subtema = request.GET.get('subtema')
    subSubtema1 = SubSubtema.objects.filter(subtema=subtema).order_by('nombre')
    return render(request,'vistas/dependent_list/list_subSubtemas.html',{'subSubtemas':subSubtema1})

#listas para los selects dependientes
def list_cts(request):
    curTemStem = request.GET.get('curTemStem')
    tem_curTemStem = CurTemStem.objects.get(id = curTemStem)

    subtema1 = Subtema.objects.filter(tema__id=tem_curTemStem.tema.id)
    return render(request,'vistas/dependent_list/list_cts.html',{'subtemas':subtema1})


    
#listas para los selects dependientes
def list_ctsd(request):
    cts = request.GET.get('cts')
    tem_cts = Cts.objects.get(id = cts)

    subsubtema1 = SubSubtema.objects.filter(subtema__id = tem_cts.subtema.id)
    return render(request,'vistas/dependent_list/list_ctsd.html',{'subsubtemas':subsubtema1})




class Create_SubSubtema(CreateView): #crear usuario
    model = SubSubtema
    template_name = 'vistas/subsubtema_form.html'
    form_class = SubSubtemaForm
    success_url = reverse_lazy('Create_SubSubtema')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subsubtemas'] = SubSubtema.objects.all()
        context['accion'] = "crear"
        context['users'] = User.objects.get(username = self.request.user.username)
        return context

class Update_SubSubtema(UpdateView): #crear usuario
    model = SubSubtema
    template_name = 'vistas/subsubtema_form.html'
    form_class = SubSubtemaForm
    success_url = reverse_lazy('Create_SubSubtema')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subsubtemas'] = SubSubtema.objects.all()
        context['accion'] = "editar"
        context['users'] = User.objects.get(username = self.request.user.username)
        return context



class Create_CurTemStem(CreateView): #crear usuario
    model = CurTemStem
    template_name = 'vistas/curTemStem_form.html'
    form_class = CurTemStemForm
    success_url = reverse_lazy('Create_CurTemStem')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['curtemstems'] = CurTemStem.objects.all()
        context['ctsds'] = Ctsd.objects.all()
        context['accion'] = "crear"
        context['users'] = User.objects.get(username = self.request.user.username)
        return context

class Update_CurTemStem(UpdateView): #crear usuario
    model = CurTemStem
    template_name = 'vistas/curTemStem_form.html'
    form_class = CurTemStemForm
    success_url = reverse_lazy('Create_CurTemStem')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['curtemstems'] = CurTemStem.objects.all()
        context['accion'] = "editar"
        context['users'] = User.objects.get(username = self.request.user.username)
        return context



class Create_Actividad(CreateView): #crear usuario
    model = Actividad
    template_name = 'vistas/actividad_form.html'
    form_class = ActividadForm
    success_url = reverse_lazy('Create_Actividad')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['actividads'] = Actividad.objects.all()
        context['accion'] = "crear"
        context['users'] = User.objects.get(username = self.request.user.username)
        return context


class Update_Actividad(UpdateView): #crear usuario
    model = Actividad
    template_name = 'vistas/actividad_form.html'
    form_class = ActividadForm
    success_url = reverse_lazy('Create_Actividad')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['actividads'] = Actividad.objects.all()
        context['accion'] = "editar"
        context['users'] = User.objects.get(username = self.request.user.username)
        return context


class Create_Act_Pregunta(CreateView): #crear usuario
    model = Act_Pregunta
    template_name = 'vistas/act_Pregunta_form.html'
    form_class = Act_PreguntaForm
    success_url = reverse_lazy('Create_Act_Pregunta')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Act_Preguntas'] = Act_Pregunta.objects.all()
        context['accion'] = "crear"
        context['users'] = User.objects.get(username = self.request.user.username)
        return context


class Update_Act_Pregunta(UpdateView): #crear usuario
    model = Act_Pregunta
    template_name = 'vistas/act_Pregunta_form.html'
    form_class = Act_PreguntaForm
    success_url = reverse_lazy('Create_Act_Pregunta')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['accion'] = "editar"
        context['users'] = User.objects.get(username = self.request.user.username)
        return context


class Create_Act_Pregunta_Opt(CreateView): #crear usuario
    model = Act_Pregunta_Opt
    template_name = 'vistas/create_Act_Pregunta_Opt_form.html'
    form_class = Act_Pregunta_OptForm
    success_url = reverse_lazy('Create_Act_Pregunta_Opt')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Act_Pregunta_Opts'] = Act_Pregunta_Opt.objects.all()
        context['accion'] = "crear"
        context['users'] = User.objects.get(username = self.request.user.username)
        return context

class Update_Act_Pregunta_Opt(UpdateView): #crear usuario
    model = Act_Pregunta_Opt
    template_name = 'vistas/create_Act_Pregunta_Opt_form.html'
    form_class = Act_Pregunta_OptForm
    success_url = reverse_lazy('Create_Act_Pregunta_Opt')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['accion'] = "Editar"
        context['users'] = User.objects.get(username = self.request.user.username)
        return context



#esta es la vista de inscripcion para el USUARIO
def Create_Inscripcion(request, id_):

    usuario = User.objects.get(username = request.user.username)
    curso = Curso.objects.get(id = id_)

    instancia = Inscripcion()
    instancia.user = usuario
    instancia.curso = curso
    instancia.estado = "Inscrito"
    instancia.nota_def = 0.0
    instancia.porcentaje_prog = 0.0

    # print(instancia)
    if request.method == 'POST' :
        form = InscripcionForm(request.POST)
        if form.is_valid(): 
            print("formulario guardado", form)
            form.save()
        return redirect('/chat/'+str(id_)+'/')
    else:
        form = InscripcionForm(instance = instancia)
        print("formulario", form)
    return render(request, 'vistas/inscripcion_form.html', {'form':form, 'users':User.objects.get(username = request.user.username)})


#esta es la vista de inscripcion para el ADMINISTRADOR
class Create_Inscripcion_Admin(CreateView): #crear usuario
    model = Inscripcion
    template_name = 'vistas/inscripcion_admin_form.html'
    form_class = InscripcionForm
    success_url = reverse_lazy('Create_Inscripcion_Admin')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['inscipcions'] = Inscripcion.objects.all()
        context['accion'] = "crear"
        context['users'] = User.objects.get(username = self.request.user.username)
        return context

class Update_Inscripcion_Admin(UpdateView): #crear usuario
    model = Inscripcion
    template_name = 'vistas/inscripcion_admin_form.html'
    form_class = InscripcionForm
    success_url = reverse_lazy('Create_Inscripcion_Admin')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['accion'] = "Editar"
        context['users'] = User.objects.get(username = self.request.user.username)
        return context




class Create_Prog_Acti(CreateView): #crear usuario
    model = Prog_Acti
    template_name = 'vistas/progreso_form.html'
    form_class = Prog_ActiForm
    success_url = reverse_lazy('Create_Progreso')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['progresos'] = Prog_Acti.objects.all()
        context['accion'] = "crear"
        context['users'] = User.objects.get(username = self.request.user.username)
        return context


class Update_Prog_Acti(UpdateView): #crear usuario
    model = Prog_Acti
    template_name = 'vistas/progreso_form.html'
    form_class = Prog_ActiForm
    success_url = reverse_lazy('Create_Progreso')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['accion'] = "Editar"
        context['users'] = User.objects.get(username = self.request.user.username)
        return context



class Create_Prog_Preg(CreateView): #crear usuario
    model = Prog_Preg
    template_name = 'vistas/progresoDet_form.html'
    form_class = Prog_PregForm
    success_url = reverse_lazy('Create_ProgresoDet')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ProgresoDets'] = Prog_Preg.objects.all()
        context['accion'] = "crear"
        context['users'] = User.objects.get(username = self.request.user.username)
        return context

class Update_Prog_Preg(UpdateView): #crear usuario
    model = Prog_Preg
    template_name = 'vistas/progresoDet_form.html'
    form_class = Prog_PregForm
    success_url = reverse_lazy('Create_ProgresoDet')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['accion'] = "editar"
        context['users'] = User.objects.get(username = self.request.user.username)
        return context







class Create_Cts(CreateView): #crear usuario
    model = Cts
    template_name = 'vistas/cts_form.html'
    form_class = CtsForm
    success_url = reverse_lazy('Create_Cts')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Ctss'] = Cts.objects.all()
        context['accion'] = "crear"
        context['users'] = User.objects.get(username = self.request.user.username)
        return context



class Update_Cts(UpdateView): #crear usuario
    model = Cts
    template_name = 'vistas/cts_form.html'
    form_class = CtsForm
    success_url = reverse_lazy('Create_Cts')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['accion'] = "editar"
        context['users'] = User.objects.get(username = self.request.user.username)
        return context




class Create_Ctsd(CreateView): #crear usuario
    model = Ctsd
    template_name = 'vistas/ctsd_form.html'
    form_class = CtsdForm
    success_url = reverse_lazy('Create_Ctsd')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Ctsds'] = Ctsd.objects.all()
        context['accion'] = "crear"
        context['users'] = User.objects.get(username = self.request.user.username)
        return context


class Update_Ctsd(UpdateView): #crear usuario
    model = Ctsd
    template_name = 'vistas/ctsd_form.html'
    form_class = CtsdForm
    success_url = reverse_lazy('Create_Ctsd')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['accion'] = "editar"
        context['users'] = User.objects.get(username = self.request.user.username)
        return context




# class Create_Prog_Tem(CreateView): #crear usuario
#     model = Prog_Tem
#     template_name = 'vistas/prog_Tem_form.html'
#     form_class = Prog_TemForm
#     success_url = reverse_lazy('Create_Prog_Tem')

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['Prog_Tems'] = Prog_Tem.objects.all()
#         context['accion'] = "crear"
#         return context


# class Update_Prog_Tem(UpdateView): #crear usuario
#     model = Prog_Tem
#     template_name = 'vistas/prog_Tem_form.html'
#     form_class = Prog_TemForm
#     success_url = reverse_lazy('Create_Prog_Tem')

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['accion'] = "editar"
#         return context




# class Create_Prog_Stem(CreateView): #crear usuario
#     model = Prog_Stem
#     template_name = 'vistas/prog_Stem_form.html'
#     form_class = Prog_StemForm
#     success_url = reverse_lazy('Create_Prog_Stem')

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['Prog_Stems'] = Prog_Stem.objects.all()
#         context['accion'] = "crear"
#         return context


# class Update_Prog_Stem(UpdateView): #crear usuario
#     model = Prog_Stem
#     template_name = 'vistas/prog_Stem_form.html'
#     form_class = Prog_StemForm
#     success_url = reverse_lazy('Create_Prog_Stem')

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['accion'] = "editar"
#         return context




# class Create_Prog_Sstem(CreateView): #crear usuario
#     model = Prog_Sstem
#     template_name = 'vistas/prog_Sstem_form.html'
#     form_class = Prog_SstemForm
#     success_url = reverse_lazy('Create_Prog_Sstem')

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['Prog_Sstems'] = Prog_Sstem.objects.all()
#         context['accion'] = "crear"
#         return context


# class Update_Prog_Sstem(UpdateView): #crear usuario
#     model = Prog_Sstem
#     template_name = 'vistas/prog_Sstem_form.html'
#     form_class = Prog_SstemForm
#     success_url = reverse_lazy('Create_Prog_Sstem')

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['accion'] = "editar"
#         return context