from .icon_urls import icon_url
import datetime
import flask
import posixpath


def full_computer(computer, jamf_url):
    return {
        'style': "application",
        'title': "Computer Search Result: {}".format(computer['general']['name'].encode('utf-8')),
        'url': posixpath.join(jamf_url, 'computers.html?id={}'.format(computer['general']['id'])),
        'id': computer['general']['udid'],
        'icon': {
            'url': flask.url_for('static', filename='images/images/computers_32.png', _external=True),
            'url@2x': flask.url_for('static', filename='images/computers_64.png', _external=True)
        },
        'attributes': [
            {
                'label': 'ID',
                'value': {'label': str(computer['general']['id'])}
            },
            {
                'label': 'Managed?',
                'value': {'label': str(computer['general']['remote_management']['managed'])}
            },
            {
                'label': 'Serial #',
                'value': {'label': _alt_text(computer['general']['serial_number'])}
            },
            {
                'label': 'MAC Address',
                'value': {'label': _alt_text(computer['general']['mac_address'])}
            },
            {
                'label': 'Assigned User',
                'value': {'label': _alt_text(computer['location']['username'].encode('utf-8'))}
            },
            {
                'label': 'Asset Tag',
                'value': {'label': _alt_text(computer['general']['asset_tag'].encode('utf-8'))}
            },
            {
                'label': 'Model',
                'value': {'label': _alt_text(computer['hardware']['model'])}
            },
            {
                'label': 'OS',
                'value': {'label': '{} {}'.format(
                    _alt_text(computer['hardware']['os_name']),
                    _alt_text(computer['hardware']['os_version'])
                )}
            },
            {
                'label': 'Reported IP',
                'value': {'label': _alt_text(computer['general']['ip_address'])}
            },
            {
                'label': 'Last Check-In',
                'value': {'label': _date_from_epoch(computer['general']['last_contact_time_epoch'])}
            },
            {
                'label': 'Last Inventory',
                'value': {'label': _date_from_epoch(computer['general']['report_date_epoch'])}
            },
            {
                'label': 'UUID',
                'value': {'label': computer['general']['udid']}
            }
        ]
    }


def full_mobile_device(mobile_device, jamf_url):
    return {
        'style': "application",
        'title': "Mobile Device Search Result: {}".format(mobile_device['general']['name'].encode('utf-8')),
        'url': posixpath.join(jamf_url, 'mobileDevices.html?id={}'.format(mobile_device['general']['id'])),
        'id': mobile_device['general']['udid'],
        'icon': icon_url(mobile_device['general']['model_identifier']),
        'attributes': [
            {
                'label': 'ID',
                'value': {'label': str(mobile_device['general']['id'])}
            },
            {
                'label': 'Managed?',
                'value': {'label': str(mobile_device['general']['managed'])}
            },
            {
                'label': 'Ownership',
                'value': {'label': mobile_device['general']['device_ownership_level']}
            },
            {
                'label': 'Supervised?',
                'value': {'label': str(mobile_device['general']['supervised'])}
            },
            {
                'label': 'Serial #',
                'value': {'label': _alt_text(mobile_device['general']['serial_number'])}
            },
            {
                'label': 'MAC Address',
                'value': {'label': _alt_text(mobile_device['general']['wifi_mac_address'])}
            },
            {
                'label': 'Assigned User',
                'value': {'label': _alt_text(mobile_device['location']['username'].encode('utf-8'))}
            },
            {
                'label': 'Asset Tag',
                'value': {'label': _alt_text(mobile_device['general']['asset_tag'].encode('utf-8'))}
            },
            {
                'label': 'Model',
                'value': {'label': _alt_text(mobile_device['general']['model'])}
            },
            {
                'label': 'OS',
                'value': {'label': '''{} {}'''.format(
                    _alt_text(mobile_device['general']['os_type']),
                    _alt_text(mobile_device['general']['os_version'])
                )}
            },
            {
                'label': 'Reported IP',
                'value': {'label': _alt_text(mobile_device['general']['ip_address'])}
            },
            {
                'label': 'Last Inventory',
                'value': {'label': _date_from_epoch(mobile_device['general']['last_inventory_update_epoch'])}
            },
            {
                'label': 'UUID',
                'value': {'label': mobile_device['general']['udid']}
            }
        ]
    }


