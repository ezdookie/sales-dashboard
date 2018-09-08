from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.urls import reverse
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from guardian.shortcuts import assign_perm
from apps.core.base_model import TimeStampedModel
from apps.services.models import PUService, PUCustomerService


class PUSubscriptionStatus(models.Model):

    name = models.CharField(max_length=100)
    slug = models.SlugField()

    class Meta:
        db_table = 'pu_subscription_status'


class PUSubscription(TimeStampedModel):

    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    service = models.ForeignKey(PUService, on_delete=models.CASCADE, verbose_name='Servicio')
    cservice = models.ForeignKey(PUCustomerService, on_delete=models.CASCADE, blank=True, null=True)
    status = models.ForeignKey(PUSubscriptionStatus, on_delete=models.CASCADE)
    period_months = models.IntegerField()
    register_date = models.DateTimeField(blank=True, null=True)
    renewal_date = models.DateTimeField(blank=True, null=True)
    expiration_date = models.DateTimeField(blank=True, null=True)

    def set_cservice_by_domain(self, domain_name):
        self.cservice = PUCustomerService.objects.get(data__name=domain_name)
        self.assign_cservice_perm()

    def assign_cservice_perm(self):
        assign_perm('view_cservice', self.customer, self.cservice)

    def set_status_by_slug(self, status_slug):
        self.status = PUSubscriptionStatus.objects.get(slug=status_slug)

    def set_register_date(self):
        self.register_date = datetime.now()
        self.set_expiration_date()

    def set_expiration_date(self):
        self.expiration_date = self.register_date + relativedelta(months=self.period_months)

    def get_cservice_link(self):
        return reverse('services:hosting-details', args=[self.cservice.id])

    class Meta:
        db_table = 'pu_subscription'
        permissions = (
            ('view_subscription', 'View subscription'),
        )


class PUOrder(TimeStampedModel):

    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    subscription = models.ForeignKey(PUSubscription, on_delete=models.CASCADE, blank=True, null=True)
    total = models.DecimalField(max_digits=8, decimal_places=2)
    taxes = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        db_table = 'pu_order'


class PUOrderItem(models.Model):

    order = models.ForeignKey(PUOrder, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    taxes = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        db_table = 'pu_order_item'


@receiver(post_save, sender=PUSubscription)
def subscription_post_save(sender, instance, created, **kwargs):
    if created:
        assign_perm('view_subscription', instance.customer, instance)
