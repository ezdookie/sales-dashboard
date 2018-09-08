from django.contrib.postgres.fields import JSONField
from django.db import models
from apps.core.base_model import TimeStampedModel


class PUCategoryService(models.Model):

    name = models.CharField(max_length=100)
    slug = models.SlugField()

    class Meta:
        db_table = 'pu_category_service'


class PUService(models.Model):

    category = models.ForeignKey(PUCategoryService, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    ext_id = models.CharField(max_length=128, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'pu_service'


class PUCustomerService(TimeStampedModel):

    service = models.ForeignKey(PUService, on_delete=models.CASCADE)

    ext_id = models.CharField(max_length=32, blank=True, null=True)
    data = JSONField(blank=True, null=True)

    class Meta:
        db_table = 'pu_cservice'
        permissions = (
            ('view_cservice', 'View cservice'),
        )


class PUCustomerServiceLog(TimeStampedModel):

    cservice = models.ForeignKey(PUCustomerService, on_delete=models.CASCADE)
    message = models.TextField()

    class Meta:
        db_table = 'pu_cservice_log'


class PUCustomerServiceHostingUser(TimeStampedModel):

    cservice = models.ForeignKey(PUCustomerService, on_delete=models.CASCADE, related_name='hostingusers')
    full_name = models.CharField(max_length=100, verbose_name='Nombre completo')
    username = models.CharField(max_length=100, verbose_name='Dirección e-mail')
    data = JSONField(blank=True, null=True)

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'pu_cservice_hosting_user'
