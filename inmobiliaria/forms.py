from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from dal import autocomplete
from django.core.validators import RegexValidator
from django import forms
from .models import *


# Formulario para el registro de usuarios nuevos:
class UsuarioCreationForm(UserCreationForm):
    fecha_nac = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'placeholder': 'yyyy-mm-dd'}),
        input_formats=['%Y-%m-%d', '%d-%m-%Y']  # Formatos de entrada permitidos
    )

    telefono_validator = RegexValidator(
        regex=r'^\d{8}$',
        message="El número de teléfono debe contener exactamente 8 dígitos.",
        code='invalid_telefono'
    )
    
    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = ('username', 'rut', 'primer_nombre', 'segundo_nombre', 'apellido_paterno', 'apellido_materno', 'fecha_nac', 'telefono', 'email', 'password1', 'password2', 'tipo_usuario')
        labels = {
            'username': 'Nombre de pila o alias',
            'rut': 'Rut (sin puntos ni guión)',
            'primer_nombre': 'Primer nombre',
            'segundo_nombre': 'Segundo nombre',
            'apellido_paterno': 'Primer apellido',
            'apellido_materno': 'Segundo apellido',
            'fecha_nac': 'Fecha de nacimiento',
            'telefono': 'Teléfono celular',
            'email': 'Correo electrónico',
            'password1': 'Constraseña',
            'password2': 'Confirma tu contraseña',
            'tipo_usuario': 'Tipo de usuario',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'rut': forms.TextInput(attrs={'class': 'form-control'}),
            'primer_nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'segundo_nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido_paterno': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido_materno': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_nac': forms.DateInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
            'tipo_usuario': forms.Select(attrs={'class': 'form-control'}),
        }

    telefono = forms.CharField(label='Teléfono celular', validators=[telefono_validator])
    
    # Modificamos el __init__ del formulario para filtrar las opciones de "tipo_usuario"; no queremos que aparezca "Administrador":
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tipo_usuario'].choices = [
            (value, label) for value, label in Usuario.tipo_choices if value != 'administrador'
        ]

    # Funciones de ajuste para guardar la información de nombres y apellidos con el formato: "Nombre", "Apellido" a pesar de cómo ingrese la información el usuario en los campos:
        # Antes de guardar la info en la BD, se ejecutarán los métodos (por eso recibe cleaned_data):
    def clean_primer_nombre(self):
        primer_nombre = self.cleaned_data.get('primer_nombre')
        return primer_nombre.capitalize()
    
    def clean_segundo_nombre(self):
        segundo_nombre = self.cleaned_data.get('segundo_nombre')
        return segundo_nombre.capitalize()

    def clean_apellido_paterno(self):
        apellido_paterno = self.cleaned_data.get('apellido_paterno')
        return apellido_paterno.capitalize()
    
    def clean_apellido_materno(self):
        apellido_materno = self.cleaned_data.get('apellido_materno')
        return apellido_materno.capitalize()
    
    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if not telefono.isdigit():
            raise forms.ValidationError("El número de teléfono debe contener solo dígitos.")
        return telefono


# Formulario para que el usuario pueda modificar su información personal:

# Obtenemos el modelo de usuario que se esté utilizando actualmente en el proyecto
Usuario = get_user_model()

class UsuarioUpdateForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['username', 'primer_nombre', 'segundo_nombre', 'apellido_paterno', 'apellido_materno', 'email', 'telefono']
        labels = {
            'username': 'Nombre de pila o alias',
            'primer_nombre': 'Primer nombre',
            'segundo_nombre': 'Segundo nombre',
            'apellido_paterno': 'Primer apellido',
            'apellido_materno': 'Segundo apellido',
            'telefono': 'Teléfono celular (+569)',
            'email': 'Correo electrónico',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'primer_nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'segundo_nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido_paterno': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido_materno': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }


# Formulario para modificar contraseña:
class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label='Contraseña antigua',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    new_password1 = forms.CharField(
        label='Nueva contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    new_password2 = forms.CharField(
        label='Confirmar nueva contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    # Se define un método para determinar si el usuario ingresa la misma contraseña que desea modificar como nueva contraseña. En este caso, le saltará un mensaje al usuario reparando en su intención.
    def clean(self):
        cleaned_data = super().clean()
        old_password = cleaned_data.get("old_password")
        new_password1 = cleaned_data.get("new_password1")

        # Validar que la nueva contraseña no sea igual a la antigua
        if old_password and new_password1 and old_password == new_password1:
            raise forms.ValidationError(
                "La nueva contraseña no puede ser igual a la contraseña antigua. Por favor, elija una contraseña diferente."
            )

        return cleaned_data


# Formulario de contacto:
class ContactFormForm(forms.ModelForm):
    class Meta:
        model = ContactForm
        fields = ['customer_email', 'customer_name', 'message']
        labels = {
            'customer_email': 'Correo electrónico',
            'customer_name': 'Nombre y apellido',
            'message': 'Mensaje',
        }
        widgets = {
            'customer_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'customer_name': forms.TextInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control'}),
        }


