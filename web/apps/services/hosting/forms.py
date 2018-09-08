from django import forms
from apps.services.models import PUCustomerServiceHostingUser


class CreateHostingUser(forms.ModelForm):

    password = forms.CharField(required=True, label='Contraseña')

    class Meta:
        model = PUCustomerServiceHostingUser
        fields = ['full_name', 'username']
