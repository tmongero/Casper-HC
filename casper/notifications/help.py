from .notify import notification
from .jamf_webhooks import webhook_events
import flask
import re

_HELP_REGEX = '^casper\s(?:h|help)\s(.*)'
_SUPPORTED_WEBHOOKS = sorted(webhook_events.keys())


def _help_main(hipchat_room):
    return flask.render_template('notifications/help_main.html', help={
        'webhook_id': hipchat_room.jamf_webhook_id,
        'jamf_configured': hipchat_room.jamf_configured
    })


def _help_webhooks():
    return flask.render_template('notifications/help_webhooks.html', webhooks=_SUPPORTED_WEBHOOKS)


def _parse_command(string):
    match = re.match(_HELP_REGEX, string)
    if not match:
        return 'main'
    else:
        group1 = match.groups()[0]
        if group1 in ('c', 'computer', 'computers'):
            return 'computers'
        elif group1 in ('m', 'mobile', 'mobiles'):
            return 'mobile'
        elif group1 in ('u', 'user', 'users'):
            return 'users'
        elif group1 in ('w', 'webhook', 'webhooks'):
            return 'webhooks'
        else:
            return 'main'


def help_message(hipchat_room, data):
    command = _parse_command(data['item']['message']['message'])
    if command == 'main':
        message = _help_main(hipchat_room)
    elif command == 'webhooks':
        message = _help_webhooks()
    else:
        message = 'Help text not yet available.'

    return notification(message, color='purple', label='Help')
