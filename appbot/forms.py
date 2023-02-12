from django import forms
from django.conf import settings
# from django.contrib.admin import widgets
# import datetime
from .models import *


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        
        fields=(
            # '__all__'
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
            'tipo_user',#este es por defecto
            'colegio',
            'direccion',
            'estado',#este es por defecto
            'fecha_creacion',#este es por defecto
            'grado_cursado',
            'telefono',
            'fecha_naci',
            'genero',
            'estrato'
        )

 
        
    def __init__(self, *args, **kwargs):  
        super().__init__(*args, **kwargs)  
        for field in iter(self.fields):  
            self.fields[field].widget.attrs.update({  
                'class': 'form-control border-right border-bottom border-left border-success',
                'style': 'padding-left: 83px;'
            })
        
        self.fields['fecha_creacion'].widget.attrs.update({ 
                'class': 'form-control border-right border-bottom border-left border-success datetime',
                'autocomplete':'off'
            })
        self.fields['password'].widget.attrs.update({ 
                'type': 'hidden'
            })
        self.fields['estado'].widget.attrs.update({ 
                'type': 'hidden'
            })

        # self.fields['fecha_naci'].widget.attrs.update({ 
        #         'class': 'form-control border-right border-bottom border-left border-success datetime',
        #         'autocomplete':'off'
        #     })


class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        
        fields=(
            '__all__'
        )

        
    def __init__(self, *args, **kwargs):  
        super().__init__(*args, **kwargs)  
        for field in iter(self.fields):  
            self.fields[field].widget.attrs.update({  
                'class': 'form-control border border-success',
                # 'style': 'padding-left: 83px;'
            })

        self.fields['descripcion'].widget.attrs.update({  
            'style': 'height: 296px;'  
        })
        self.fields['fecha_inicial'].widget.attrs.update({  
            'class': 'form-control border border-success datetime',
            'autocomplete':'off'
        })
        self.fields['fecha_final'].widget.attrs.update({  
            'class': 'form-control border border-success datetime',
            'autocomplete':'off'
        })




class TipoActividadForm(forms.ModelForm):
    class Meta:
        model = TipoActividad
        
        fields=(
            '__all__'
        )

        
    def __init__(self, *args, **kwargs):  
        super().__init__(*args, **kwargs)  
        for field in iter(self.fields):  
            self.fields[field].widget.attrs.update({  
                'class': 'form-control border border-success',
                # 'style': 'padding-left: 83px;'
            })


class TemaForm(forms.ModelForm):
    class Meta:
        model = Tema
        
        fields=(
            '__all__'
        )

        
    def __init__(self, *args, **kwargs):  
        super().__init__(*args, **kwargs)  
        for field in iter(self.fields):  
            self.fields[field].widget.attrs.update({  
                'class': 'form-control border border-success',
                # 'style': 'padding-left: 83px;'
            })
        self.fields['descripcion'].widget.attrs.update({  
                'style': 'height: 438px; '  
            })
        self.fields['recurso_link_video'].widget.attrs.update({  
                'style': 'height: 95px; '  #visibility: hidden;
            })
        # self.fields['recurso_archivo'].widget.attrs.update({  
        #         'style': 'visibility: hidden;'  
        #     })


            
class SubtemaForm(forms.ModelForm):
    class Meta:
        model = Subtema
        
        fields=(
            '__all__'
        )

        
    def __init__(self, *args, **kwargs):  
        super().__init__(*args, **kwargs)  
        for field in iter(self.fields):  
            self.fields[field].widget.attrs.update({  
                'class': 'form-control border border-success',
                # 'style': 'padding-left: 83px;'
            })
        self.fields['descripcion'].widget.attrs.update({  
                        'style': 'height: 503px;'
                    })
        self.fields['recurso_link_video'].widget.attrs.update({  
                'style': 'height: 74px; ' #visibility: hidden;
            })
        # self.fields['recurso_archivo'].widget.attrs.update({  
        #         'style': 'visibility: hidden;'  
        #     })

        

class SubSubtemaForm(forms.ModelForm):
    class Meta:
        model = SubSubtema
        
        fields=(
            '__all__'
        )

        
    def __init__(self, *args, **kwargs):  
        super().__init__(*args, **kwargs)  

        for field in iter(self.fields):  
            self.fields[field].widget.attrs.update({  
                'class': 'form-control border border-success',
                # 'style': 'padding-left: 83px;'
            })
        self.fields['descripcion'].widget.attrs.update({  
                        'style': 'height: 418px;'  
                    })
        self.fields['recurso_link_video'].widget.attrs.update({  
                'style': 'height: 74px;'#visibility: hidden;
            })
        # self.fields['recurso_archivo'].widget.attrs.update({  
        #         'style': 'visibility: hidden;'  
        #     })


        self.fields['subtema'].queryset = Subtema.objects.none()   

        if 'tema' in self.data:
            try:
                tema_id = int(self.data.get('tema'))
                
                self.fields['subtema'].queryset = Subtema.objects.filter(tema_id=tema_id).order_by('nombre')
            except (ValueError, TypeError):
                print('Error') # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['subtema'].queryset = self.instance.tema.subtema_set.order_by('nombre') # self.instance.tema.subtema.order_by('nombre')




