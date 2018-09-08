from django.core.management.base import BaseCommand

from apps.services.hosting import params
from apps.services.models import PUCustomerService, PUService, PUCustomerServiceHostingUser
from apps.services.utils import get_vmin_response


class Command(BaseCommand):

    def get_val(self, dict, value):
        return dict.get(value, [None])[0]

    def handle(self, *args, **options):
        domains = get_vmin_response(params.LIST_DOMAINS)

        for domain in domains:
            values = domain.get('values')
            if values and values.get('id'):
                self.stdout.write('Saving/updating {}...'.format(domain.get('name')))
                try:
                    cservice, created = PUCustomerService.objects.update_or_create(
                        ext_id=self.get_val(values, 'id'),
                        defaults={
                            'service': PUService.objects.get(ext_id=self.get_val(values, 'plan')),
                            'data': {
                                'name': domain.get('name'),
                                'username': self.get_val(values, 'username'),
                                'password': self.get_val(values, 'password'),
                                'server_quota': self.get_val(values, 'server_quota'),
                                'server_quota_used': self.get_val(values, 'server_quota_used'),
                                'server_block_quota': self.get_val(values, 'server_block_quota'),
                                'server_block_quota_used': self.get_val(values, 'server_block_quota_used'),
                            }
                        }
                    )

                    if created:
                        self.stdout.write('Saving users for {}...'.format(domain.get('name')))
                        users = get_vmin_response(params.LIST_USERS, domain=domain.get('name'))
                        for user in users:
                            user_vals = user.get('values')
                            real_name = self.get_val(user_vals, 'real_name')
                            if real_name:
                                PUCustomerServiceHostingUser.objects.create(
                                    cservice=cservice,
                                    full_name=real_name,
                                    username=self.get_val(user_vals, 'email_address').split('@')[0]
                                )
                        self.stdout.write('Done!')

                    self.stdout.write(
                        self.style.SUCCESS('{} was succefully saved/updated!'.format(domain.get('name'))))
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR('There was an error: {}'.format(str(e))))

        self.stdout.write(self.style.SUCCESS('Sync complete!'))
