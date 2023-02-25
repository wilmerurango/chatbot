from datetime import datetime
from pyexpat import model
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class AbstraCurso(models.Model):
    tema = "Tema"
    subtema = "Subtema"
    subSubtema = "SubSubtema"
    opcion_ = [(tema,"Tema"),(subtema,"Subtema"), (subSubtema,"SubSubtema")]

    id_curso = models.IntegerField('id Curso', blank=False, null=True)
    nombre_curso = models.CharField('Nombre Curso', max_length=50, blank=False, null=True)
    
    categoria_nivel_tema = models.CharField('Categoria Nivel Tema', max_length=10, choices=opcion_, default=subSubtema, null=True)
    id_nivel_tema = models.IntegerField('Orden', blank=False, null=True)
    nombre_nivel_tema = models.CharField('Nombre', max_length=50, blank=False, null=True)
    descripcion_nivel_tema = models.TextField('Descripción', blank=False, null=True)



class User(AbstractUser):
    admin = "Administrador"
    estud = "Estudiante"
    docen = "Docente"
    bot = "Bot"
    
    opcion_ = [(admin,"Administrador"),(estud,"Estudiante"), (docen,"Docente"), (bot,"Bot"),]

    tipo_user = models.CharField('Tipo Usuario', max_length=13, choices=opcion_, default=estud, null=True)
    direccion = models.CharField('Dirección', max_length=100, blank=False, null=True)
    telefono = models.CharField('Telefono', max_length=15, blank=False, null=True)
    fecha_creacion = models.DateTimeField(verbose_name='Fecha Creación',blank=False, null=True, default=datetime.now())
    
    activo = 'Activo'
    suspendido = 'Suspendido'
    inactivo = 'Inactivo'
    estado_estudiante = [(activo,'Activo'),
                        (suspendido,'Suspendido'),
                        (inactivo, 'Inactivo')]

    estado = models.CharField('Estado', max_length=12, choices=estado_estudiante, default=activo, null=True, db_index=True)
    colegio =  models.CharField('Colegio', max_length=100, blank=False, null=True)
    grado_cursado = models.CharField('Grado Cursado', max_length=10, blank=False, null=True)
    fecha_naci = models.DateField('Fecha de Nacimiento', blank=False, null=True)

    m = "Masculino"
    f = "Femenino"
    list_gen = [(m,"Masculino"),(f,"Femenino")]
    genero = models.CharField('Género', max_length=9, choices=list_gen, default=m, null=True, db_index=True)

    uno = "1"
    dos = "2"
    tres = "3"
    cuatro = "4"
    cinco = "5"
    seis = "6"

    list_num =[
        (uno , "1"),
        (dos , "2"),
        (tres , "3"),
        (cuatro , "4"),
        (cinco , "5"),
        (seis , "6")
    ]
    estrato = models.CharField('Estrato', max_length=1, choices=list_num, default=uno, null=True)


    def __str__(self):
        return '%s' % (self.username)



class Curso(models.Model):
    abierto = "Abierto"
    cerrado = "Cerrado"
    # en_proceso = "En Proceso"
    
    opcion_ = [(abierto,"Abierto"),(cerrado,"Cerrado")]

    nombre_curso  = models.CharField('Nombre de Curso', max_length=100, blank=False, null=True)
    fecha_inicial = models.DateTimeField(verbose_name='Fecha Inicial', null=True)
    fecha_final = models.DateTimeField(verbose_name='Fecha Final', null=True)
    descripcion = models.TextField('Descripción del Curso', null=True)
    estado =  models.CharField('Estado del Curso', max_length=10, choices=opcion_, default=cerrado, null=True)

    def __str__(self):
        return '%s %s %s' % (self.nombre_curso, " -- ",self.estado )

# Create your models here.


class TipoActividad(models.Model):
    nombre_tipo_actividad = models.CharField('Nombre Tipo de Actividad', max_length=50, blank=False, null=True)
    fecha_creacion = models.DateTimeField(verbose_name='Fecha Creación', null=True)
    estado = models.IntegerField('Estado', db_index=True, null=True)

    def __str__(self):
        return '%s' % (self.nombre_tipo_actividad)


