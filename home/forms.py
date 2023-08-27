from .models import NewData, PipeData

from django import forms

class UploadDataForm(forms.ModelForm):
    class Meta:
        model = NewData
        fields = ["label", "density", "data"]
        widgets = {
            "label": forms.TextInput(attrs={"class": "form-control", "placeholder": "data name e.g. data1, data2, etc."}),
            "density": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Density (S.I/Field Units)"}),
        }

class PipeDataForm(forms.ModelForm):
    class Meta:
        model = PipeData 
        fields = ["unit", "diameter", "length", "fluid_data"]
        widgets = {}
