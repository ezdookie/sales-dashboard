from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class PUUser(AbstractUser):

    email = models.EmailField(_('email address'), unique=True)
    is_reseller = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = 'pu_user'


class PUResellerProfile(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='reseller_profile')
    service_hosting_gb_limit = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'pu_reseller_profile'


class PUCustomerProfile(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='customer_profile')
    reseller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='customer_reseller_profile', blank=True, null=True)

    class Meta:
        db_table = 'pu_customer_profile'
