
from django import forms

from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


from django import forms
from django.contrib.auth.models import User

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def clean_password2(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password and password2 and password != password2:
            raise forms.ValidationError("Passwords don't match.")

        return password2
    
    
    
    
# prediction/forms.py

from django import forms

class CropPredictionForm(forms.Form):
    Nitrogen = forms.FloatField(label='Nitrogen', widget=forms.NumberInput(attrs={'step': '0.01'}))
    Phosphorus = forms.FloatField(label='Phosphorus', widget=forms.NumberInput(attrs={'step': '0.01'}))
    Potassium = forms.FloatField(label='Potassium', widget=forms.NumberInput(attrs={'step': '0.01'}))
    Temperature = forms.FloatField(label='Temperature', widget=forms.NumberInput(attrs={'step': '0.01'}))
    Humidity = forms.FloatField(label='Humidity', widget=forms.NumberInput(attrs={'step': '0.01'}))
    Ph = forms.FloatField(label='pH', widget=forms.NumberInput(attrs={'step': '0.01'}))
    Rainfall = forms.FloatField(label='Rainfall', widget=forms.NumberInput(attrs={'step': '0.01'}))



from django import forms
from .models import CropProduction  # Assurez-vous d'importer votre modèle

class CropProductionForm(forms.ModelForm):
    class Meta:
        model = CropProduction
        fields = ['district', 'crop', 'season', 'area', 'yield1']


