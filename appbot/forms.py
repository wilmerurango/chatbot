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
            'usuario_bot',#este es por defecto
            'colegio',
            'direccion',
            'estado',#este es por defecto
            'fecha_creacion',#este es por defecto
            'grado_cursado',
            'telefono'
        )

 
        
    def __init__(self, *args, **kwargs):  
        super().__init__(*args, **kwargs)  
        for field in iter(self.fields):  
            self.fields[field].widget.attrs.update({  
                'class': 'form-control border border-success',
                'style': 'padding-left: 83px;'
            })
        self.fields['password'].widget.attrs.update({ 
                'type': 'password'
            })


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
            'class': 'datepicker form-control border border-success'  
        })
        self.fields['fecha_final'].widget.attrs.update({  
            'class': 'form-control border border-success'  
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
                'style': 'height: 124px;'  
            })

            
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
                        'style': 'height: 210px;'  
                    })


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


class ActividadDetForm(forms.ModelForm):
    class Meta:
        model = ActividadDet
        
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
                        'style': 'height: 209px;'  
                    })


class ActDetOptForm(forms.ModelForm):
    class Meta:
        model = ActDetOpt
        
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
            })



class ProgresoForm(forms.ModelForm):
    class Meta:
        model = ProgresoDet
        
        fields=(
            '__all__'
        )

        
    def __init__(self, *args, **kwargs):  
        super().__init__(*args, **kwargs)  
        for field in iter(self.fields):  
            self.fields[field].widget.attrs.update({  
                'class': 'form-control border border-success',
            })




class ProgresoForm(forms.ModelForm):
    class Meta:
        model = Progreso
        
        fields=(
            '__all__'
        )

        
    def __init__(self, *args, **kwargs):  
        super().__init__(*args, **kwargs)  
        for field in iter(self.fields):  
            self.fields[field].widget.attrs.update({  
                'class': 'form-control border border-success',
            })