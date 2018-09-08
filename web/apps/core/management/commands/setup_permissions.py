from apps.sales.models import PUSubscription
from django.core.management.base import BaseCommand
from guardian.shortcuts import assign_perm


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            for obj_subscription in PUSubscription.objects.all():
                assign_perm('view_subscription', obj_subscription.customer, obj_subscription)
                obj_subscription.assign_cservice_perm()
            self.stdout.write(self.style.SUCCESS('Permissions Task done!'))
        except Exception as e:
            self.stdout.write(
                self.style.ERROR('There was an error: {}'.format(str(e))))