def full_user(user, jamf_url):
    email = _alt_text(user['email'])
    phone = _alt_text(user['phone_number'])
    position = _alt_text(user['position'])

    description = str()
    description += '<a href="mailto:{0}">{0}</a> &nbsp;| &nbsp;'.format(email) if email != 'none' else ''
    description += '<a href="tel:{0}">{0}</a> &nbsp;| &nbsp;'.format(phone) if phone != 'none' else ''
    description += position if position != 'none' else ''
    description = description if description else 'No additional details available'

    return {
        'style': "application",
        'title': "User Search Result: {}".format(user['full_name'].encode('utf-8')),
        'url': posixpath.join(jamf_url, 'users.html?id={}'.format(user['id'])),
        'id': user['name'],
        'icon': {
            'url': flask.url_for('static', filename='images/user_32.png', _external=True),
            'url@2x': flask.url_for('static', filename='images/user_64.png', _external=True)
        },

        'description': {
            'value': description,
            'format': 'html'
        },
        'attributes': [
            {
                'value': {
                    'icon': {
                        'url': flask.url_for('static', filename='images/computers_32.png', _external=True),
                        'url@2x': flask.url_for('static', filename='images/computers_64.png', _external=True)
                    },
                    'label': '{} Computers'.format(len(user['links']['computers']))
                }
            },
            {
                'value': {
                    'icon': {
                        'url': flask.url_for('static', filename='images/mobiledevices_32.png', _external=True),
                        'url@2x': flask.url_for('static', filename='images/mobiledevices_64.png', _external=True)
                    },
                    'label': '{} Mobile Devices'.format(len(user['links']['mobile_devices']))
                }
            },
            {
                'value': {
                    'icon': {
                        'url': flask.url_for('static', filename='images/peripherals_32.png', _external=True),
                        'url@2x': flask.url_for('static', filename='images/peripherals_64.png', _external=True)
                    },
                    'label': '{} Peripherals'.format(len(user['links']['peripherals']))
                }
            },
            {
                'value': {
                    'icon': {
                        'url': flask.url_for('static', filename='images/vpp_32.png', _external=True),
                        'url@2x': flask.url_for('static', filename='images/vpp_64.png', _external=True)
                    },
                    'label': '{} VPP Content'.format(len(user['links']['vpp_assignments']))
                }
            }
        ]
    }


def mini_computer(title, computer, jamf_url):
    title = "{}: {}".format(title, computer['deviceName'].encode('utf-8'))
    serial = _alt_text(computer['serialNumber'])
    return {
        'style': "application",
        'format': 'compact',
        'title': title,
        'url': posixpath.join(jamf_url, 'computers.html?id={}'.format(computer['jssID'])),
        'id': computer['udid'],
        'activity': {
            'html': '<b>{} ({})</b>'.format(title, serial),
            'icon': {
                'url': flask.url_for('static', filename='images/computers_32.png', _external=True),
                'url@2x': flask.url_for('static', filename='images/computers_64.png', _external=True)
            },
        },
        'attributes': [
            {
                'label': 'ID',
                'value': {'label': str(computer['jssID'])}
            },
            {
                'label': 'Serial #',
                'value': {'label': serial}
            },
            {
                'label': 'Model',
                'value': {'label': _alt_text(computer['model'])}
            },
            {
                'label': 'Assigned User',
                'value': {'label': _alt_text(computer['username'].encode('utf-8'))}
            },
        ]
    }