# Formulario para agregar inmuebles (usuario arrendador):
class InmuebleCreateForm(forms.ModelForm):
    class Meta:
        model = Inmueble
        fields = ['nombre', 'descripcion', 'm2_construidos', 'm2_totales', 'n_habitaciones', 'n_banios', 'n_estacionamientos', 'precio', 'tipo_inmueble']
        labels = {
            'nombre': 'Nombre (p.e. Departamento en Santiago centro)',
            'descripcion': 'Descripción del inmueble',
            'm2_construidos': 'Metros cuadrados construídos',
            'm2_totales': 'Metros cuadrados totales del terreno',
            'n_habitaciones': 'Cantidad de habitaciones',
            'n_banios': 'Cantidad de baños',
            'n_estacionamientos': 'Cantidad de estacionamientos (de no haber, indique 0)',
            'precio': 'Coste de arriendo (en miles, p.e. 750000)',
            'tipo_inmueble': 'Tipo de inmueble',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'm2_construidos': forms.NumberInput(attrs={'class': 'form-control'}),
            'm2_totales': forms.NumberInput(attrs={'class': 'form-control'}),
            'n_habitaciones': forms.NumberInput(attrs={'class': 'form-control'}),
            'n_banios': forms.NumberInput(attrs={'class': 'form-control'}),
            'n_estacionamientos': forms.NumberInput(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
            'tipo_inmueble': forms.Select(attrs={'class': 'form-control'}),
        }

# Formulario para agregar dirección del inmueble a crear (usuario arrendador):
class DireccionForm(forms.ModelForm):
    class Meta:
        model = Direccion
        fields = ['calle', 'numero', 'numero_departamento', 'region', 'comuna']   # me arrojaba un error al incluír 'inmueble'; se debía a que inmueble se crea junto con el formulario, por lo que al presionar el botón con la solicitud POST, el inmueble no existe al momento de llamarlo en este formulario... locurote, pero era un error lógico que no saltaba ningún error o indicio por consola, solo se debía ajustar el código para que muestre mensajes de depuración por renderizado http
        labels = {
            'calle': 'Nombre de la calle',
            'numero': 'Número asociado a la calle',
            'numero_departamento': 'Número de departamento (omitir si el tipo de inmueble no es un Departamento)',
            'region': 'Región',
            'comuna': 'Comuna',
        }
        widgets = {
            'calle': forms.TextInput(attrs={'class': 'form-control'}),
            'numero': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_departamento': forms.TextInput(attrs={'class': 'form-control'}),
            'region': forms.Select(attrs={'class': 'form-control'}),
            'comuna': forms.Select(attrs={'class': 'form-control'}),
        }

class InmuebleUpdateForm(forms.ModelForm):
    class Meta:
        model = Inmueble
        fields = ['nombre', 'descripcion', 'm2_construidos', 'm2_totales', 'n_habitaciones', 'n_banios', 'n_estacionamientos', 'precio']
        labels = {
            'nombre': 'Nombre (p.e. Departamento en Santiago centro)',
            'descripcion': 'Descripción del inmueble',
            'm2_construidos': 'Metros cuadrados construídos',
            'm2_totales': 'Metros cuadrados totales del terreno',
            'n_habitaciones': 'Cantidad de habitaciones',
            'n_banios': 'Cantidad de baños',
            'n_estacionamientos': 'Cantidad de estacionamientos (de no haber, indique 0)',
            'precio': 'Coste de arriendo (en miles, p.e. 750000)',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'm2_construidos': forms.NumberInput(attrs={'class': 'form-control'}),
            'm2_totales': forms.NumberInput(attrs={'class': 'form-control'}),
            'n_habitaciones': forms.NumberInput(attrs={'class': 'form-control'}),
            'n_banios': forms.NumberInput(attrs={'class': 'form-control'}),
            'n_estacionamientos': forms.NumberInput(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
            'tipo_inmueble': forms.Select(attrs={'class': 'form-control'}),
        }

    # Lógica de filtrado dinámico, útil para filtrar las comunas que se corresponden con una región seleccionada
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['comuna'].queryset = Comuna.objects.none()

        if 'region' in self.data:
            try:
                region_id = int(self.data.get('region'))
                self.fields['comuna'].queryset = Comuna.objects.filter(region_id=region_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['comuna'].queryset = self.instance.region.comuna_set.order_by('nombre')


