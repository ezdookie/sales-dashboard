from django.core.management import call_command
from apps.sales.models import PUSubscription
from apps.services.hosting import params
from apps.services.models import PUService, PUCustomerService
from apps.services.utils import get_vmin_response, get_cloudflare_response, generate_password


def create_hosting(**kwargs):

    service = PUService.objects.get(pk=kwargs.get('service_id'))
    domain_name = kwargs.get('domain_name')

    domain = get_vmin_response(params.CREATE_DOMAIN,
                                get_status=True,
                                domain=domain_name,
                                password=generate_password(),
                                plan_name=service.ext_id)

    if domain.get('status') == 'success':
        print ('Domain sucessfully created!')

        zone = get_cloudflare_response(params.CREATE_ZONE, domain=domain_name)
        zone_id = zone['result']['id']
        print ('Zone sucessfully created!')

        dns_record = get_cloudflare_response(params.CREATE_DNS_RECORD,
                                             zone_id=zone_id,
                                             type='A',
                                             name='@',
                                             content='158.69.216.205',
                                             proxied='true')
        print ('DNS Record A sucessfully created!')

        dns_record = get_cloudflare_response(params.CREATE_DNS_RECORD,
                                             zone_id=zone_id,
                                             type='CNAME',
                                             name='www',
                                             content=domain_name,
                                             proxied='true')
        print ('DNS Record CNAME sucessfully created!')

        dns_record = get_cloudflare_response(params.CREATE_DNS_RECORD,
                                             zone_id=zone_id,
                                             type='CNAME',
                                             name='ftp',
                                             content=domain_name)
        print ('DNS Record CNAME sucessfully created!')

        dns_record = get_cloudflare_response(params.CREATE_DNS_RECORD,
                                             zone_id=zone_id,
                                             type='CNAME',
                                             name='mail',
                                             content=domain_name)
        print ('DNS Record CNAME sucessfully created!')

        dns_record = get_cloudflare_response(params.CREATE_DNS_RECORD,
                                             zone_id=zone_id,
                                             type='MX',
                                             name='@',
                                             content='vps70597.vps.ovh.ca',
                                             priority=5)
        print ('DNS Record MX sucessfully created!')

        dns_record = get_cloudflare_response(params.CREATE_DNS_RECORD,
                                             zone_id=zone_id,
                                             type='TXT', name='@',
                                             content='v=spf1 include:pukutay.com ~all')
        print ('DNS Record TXT sucessfully created!')

        call_command('vminsync')

        obj_subscription = PUSubscription.objects.get(pk=kwargs.get('subscription_id'))
        obj_subscription.set_cservice_by_domain(domain_name)
        obj_subscription.set_status_by_slug('active')
        obj_subscription.set_register_date()
        obj_subscription.save()

    else:
        print ('Something went wrong!')


def create_hosting_user(**kwargs):

    cservice = PUCustomerService.objects.get(pk=kwargs.get('cservice_id'))
    domain_name = cservice.data.get('name')

    get_vmin_response(params.CREATE_USER,
                        domain=domain_name,
                        user=kwargs.get('username'),
                        passwd=kwargs.get('password'),
                        realname=kwargs.get('full_name'))


def delete_hosting_user(**kwargs):

    cservice = PUCustomerService.objects.get(pk=kwargs.get('cservice_id'))
    domain_name = cservice.data.get('name')

    get_vmin_response(params.DELETE_USER,
                        domain=domain_name,
                        user=kwargs.get('username'))