def mini_mobile(title, mobile_device, jamf_url):
    title = "{}: {}".format(title, mobile_device['deviceName'].encode('utf-8'))
    serial = _alt_text(mobile_device['serialNumber'])
    return {
        'style': "application",
        'format': 'compact',
        'title': title,
        'url': posixpath.join(jamf_url, 'mobileDevices.html?id={}'.format(mobile_device['jssID'])),
        'id': mobile_device['udid'],
        'activity': {
            'html': '<b>{} ({})</b>'.format(title, serial),
            'icon': icon_url(mobile_device['model']),
        },
        'attributes': [
            {
                'label': 'ID',
                'value': {'label': str(mobile_device['jssID'])}
            },
            {
                'label': 'Serial #',
                'value': {'label': serial}
            },
            {
                'label': 'Model',
                'value': {'label': _alt_text(mobile_device['modelDisplay'])}
            },
            {
                'label': 'Assigned User',
                'value': {'label': _alt_text(mobile_device['username'].encode('utf-8'))}
            }
        ]
    }


def patch_update(patch):
    return {
        'style': "application",
        'format': 'compact',
        'title': '{} (click here to view report)'.format(patch['name']),
        'url': patch['reportUrl'],
        'id': '{}-{}'.format(patch['name'], patch['latestVersion']),
        'activity': {
            'html': '<b>Patch Definition Update: {}</b>'.format(patch['name']),
            'icon': {
                'url': flask.url_for('static', filename='images/patch_32.png', _external=True),
                'url@2x': flask.url_for('static', filename='images/patch_64.png', _external=True)
            },
        },
        'attributes': [
            {
                'label': 'Report ID',
                'value': {'label': str(patch['jssID'])}
            },
            {
                'label': 'New Version',
                'value': {'label': patch['latestVersion']}
            },
            {
                'label': 'Date Updated',
                'value': {'label': _date_from_epoch(patch['lastUpdate'])}
            }
        ]
    }


def rest_api(api_op):
    return {
        'style': "application",
        'format': 'compact',
        'title': 'A REST API operation has been performed on the Jamf Pro server',
        'id': '{}-{}-{}-{}'.format(api_op['restAPIOperationType'],api_op['objectTypeName'],
                                   api_op['objectID'], api_op['authorizedUsername']),
        'activity': {
            'html': '<b>REST API: {} {} {}</b>'.format(
                api_op['restAPIOperationType'], api_op['objectTypeName'], api_op['objectID']
            ),
            'icon': {
                'url': flask.url_for('static', filename='images/jamfapi_32.png', _external=True),
                'url@2x': flask.url_for('static', filename='images/jamfapi_64.png', _external=True)
            },
        },
        'attributes': [
            {
                'label': 'Request Type',
                'value': {'label': api_op['restAPIOperationType']}
            },
            {
                'label': 'Object Type',
                'value': {'label': api_op['objectTypeName']}
            },
            {
                'label': 'Object ID',
                'value': {'label': str(api_op['objectID'])}
            },
            {
                'label': 'Object Name',
                'value': {'label': _alt_text(api_op['objectTypeName'])}
            },
            {
                'label': 'Authenticating User',
                'value': {'label': api_op['authorizedUsername']}
            },
            {
                'label': 'Result?',
                'value': {
                    'label': 'Success' if api_op['operationSuccessful'] else 'Fail',
                    'style': 'lozenge-success' if api_op['operationSuccessful'] else 'lozenge-error'
                }
            },
        ]
    }


def _alt_text(string, alt='none'):
    return alt if string is None or string.strip() == "" else string


def _date_from_epoch(epoch_string):
    try:
        epoch = datetime.datetime.utcfromtimestamp(float(epoch_string) / 1000)
    except Exception as e:
        return 'none'

    return epoch.strftime('%Y-%m-%d %H:%M:%S')


def _unix_timestamp():
    return int((datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1)).total_seconds())
