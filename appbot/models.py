# from ast import AugLoad
# import email
# from pickle import TRUE
# from statistics import correlation, mode
# from mailbox import NoSuchMailboxError
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
# from django.contrib.auth.models import User
# from sqlalchemy import true



class User(AbstractUser):
    si = "Si"
    no = "No"
    opcion_ = [(si,"Si"),(no,"no")]

    usuario_bot = models.CharField('Usuario Bot', max_length=2, choices=opcion_, default=no, null=True)
    direccion = models.CharField('Dirección', max_length=100, blank=False, null=True)
    telefono = models.CharField('Telefono', max_length=15, blank=False, null=True)
    fecha_creacion = models.DateTimeField(verbose_name='Fecha Creación',blank=False, null=True)
    
    activo = 'Activo'
    suspendido = 'Suspendido'
    inactivo = 'Inactivo'
    estado_estudiante = [(activo,'Activo'),
                        (suspendido,'Suspendido'),
                        (inactivo, 'Inactivo')]

    estado = models.CharField('Estado', max_length=12, choices=estado_estudiante, default=activo, null=True)
    colegio =  models.CharField('Colegio', max_length=100, blank=False, null=True)
    grado_cursado = models.CharField('Grado Cursado', max_length=10, blank=False, null=True)

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
    mensaje = models.TextField('Mensaje')
    fecha = models.DateTimeField(verbose_name='Fecha/Hora')
    tipo_mensje = models.CharField('Estado del Tema', max_length=10, choices=opcion_, default=texto, null=True)

    def __str__(self):
        return '%s' % (self.user.username)



class TipoActividad(models.Model):
    nombre_tipo_actividad = models.CharField('Nombre Tipo de Actividad', max_length=50, blank=False, null=True)
    fecha_creacion = models.DateTimeField(verbose_name='Fecha Creación')
    estado = models.IntegerField('Estado')

    def __str__(self):
        return '%s' % (self.nombre_tipo_actividad)


class Tema(models.Model):
    activo = "Activo"
    inactivo = "Inactivo"

    opcion_ = [(activo , "Activo"),(inactivo , "Inactivo")]

    nombre_tema = models.CharField('Nombre del Tema', max_length=50, blank=False, null=True)
    descripcion = models.TextField('Descripción del Tema')
    estado =  models.CharField('Estado del Tema', max_length=10, choices=opcion_, default=activo, null=True)

    def __str__(self):
        return '%s %s %s' % (self.nombre_tema, " -- ", self.estado)


class Subtema(models.Model):

    activo = "Activo"
    inactivo = "Inactivo"

    opcion_ = [(activo , "Activo"),(inactivo , "Inactivo")]
    tema = models.ForeignKey(Tema, verbose_name='Tema', null=True, on_delete=models.PROTECT)
    nombre = models.CharField('Nombre Subtema', max_length=50, blank=False, null=True)
    descripcion = models.TextField('Descripción Subtema')
    estado = models.CharField('Estado del Subtema', max_length=10, choices=opcion_, default=activo, null=True)


    def __str__(self):
        return '%s %s %s' % (self.nombre, " -- ", self.estado)


class SubSubtema(models.Model):

    activo = "Activo"
    inactivo = "Inactivo"

    opcion_ = [(activo , "Activo"),(inactivo , "Inactivo")]
    subtema = models.ForeignKey(Subtema, verbose_name='Subtema', null=True, on_delete=models.PROTECT)
    nombre = models.CharField('Nombre tema nivel tres', max_length=50, blank=False, null=True)
    descripcion = models.TextField('Descripción Tema')
    estado = models.CharField('Estado del tema', max_length=10, choices=opcion_, default=activo, null=True)


    def __str__(self):
        return '%s %s %s' % (self.nombre, " -- ", self.estado)


class CurTemStem(models.Model):
    curso = models.ForeignKey(Curso, verbose_name='Curso', null=True, on_delete=models.PROTECT)
    tema = models.ForeignKey(Tema, verbose_name='Tema', null=True, on_delete=models.PROTECT)
    subtema = models.ForeignKey(Subtema, verbose_name='Subtema', null=True, on_delete=models.PROTECT)
    subSubtema = models.ForeignKey(SubSubtema, verbose_name='SubSubtema', null=True, on_delete=models.PROTECT)
    fecha_i = models.DateTimeField(verbose_name='Fecha Inicio')
    fecha_f = models.DateTimeField(verbose_name='Fecha Fin')
    orden = models.IntegerField('Orden', unique=True)

    def __str__(self):
        return '%s' % (self.curso.nombre_curso)



class Actividad(models.Model):
    curTemStem = models.ForeignKey(CurTemStem, verbose_name='CurTemStem', null=True, on_delete=models.PROTECT)
    tipoActividad = models.ForeignKey(TipoActividad, verbose_name='Tipo de Actividad', null=True, on_delete=models.PROTECT)
    nombre = models.CharField('Nombre de la Actividad', max_length=50, blank=False, null=True)
    descripcion = models.TextField('Descripción de La Actividad')
    estado = models.IntegerField('Estado de la Actividad')
    fecha_i = models.DateTimeField(verbose_name='Fecha Inicio')
    fecha_f = models.DateTimeField(verbose_name='Fecha Fin')

    def __str__(self):
        return '%s' % (self.nombre)


class ActividadDet(models.Model):
    actividad = models.ForeignKey(Actividad, verbose_name='Actividad', null=True, on_delete=models.PROTECT)
    tipo  = models.IntegerField('Orden')
    descripcion = models.TextField('Descripción Actividad')
    nota = models.FloatField('Nota')

    def __str__(self):
        return '%s' % (self.actividad.nombre)



class ActDetOpt(models.Model):
    actividadDet = models.ForeignKey(ActividadDet, verbose_name='ActividadDet', null=True, on_delete=models.PROTECT)
    descripcion = models.TextField('Descripción ActDetOpt')
    orden = models.IntegerField('Orden')
    opt_correcta = models.IntegerField('Opción Correcta')
    nota = models.FloatField('Nota')

    def __str__(self):
        return '%s' % (self.actividadDet.actividad.nombre)


class Inscripcion(models.Model):
    user = models.ForeignKey(User, verbose_name='Usuario', null=True, on_delete=models.PROTECT)
    curso = models.ForeignKey(Curso, verbose_name='Curso', null=True, on_delete=models.PROTECT)
    estado = models.IntegerField('Estado')

    def __str__(self):
        return '%s %s %s' % (self.user.username,"--",self.curso.nombre_curso)


class Progreso(models.Model):
    inscripcion = models.ForeignKey(Inscripcion, verbose_name='Inscripcion', null=True, on_delete=models.PROTECT)
    curTemStem = models.ForeignKey(CurTemStem, verbose_name='CurTemStem', null=True, on_delete=models.PROTECT)
    estado = models.IntegerField('Estado')
    nota = models.FloatField('Nota')

    def __str__(self):
        return '%s %s' % (self.user.username, self.curso.nombre_curso)


class ProgresoDet(models.Model):
    progreso = models.ForeignKey(Progreso, verbose_name='Progreso', null=True, on_delete=models.PROTECT)
    actDetOpt = models.ForeignKey(ActDetOpt, verbose_name='ActDetOpt', null=True, on_delete=models.PROTECT)
    estado = models.IntegerField('Estado')
    nota = models.FloatField('Nota')

    def __str__(self):
        return '%s %s' % (self.user.username, self.curso.nombre_curso)