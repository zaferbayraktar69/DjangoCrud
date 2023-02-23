from django import forms
from CRUDOperation.models import IhaModel



class IhaForms(forms.ModelForm):
    class Meta:
        model = IhaModel
        fields="__all__"

