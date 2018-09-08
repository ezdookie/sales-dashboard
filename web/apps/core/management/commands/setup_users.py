from apps.core.models import PUUser
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            for user in PUUser.objects.all():
                user.set_password(user.password)
                user.save()
            self.stdout.write(self.style.SUCCESS('Users Task done!'))
        except Exception as e:
            self.stdout.write(
                self.style.ERROR('There was an error: {}'.format(str(e))))
