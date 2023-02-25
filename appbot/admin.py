from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from .models import *


# crear un formulario basado en el modelo sobreescrito de User
class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User


# Sobreescribir la clase UserAdmin para mostrar el formulario recien creado 'MyUserChangeForm'
# toca agregar los campos nuevos
class UserAdmin(UserAdmin):
    form = MyUserChangeForm

    fieldsets = UserAdmin.fieldsets + (
            (None, {'fields': (
                'tipo_user',
                'colegio',
                'direccion',
                'estado',#este es por defecto
                'fecha_creacion',#este es por defecto
                'grado_cursado',
                'telefono',
                'fecha_naci',
                'genero',
                'estrato',
            )}),
    )

admin.site.register(User, UserAdmin)
admin.site.register(Conversacion)
admin.site.register(Curso)
admin.site.register(TipoActividad)
admin.site.register(Tema)
admin.site.register(Subtema)
admin.site.register(SubSubtema)
admin.site.register(CurTemStem)
admin.site.register(Actividad)
admin.site.register(Act_Pregunta)
admin.site.register(Act_Pregunta_Opt)
admin.site.register(Inscripcion)
admin.site.register(Prog_Acti)
admin.site.register(Prog_Preg)
admin.site.register(Prog_Tem)
admin.site.register(Prog_Stem)
admin.site.register(Prog_Sstem)
admin.site.register(Cts)
admin.site.register(Ctsd)
admin.site.register(UserActivityLog)