class CurTemStemForm(forms.ModelForm):
    class Meta:
        model = CurTemStem
        
        fields=(
            '__all__'
        )

        
    def __init__(self, *args, **kwargs):  
        super().__init__(*args, **kwargs)  
        for field in iter(self.fields):  
            self.fields[field].widget.attrs.update({  
                'class': 'form-control border border-success',
                # 'style': 'padding-left: 83px;'
            })
        self.fields['fecha_i'].widget.attrs.update({  
                        'class': 'form-control border border-success datetime',
                        'autocomplete':"off"
                    })
        self.fields['fecha_f'].widget.attrs.update({  
                        'class': 'form-control border border-success datetime',
                        'autocomplete':"off" 
                    })

        # self.fields['subtema'].queryset = Subtema.objects.none()
        # self.fields['subSubtema'].queryset = Subtema.objects.none()

        # # print("wesro q es ? ", self.data)

        # if ('tema' in self.data) or ('subtema' in self.data):
        #     try:
        #         tema_id = int(self.data.get('tema'))
        #         self.fields['subtema'].queryset = Subtema.objects.filter(tema_id=tema_id).order_by('nombre')

        #         subtema_id = int(self.data.get('subtema'))
        #         self.fields['subSubtema'].queryset = SubSubtema.objects.filter(subtema_id=subtema_id).order_by('nombre')
        #     except (ValueError, TypeError):
        #         print('Error') # invalid input from the client; ignore and fallback to empty City queryset
        # elif self.instance.pk:
        #     print(self.fields['subSubtema'].queryset)
        #     self.fields['subtema'].queryset =  self.instance.tema.subtema_set.order_by('nombre')
        #     self.fields['subSubtema'].queryset = self.instance.subtema.subsubtema_set.order_by('nombre') # self.instance.tema.subtema.order_by('nombre')



class ActividadForm(forms.ModelForm):
    class Meta:
        model = Actividad
        
        fields=(
            '__all__'
        )

        
    def __init__(self, *args, **kwargs):  
        super().__init__(*args, **kwargs)  
        for field in iter(self.fields):  
            self.fields[field].widget.attrs.update({  
                'class': 'form-control border border-success',
                # 'style': 'padding-left: 83px;'
            })
        self.fields['descripcion'].widget.attrs.update({  
                        'style': 'height: 383px;'  
                    })
        self.fields['fecha_i'].widget.attrs.update({  
                        'class': 'form-control border border-success datetime',
                        'autocomplete':"off"
                    })
        self.fields['fecha_f'].widget.attrs.update({  
                        'class': 'form-control border border-success datetime',
                        'autocomplete':"off" 
                    })


class Act_PreguntaForm(forms.ModelForm):
    class Meta:
        model = Act_Pregunta
        
        fields=(
            '__all__'
        )

        
    def __init__(self, *args, **kwargs):  
        super().__init__(*args, **kwargs)  
        for field in iter(self.fields):  
            self.fields[field].widget.attrs.update({  
                'class': 'form-control border border-success',
                # 'style': 'padding-left: 83px;'
            })
        self.fields['descripcion'].widget.attrs.update({  
                        'style': 'height: 123px;'  
                    })


class Act_Pregunta_OptForm(forms.ModelForm):
    class Meta:
        model = Act_Pregunta_Opt
        
        fields=(
            '__all__'
        )

        
    def __init__(self, *args, **kwargs):  
        super().__init__(*args, **kwargs)  
        for field in iter(self.fields):  
            self.fields[field].widget.attrs.update({  
                'class': 'form-control border border-success',
                # 'style': 'heigth: 209px;'
            })
        self.fields['descripcion'].widget.attrs.update({  
                        'style': 'height: 209px;'  
                    })



class InscripcionForm(forms.ModelForm):
    class Meta:
        model = Inscripcion
        
        fields=(
            '__all__'
        )

        
    def __init__(self, *args, **kwargs):  
        super().__init__(*args, **kwargs)  
        for field in iter(self.fields):  
            self.fields[field].widget.attrs.update({  
                'class': 'form-control border border-success',
                'readonly':''
            })



