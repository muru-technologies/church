from django import forms
from . models import ChildDedication

class ChildDedicationForm(forms.ModelForm):
    class Meta:
        model = ChildDedication
        fields = "__all__"