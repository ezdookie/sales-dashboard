LIST_DOMAINS = {
    'schema': {
        'category-cmd': 'virtual-server',
        'data': {
            'program': 'list-domains',
            'multiline': '',
            'toplevel': '',
            'json': 1,
        }
    }
}

CREATE_DOMAIN = {
    'schema': {
        'category-cmd': 'virtual-server',
        'data': {
            'program': 'create-domain',
            'domain': '${domain}',
            'pass': '${password}',
            'features-from-plan': '',
            'plan': '${plan_name}',
            'json': 1,
        }
    }
}

LIST_USERS = {
    'schema': {
        'category-cmd': 'virtual-server',
        'data': {
            'program': 'list-users',
            'multiline': '',
            'domain': '${domain}',
            'json': 1
        }
    }
}

CREATE_USER = {
    'schema': {
        'category-cmd': 'virtual-server',
        'data': {
            'program': 'create-user',
            'domain': '${domain}',
            'user': '${user}',
            'pass': '${passwd}',
            'real': '${realname}'
        }
    }
}

DELETE_USER = {
    'schema': {
        'category-cmd': 'virtual-server',
        'data': {
            'program': 'delete-user',
            'domain': '${domain}',
            'user': '${user}'
        }
    }
}

CREATE_ZONE = {
    'schema': {
        'object': 'zones',
        'method': 'post',
        'data': {
            'name': '${domain}'
        }
    }
}

ZONE_LIST = {
    'schema': {
        'object': 'zones',
        'method': 'get'
    }
}

CREATE_DNS_RECORD = {
    'schema': {
        'object': 'zones/${zone_id}/dns_records',
        'method': 'post',
        'data': {
            'type': '${type}',
            'name': '${name}',
            'content': '${content}',
            'proxied': '${proxied}',
            'priority': '${priority}'
        }
    },
    'types': {
        'proxied': bool
    },
    'optional': [
        'proxied', 'priority'
    ]
}

LIST_DNS_RECORD = {
    'schema': {
        'object': 'zones/${zone_id}/dns_records',
        'method': 'get'
    }
}