class Tema(models.Model):
    activo = "Activo"
    inactivo = "Inactivo"

    opcion_ = [(activo , "Activo"),(inactivo , "Inactivo")]

    link  = 'Enlace'
    archivo = 'Archivo'
    video = 'Video'
    opcion_recurso = [(link,"Enlace"),(archivo,"Archivo"),(video,"Video")]

    nombre_tema = models.CharField('Nombre del Tema', max_length=50, blank=False, null=True)
    descripcion = models.TextField('Descripción del Tema', null=True)
    estado =  models.CharField('Estado del Tema', max_length=10, choices=opcion_, default=activo, null=True)

    recurso = models.CharField('Recurso', max_length=7, choices=opcion_recurso,  null=True, blank = True)
    recurso_link_video = models.TextField('Enlace',null=True, blank = True)
    recurso_archivo = models.FileField('Cargar archivo', upload_to = "Tema/", null=True, blank = True)

    def __str__(self):
        return '%s %s %s' % (self.nombre_tema, " -- ", self.estado)


class Subtema(models.Model):

    activo = "Activo"
    inactivo = "Inactivo"
    opcion_ = [(activo , "Activo"),(inactivo , "Inactivo")]

    link  = 'Enlace'
    archivo = 'Archivo'
    video = 'Video'
    opcion_recurso = [(link,"Enlace"),(archivo,"Archivo"),(video,"Video")]

    tema = models.ForeignKey(Tema, verbose_name='Tema', null=True, on_delete=models.PROTECT)
    nombre = models.CharField('Nombre Subtema', max_length=100, blank=False, null=True)
    descripcion = models.TextField('Descripción Subtema', null=True)
    estado = models.CharField('Estado del Subtema', max_length=10, choices=opcion_, default=activo, null=True)

    recurso = models.CharField('Recurso', max_length=7, choices=opcion_recurso,  null=True, blank = True)
    recurso_link_video = models.TextField('Enlace',null=True, blank = True)
    recurso_archivo = models.FileField('Cargar archivo', upload_to = "Subtema/", null=True, blank = True)


    def __str__(self):
        return '%s %s %s' % (self.nombre, " -- ", self.estado)


class SubSubtema(models.Model):

    activo = "Activo"
    inactivo = "Inactivo"
    opcion_ = [(activo , "Activo"),(inactivo , "Inactivo")]

    link  = 'Enlace'
    archivo = 'Archivo'
    video = 'Video'
    opcion_recurso = [(link,"Enlace"),(archivo,"Archivo"),(video,"Video")]

    tema = models.ForeignKey(Tema, verbose_name='Tema', null=True, on_delete=models.PROTECT)
    subtema = models.ForeignKey(Subtema, verbose_name='Subtema', null=True, on_delete=models.PROTECT)
    nombre = models.CharField('Nombre tema nivel tres', max_length=100, blank=False, null=True)
    descripcion = models.TextField('Descripción Tema', null=True)
    estado = models.CharField('Estado del tema', max_length=10, choices=opcion_, default=activo, null=True)

    recurso = models.CharField('Recurso', max_length=7, choices=opcion_recurso,  null=True, blank = True)
    recurso_link_video = models.TextField('Enlace',null=True, blank = True)
    recurso_archivo = models.FileField('Cargar archivo', upload_to = "SubSubtema", null=True, blank = True)


    def __str__(self):
        return '%s %s %s' % (self.nombre, " -- ", self.estado)


#se actualizo se quito la relacion al subsubtema
class CurTemStem(models.Model):
    curso = models.ForeignKey(Curso, verbose_name='Curso', null=True, on_delete=models.PROTECT)
    tema = models.ForeignKey(Tema, verbose_name='Tema', null=True, on_delete=models.PROTECT)
    fecha_i = models.DateTimeField(verbose_name='Fecha Inicio', null=True)
    fecha_f = models.DateTimeField(verbose_name='Fecha Fin', null=True)
    orden = models.IntegerField('Orden', null=True)

    def __str__(self):
        return '%s' % (self.tema.nombre_tema)


class Cts(models.Model):
    curTemStem = models.ForeignKey(CurTemStem, verbose_name='Detallado del Curso', null=True, on_delete=models.PROTECT)
    subtema = models.ForeignKey(Subtema, verbose_name='Subtema', null=True, on_delete=models.PROTECT)
    orden = models.IntegerField('Orden', null=True)

    def __str__(self):
        return '%s' % (self.subtema.nombre)



#se crea tabla en la actualizacion
class Ctsd(models.Model):
    cts = models.ForeignKey(Cts, verbose_name='Curso Tema Subtema', null=True, on_delete=models.PROTECT)
    subSubtema = models.ForeignKey(SubSubtema, verbose_name='SubSubtema', null=True, on_delete=models.PROTECT)
    orden = models.IntegerField('Orden', null=True)

    def __str__(self):
        return '%s' % (self.subSubtema.nombre)




