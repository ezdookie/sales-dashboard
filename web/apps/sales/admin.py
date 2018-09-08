from django.contrib import admin
from apps.sales.models import PUSubscription
from guardian.admin import GuardedModelAdmin


class SubscriptionAdmin(GuardedModelAdmin):
    pass
admin.site.register(PUSubscription, SubscriptionAdmin)