class Prog_ActiForm(forms.ModelForm):
    class Meta:
        model = Prog_Acti
        
        fields=(
            '__all__'
        )

        
    def __init__(self, *args, **kwargs):  
        super().__init__(*args, **kwargs)  
        for field in iter(self.fields):  
            self.fields[field].widget.attrs.update({  
                'class': 'form-control border border-success',
            })




class Prog_PregForm(forms.ModelForm):
    class Meta:
        model = Prog_Preg
        
        fields=(
            '__all__'
        )

        
    def __init__(self, *args, **kwargs):  
        super().__init__(*args, **kwargs)  
        for field in iter(self.fields):  
            self.fields[field].widget.attrs.update({  
                'class': 'form-control border border-success',
            })



class CtsForm(forms.ModelForm):
    class Meta:
        model = Cts
        
        fields=(
            '__all__'
        )

        
    def __init__(self, *args, **kwargs):  
        # print('sto es selft -------------',self)
        super().__init__(*args, **kwargs)  
        for field in iter(self.fields):  
            self.fields[field].widget.attrs.update({  
                'class': 'form-control border border-success',
            })

        self.fields['subtema'].queryset = Subtema.objects.none()

        if 'curTemStem' in self.data:
            try:
                curTemStem_id = int(self.data.get('curTemStem'))
                tem_curTemStem = CurTemStem.objects.get(id = curTemStem_id)
                self.fields['subtema'].queryset = Subtema.objects.filter(tema__id=tem_curTemStem.tema.id)
            except (ValueError, TypeError):
                print('Error') # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            # print('qui estoy -------------: ',self.instance.curTemStem.tema.subtema_set)
            self.fields['subtema'].queryset = self.instance.curTemStem.tema.subtema_set



class CtsdForm(forms.ModelForm):
    class Meta:
        model = Ctsd
        
        fields=(
            '__all__'
        )

        
    def __init__(self, *args, **kwargs):  
        super().__init__(*args, **kwargs)  
        for field in iter(self.fields):  
            self.fields[field].widget.attrs.update({  
                'class': 'form-control border border-success',
            })
            
        self.fields['subSubtema'].queryset = SubSubtema.objects.none()

        if 'cts' in self.data:
            try:
                cts_id = int(self.data.get('cts'))

                tem_cts = Cts.objects.get(id = cts_id)

                self.fields['subSubtema'].queryset = SubSubtema.objects.filter(subtema__id = tem_cts.subtema.id)
            except (ValueError, TypeError):
                print('Error') # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            # print('qui estoy -------------: ',self.instance.cts.subtema.subsubtema_set)
            self.fields['subSubtema'].queryset = self.instance.cts.subtema.subsubtema_set




# class Prog_TemForm(forms.ModelForm):
#     class Meta:
#         model = Prog_Tem
        
#         fields=(
#             '__all__'
#         )

        
#     def __init__(self, *args, **kwargs):  
#         super().__init__(*args, **kwargs)  
#         for field in iter(self.fields):  
#             self.fields[field].widget.attrs.update({  
#                 'class': 'form-control border border-success',
#             })
#         self.fields['fecha_i'].widget.attrs.update({  
#                         'class': 'form-control border border-success datetime',
#                         'autocomplete':"off"
#                     })
#         self.fields['fecha_f'].widget.attrs.update({  
#                         'class': 'form-control border border-success datetime',
#                         'autocomplete':"off" 
#                     })



# class Prog_StemForm(forms.ModelForm):
#     class Meta:
#         model = Prog_Stem
        
#         fields=(
#             '__all__'
#         )

        
#     def __init__(self, *args, **kwargs):  
#         super().__init__(*args, **kwargs)  
#         for field in iter(self.fields):  
#             self.fields[field].widget.attrs.update({  
#                 'class': 'form-control border border-success',
#             })
#         self.fields['fecha_i'].widget.attrs.update({  
#                         'class': 'form-control border border-success datetime',
#                         'autocomplete':"off"
#                     })
#         self.fields['fecha_f'].widget.attrs.update({  
#                         'class': 'form-control border border-success datetime',
#                         'autocomplete':"off" 
#                     })





# class Prog_SstemForm(forms.ModelForm):
#     class Meta:
#         model = Prog_Sstem
        
#         fields=(
#             '__all__'
#         )

        
#     def __init__(self, *args, **kwargs):  
#         super().__init__(*args, **kwargs)  
#         for field in iter(self.fields):  
#             self.fields[field].widget.attrs.update({  
#                 'class': 'form-control border border-success',
#             })
#         self.fields['fecha_i'].widget.attrs.update({  
#                         'class': 'form-control border border-success datetime',
#                         'autocomplete':"off"
#                     })
#         self.fields['fecha_f'].widget.attrs.update({  
#                         'class': 'form-control border border-success datetime',
#                         'autocomplete':"off" 
#                     })