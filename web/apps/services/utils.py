import os
import json
import requests
import random
import string


def get_obj_with_data(obj, **kwargs):

    t = string.Template(json.dumps(obj['schema']))
    json_obj = json.loads(t.safe_substitute(**kwargs))

    for optional in obj.get('optional', []):
        if optional not in kwargs and optional in json_obj['data']:
            del json_obj['data'][optional]

    for k, v in obj.get('types', {}).items():
        if k in json_obj['data']:
            if v == bool:
                o_value = json_obj['data'][k]
                json_obj['data'][k] = v(1 if o_value == 'true' else 0)

    return json_obj


def generate_password(size=12, chars=string.ascii_letters + string.digits):

    return ''.join(random.choice(chars) for i in range(size))


def get_vmin_response(params, get_status=False, **kwargs):

    new_params = get_obj_with_data(params, **kwargs)

    r = requests.get(
        '{}/{}/remote.cgi'.format(
            os.getenv('VMIN_URL_BASE'), new_params.get('category-cmd')),
        params=new_params.get('data'),
        auth=(os.getenv('VMIN_USER'), os.getenv('VMIN_PSSWD')))
    try:
        json_response = r.json()
        return json_response if get_status else \
            json_response.get('data') if json_response.get('status') == 'success' else {}
    except ValueError:
        return {}


def get_cloudflare_response(params, **kwargs):

    new_params = get_obj_with_data(params, **kwargs)

    headers = {
        'X-Auth-Email': os.getenv('CLOUDFLARE_AUTH_EMAIL'),
        'X-Auth-Key': os.getenv('CLOUDFLARE_AUTH_KEY')
    }

    request_action = getattr(requests, new_params.get('method'))
    r = request_action(
            '{}{}'.format(os.getenv('CLOUDFLARE_URL_BASE'),
                new_params.get('object')),
            headers=headers, json=new_params.get('data'))

    try:
        json_response = r.json()
        if json_response.get('success'):
            return json_response
        else:
            print (json_response)
            return {}
    except ValueError:
        return {}
