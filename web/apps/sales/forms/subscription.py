from django import forms
from datetime import datetime
from apps.sales.models import PUSubscription
from apps.services.models import PUService


class SubscriptionCreateForm(forms.ModelForm):

    domain_name = forms.CharField(label='Nombre de dominio')

    class Meta:
        model = PUSubscription
        fields = ['service']