class Actividad(models.Model):
    curTemStem = models.ForeignKey(CurTemStem, verbose_name='CurTemStem', null=True, on_delete=models.PROTECT)
    tipoActividad = models.ForeignKey(TipoActividad, verbose_name='Tipo de Actividad', null=True, on_delete=models.PROTECT)
    nombre = models.CharField('Nombre de la Actividad', max_length=100, blank=False, null=True)
    descripcion = models.TextField('Descripción de La Actividad', null=True)
    estado = models.IntegerField('Estado de la Actividad', db_index=True, null=True)
    fecha_i = models.DateTimeField(verbose_name='Fecha Inicio', db_index=True, null=True)
    fecha_f = models.DateTimeField(verbose_name='Fecha Fin', db_index=True, null=True)

    def __str__(self):
        return '%s' % (self.nombre)


#actualizada
class Act_Pregunta(models.Model):
    actividad = models.ForeignKey(Actividad, verbose_name='Actividad', null=True, on_delete=models.PROTECT)
    tipo  = models.IntegerField('Tipo', null=True)
    descripcion = models.TextField('Descripción Actividad', null=True)
    # nota = models.FloatField('Nota')

    def __str__(self):
        return '%s %s %s' % (self.actividad.nombre,' -- ',self.descripcion)


# se actualizo
class Act_Pregunta_Opt(models.Model):
    falsa = 'Falsa'
    correcta = 'Correcta'


    opcion_ = [(falsa , "Falsa"),(correcta , "Correcta")]


    act_Pregunta = models.ForeignKey(Act_Pregunta, verbose_name='ActividadDet', null=True, on_delete=models.PROTECT)
    descripcion = models.TextField('Descripción', null=True)
    orden = models.IntegerField('Orden', null=True)
    opt_correcta = models.CharField('Esta opción es',choices=opcion_, blank=False, null=True, default=falsa, max_length=8)
    # nota = models.FloatField('Nota')

    def __str__(self):
        return '%s %s %s' % (self.act_Pregunta.descripcion, ' -- ',self.descripcion)

# actualizado
class Inscripcion(models.Model):
    inscrito = "Inscrito"
    en_proceso = "En proceso"
    completado = "Completado"
    cancelado = "Cancelado"

    opcion = [(inscrito,"Inscrito"),(en_proceso,"En proceso"),(completado,"Completado"),(cancelado,"Cancelado")]

    user = models.ForeignKey(User, verbose_name='Usuario', null=True, on_delete=models.PROTECT)
    curso = models.ForeignKey(Curso, verbose_name='Curso', null=True, on_delete=models.PROTECT)
    estado = models.CharField('Estado', max_length=11, choices=opcion, default=inscrito, null=True)
    nota_def = models.FloatField('Nota Definitiva', null=True, default=0.0)
    porcentaje_prog = models.FloatField('%. de Progreso', null=True, default=0.0)

    def __str__(self):
        return '%s %s %s' % (self.user.username,"--",self.curso.nombre_curso)


class Conversacion(models.Model):
    link = "Link"
    video = "Video"
    lista = "Lista"
    texto = "Texto"
    
    opcion_ = [
        (link,"Link"),
        (video,"Video"),
        (lista,"Lista"),
        (texto,"Texto"),]


    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Usuario', null=True, on_delete=models.PROTECT)
    curso = models.ForeignKey(Curso, verbose_name='Curso', null=True, on_delete=models.PROTECT)
    mensaje = models.TextField('Mensaje', null=True)
    fecha = models.DateTimeField(verbose_name='Fecha/Hora', null=True)
    tipo_mensje = models.CharField('Estado del Tema', max_length=10, choices=opcion_, default=texto, null=True)
    inscripcion = models.ForeignKey(Inscripcion, verbose_name='Inscripcion', null=True, on_delete=models.PROTECT)
    title = models.TextField('Titulo',max_length=100, blank=True, null=True)

    recurso = models.CharField('Recurso', max_length=7, null=True, blank = True)
    recurso_dir = models.TextField('Direccion Recurso',null=True, blank = True)


    #comentario
    def __str__(self):
        return '%s' % (self.user.username)


#se actualizo
class Prog_Acti(models.Model):
    inscripcion = models.ForeignKey(Inscripcion, verbose_name='Inscripcion', null=True, on_delete=models.PROTECT)
    # curTemStem = models.ForeignKey(CurTemStem, verbose_name='CurTemStem', null=True, on_delete=models.PROTECT)
    actividad = models.ForeignKey(Actividad, verbose_name='Actividad', null=True, on_delete=models.PROTECT)
    estado = models.IntegerField('Estado', null=True , blank=True)
    nota = models.FloatField('Nota', null=True)
    porcentaje = models.FloatField('Porcentaje avance', null=True)

    def __str__(self):
        return '%s %s' % (self.inscripcion.user.username, self.inscripcion.curso.nombre_curso)


