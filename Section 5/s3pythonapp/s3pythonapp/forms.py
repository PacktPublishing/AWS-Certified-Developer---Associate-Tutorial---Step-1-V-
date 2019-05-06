from django import forms
from django.forms.formsets import BaseFormSet, formset_factory

class FilesForm(forms.Form):
    image_description = forms.CharField(max_length=100)
    image_file = forms.ImageField()
