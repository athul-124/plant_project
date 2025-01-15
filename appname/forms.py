# forms.py
from django import forms
from .models import SpaceImage

class SpaceImageForm(forms.ModelForm):
    class Meta:
        model = SpaceImage
        fields = ['image', 'description']


class PlantAdvisorForm(forms.Form):
    light_level = forms.ChoiceField(choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')])
    humidity = forms.ChoiceField(choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')])
    plant_type = forms.CharField(max_length=100)
    watering_frequency = forms.ChoiceField(choices=[('Weekly', 'Weekly'), ('Monthly', 'Monthly'), ('Daily', 'Daily')])
    soil_type = forms.ChoiceField(choices=[('Loamy', 'Loamy'), ('Sandy', 'Sandy'), ('Clay', 'Clay')])