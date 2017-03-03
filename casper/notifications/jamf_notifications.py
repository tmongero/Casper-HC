from .card_views import full_computer, full_mobile_device, full_user
from .notify import notification
import flask
import posixpath
import re
import requests

_HEADERS = {'Accept': 'application/json'}
_COMPUTER_REGEX = '^casper\s(?:c|computers?)\s(.*)'
_MOBILE_REGEX = '^casper\s(?:m|mobiles?)\s(.*)'
_USER_REGEX = '^casper\s(?:u|users?)\s(.*)'


def _parse_parameter(regex, data):
    match = re.match(regex, data['item']['message']['message'])
    return match.groups()[0] if match else None


def jamf_version(hipchat_room):
    r = requests.get(
        posixpath.join(hipchat_room.jamf_url, 'JSSResource/jssuser'),
        headers=_HEADERS, auth=hipchat_room.jamf_auth
    )
    if not r.ok:
        return {}

    version = r.json()['user']['version']
    message = "<b>{}</b> is running version <b>{}</b>".format(hipchat_room.jamf_url, version)
    return notification(message, label='Jamf Pro Version')


def search_computers(hipchat_room, hipchat_data):
    parameter = _parse_parameter(_COMPUTER_REGEX, hipchat_data)
    r = requests.get(
        posixpath.join(hipchat_room.jamf_url, 'JSSResource/computers/match', parameter).encode('utf-8'),
        headers=_HEADERS, auth=hipchat_room.jamf_auth
    )
    if not r.ok:
        return {}

    data = r.json()
    count = len(data['computers'])
    card = None

    if 0 < count < 2:
        r = requests.get(
            posixpath.join(hipchat_room.jamf_url, 'JSSResource/computers/id', str(data['computers'][0]['id'])),
            headers=_HEADERS, auth=hipchat_room.jamf_auth
        )
        if not r.ok:
            return {}

        print r.status_code, r.url

        computer = r.json()['computer']
        message = '''<p><b>Computer:</b> {} <i>(<a href='{}'>Click here to view in Jamf Pro</a>)</i>
        <p><ul>
            <li><b>ID:</b> {}</li>
            <li><b>Serial #:</b> {}</li>
            <li><b>macOS:</b> {}</li>
        </ul></p>'''.format(
            computer['general']['name'].encode('utf-8'),
            posixpath.join(hipchat_room.jamf_url, 'computers.html?id={}'.format(computer['general']['id'])),
            computer['general']['id'],
            computer['general']['serial_number'],
            computer['hardware']['os_version']
        )
        card = full_computer(computer, hipchat_room.jamf_url)

    elif count > 1:
        computers = {
            'count': count,
            'label': 'Computer',
            'over': True if count > 25 else False,
            'parameter': parameter,
            'results': list()
        }

        for i in range(len(data['computers'][:25])):
            computer = data['computers'][i]
            computers['results'].append({
                'url': posixpath.join(hipchat_room.jamf_url, 'computers.html?id={}'.format(computer['id'])),
                'id': computer['id'],
                'name': computer['name'],
                'serial': computer['serial_number'],
                'mac_address': computer['mac_address'],
                'user': computer['username']
            })

        message = flask.render_template('notifications/search_results.html', device_list=computers)

    else:
        message = 'There are no matching computer records for the parameter: <i>{}</i>'.format(
            parameter.encode('utf-8'))

    return notification(message, card=card if card else None)


def search_mobile_devices(hipchat_room, hipchat_data):
    parameter = _parse_parameter(_MOBILE_REGEX, hipchat_data)
    r = requests.get(
        posixpath.join(hipchat_room.jamf_url, 'JSSResource/mobiledevices/match', parameter).encode('utf-8'),
        headers=_HEADERS, auth=hipchat_room.jamf_auth
    )
    if not r.ok:
        return {}

    data = r.json()
    count = len(data['mobile_devices'])
    card = None

    if 0 < count < 2:
        r = requests.get(
            posixpath.join(hipchat_room.jamf_url, 'JSSResource/mobiledevices/id', str(data['mobile_devices'][0]['id'])),
            headers=_HEADERS, auth=hipchat_room.jamf_auth
        )
        if not r.ok:
            return {}

        mobile_device = r.json()['mobile_device']
        message = '''<p><b>Mobile Device:</b> {} <i>(<a href='{}'>Click here to view in Jamf Pro</a>)</i>
        <p><ul>
            <li><b>ID:</b> {}</li>
            <li><b>Serial #:</b> {}</li>
            <li><b>OS:</b> {}</li>
        </ul></p>'''.format(
            mobile_device['general']['name'].encode('utf-8'),
            posixpath.join(hipchat_room.jamf_url, 'mobileDevices.html?id={}'.format(mobile_device['general']['id'])),
            mobile_device['general']['id'],
            mobile_device['general']['serial_number'],
            mobile_device['general']['os_version']
        )
        card = full_mobile_device(mobile_device, hipchat_room.jamf_url)

    elif count > 1:
        mobile_devices = {
            'count': count,
            'label': 'Mobile Device',
            'over': True if count > 25 else False,
            'parameter': parameter,
            'results': list()
        }

        for i in range(len(data['mobile_devices'][:25])):
            mobile_device = data['mobile_devices'][i]
            mobile_devices['results'].append({
                'url': posixpath.join(hipchat_room.jamf_url, 'mobileDevices.html?id={}'.format(mobile_device['id'])),
                'id': mobile_device['id'],
                'name': mobile_device['name'],
                'serial': mobile_device['serial_number'],
                'mac_address': mobile_device['mac_address'],
                'user': mobile_device['username']
            })

        message = flask.render_template('notifications/search_results.html', device_list=mobile_devices)

    else:
        message = 'There are no matching mobile device records for the parameter: <i>{}</i>'.format(
            parameter.encode('utf-8'))

    return notification(message, card=card if card else None)


def search_users(hipchat_room, hipchat_data):
    parameter = _parse_parameter(_USER_REGEX, hipchat_data)
    user_type = 'email' if re.match('^.+@.+\..+$', parameter) else 'name'
    r = requests.get(
        posixpath.join(hipchat_room.jamf_url, 'JSSResource/users', user_type, parameter),
        headers=_HEADERS, auth=hipchat_room.jamf_auth
    )
    if not r.ok:
        message = 'There are no matching user records for the parameter: <i>{}</i>'.format(parameter.encode('utf-8'))
        card = None

    else:
        if user_type == 'name':
            message = 'Placeholder'
            card = full_user(r.json()['user'], hipchat_room.jamf_url)
        else:
            message = 'Multiple Results'
            card = full_user(r.json()['users'][0], hipchat_room.jamf_url)

    return notification(message, card=card)