#actualizado
class Prog_Preg(models.Model):
    prog_Acti = models.ForeignKey(Prog_Acti, verbose_name='Progreso Actividad', null=True, on_delete=models.PROTECT)
    act_Pregunta_Opt = models.ForeignKey(Act_Pregunta_Opt, verbose_name='ActDetOpt', null=True, on_delete=models.PROTECT)
    curTemStem = models.ForeignKey(CurTemStem, verbose_name='CurTemStem', null=True, on_delete=models.PROTECT)
    # estado = models.IntegerField('Estado')
    nota = models.FloatField('Nota', null=True)
    porcentaje = models.FloatField('Porcentaje avance', null=True)

    def __str__(self):
        return '%s %s' % (self.prog_Acti.inscripcion.user.username, self.curTemStem.curso.nombre_curso)


# LLevar un log que guarde por donde va el usuario en el curso
# class Log_Curso_Inscrip(models.Model):
#     en_proceso = "En proceso"
#     completado = "Completado"

#     opcion = [(en_proceso,"En proceso"),(completado,"Completado")]

#     inscripcion = models.ForeignKey(Inscripcion, verbose_name='Inscripcion', null=True, on_delete=models.PROTECT)
#     tema = models.ForeignKey(Tema, verbose_name='Tema', null=True, on_delete=models.PROTECT)
#     subtema = models.ForeignKey(Subtema, verbose_name='Subtema', null=True, on_delete=models.PROTECT)
#     subSubtema = models.ForeignKey(SubSubtema, verbose_name='SubSubtema', null=True, on_delete=models.PROTECT)
#     date_time_i = models.DateTimeField(verbose_name='Fecha/Hora Inicio', null=True)
#     date_time_f = models.DateTimeField(verbose_name='Fecha/Hora Fin', null=True)
#     estado_tema = models.CharField('Estado Tema', max_length=10, choices=opcion, default=en_proceso, null=True)
#     estado_subtema = models.CharField('Estado Subtema', max_length=10, choices=opcion, default=en_proceso, null=True)
#     estado_subsubtema = models.CharField('Estado Detalle Subtema', max_length=10, choices=opcion, default=en_proceso, null=True)



class Prog_Tem(models.Model):
    inscripcion = models.ForeignKey(Inscripcion, verbose_name='Inscripcion', null=True, on_delete=models.PROTECT)
    curTemStem = models.ForeignKey(CurTemStem, verbose_name='Detallado del Curso', null=True, on_delete=models.PROTECT)
    fecha_i = models.DateTimeField(verbose_name='Fecha Inicio', db_index=True, null=True)
    fecha_f = models.DateTimeField(verbose_name='Fecha Fin', db_index=True, null=True)
    orden = models.IntegerField('Orden', null=True)

    def __str__(self):
        return '%s' % (self.curTemStem.tema.nombre_tema)


class Prog_Stem(models.Model):
    prog_Tem = models.ForeignKey(Prog_Tem, verbose_name='Progreso SubTema', null=True, on_delete=models.PROTECT)
    cts = models.ForeignKey(Cts, verbose_name='Curso Tema Subtema', null=True, on_delete=models.PROTECT)
    fecha_i = models.DateTimeField(verbose_name='Fecha Inicio', db_index=True, null=True)
    fecha_f = models.DateTimeField(verbose_name='Fecha Fin', db_index=True, null=True)
    orden = models.IntegerField('Orden', null=True)

    def __str__(self):
        return '%s' % (self.cts.subtema.nombre)


class Prog_Sstem(models.Model):
    prog_Stem = models.ForeignKey(Prog_Stem, verbose_name='Progreso Detelle SubTema', null=True, on_delete=models.PROTECT)
    ctsd = models.ForeignKey(Ctsd, verbose_name='Curso,Tema,Subtema,Detalle', null=True, on_delete=models.PROTECT)
    fecha_i = models.DateTimeField(verbose_name='Fecha Inicio', db_index=True, null=True)
    fecha_f = models.DateTimeField(verbose_name='Fecha Fin', db_index=True, null=True)
    orden = models.IntegerField('Orden', null=True)

    def __str__(self):
        return '%s' % (self.ctsd.subSubtema.nombre)
