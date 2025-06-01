from django import forms
from django.contrib import admin
from .models import ClientInteraction, Role, Employee

class ClientInteractionForm(forms.ModelForm):
    class Meta:
        model = ClientInteraction
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        operator_role = Role.objects.filter(role__iexact='operator').first()
        if operator_role:
            self.fields['responsible'].queryset = Employee.objects.filter(user_roles__role=operator_role).distinct()
        else:
            self.fields['responsible'].queryset = Employee.objects.none()
