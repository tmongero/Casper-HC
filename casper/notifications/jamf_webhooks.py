from .card_views import mini_computer, mini_mobile, patch_update, rest_api
from .notify import send_notification


def _computer_added(data, hipchat_room):
    return '''A new computer has been added to the Jamf Pro server:<br>
    <b>ID:</b> {}  <b>Name:</b> {} <b>Username:</b> {}'''.format(
        data['jssID'], data['deviceName'], data['username']
    ), mini_computer('Computer Added', data, hipchat_room.jamf_url), 'green'


def _computer_checkin(data, hipchat_room):
    return '''A computer check-in has occurred:<br>
    <b>ID:</b> {}  <b>Name:</b> {} <b>Username:</b> {}'''.format(
        data['jssID'], data['deviceName'], data['username']
    ), mini_computer('Computer Check-In', data, hipchat_room.jamf_url), 'gray'


def _computer_inventory(data, hipchat_room):
    return '''A computer has submitted a new inventory report:<br>
    <b>ID:</b> {}  <b>Name:</b> {} <b>Username:</b> {}'''.format(
        data['jssID'], data['deviceName'], data['username']
    ), mini_computer('Computer Inventory Submitted', data, hipchat_room.jamf_url), 'gray'


def _jss_shutdown(data, hipchat_room):
    message = 'The Jamf Pro web app <b>{}</b> has initiated a shutdown'.format(data['jssUrl'])
    if data['isClusterMaster']:
        message += ' <b>(master)</b>'

    return message, None, 'red'


def _jss_startup(data, hipchat_room):
    message = 'The Jamf Pro web app <b>{}</b> has started up'.format(data['jssUrl'])
    if data['isClusterMaster']:
        message += ' <b>(master)</b>'

    return message, None, 'green'


def _mobile_checkin(data, hipchat_room):
    return '''A mobile device check-in has occurred:<br>
    <b>ID:</b> {}  <b>Name:</b> {} <b>Username:</b> {}'''.format(
        data['jssID'], data['deviceName'], data['username']
    ), mini_mobile('Mobile Device Check-In', data, hipchat_room.jamf_url), 'gray'


def _mobile_enrolled(data, hipchat_room):
    return '''A mobile device has been enrolled to the Jamf Pro server:<br>
    <b>ID:</b> {}  <b>Name:</b> {} <b>Username:</b> {}'''.format(
        data['jssID'], data['deviceName'], data['username']
    ), mini_mobile('Mobile Device Enrolled', data, hipchat_room.jamf_url), 'green'


def _mobile_unenrolled(data, hipchat_room):
    return '''A mobile device has been unenrolled from the Jamf Pro server:<br>
    <b>ID:</b> {}  <b>Name:</b> {} <b>Username:</b> {}'''.format(
        data['jssID'], data['deviceName'], data['username']
    ), mini_mobile('Mobile Device Unenrolled', data, hipchat_room.jamf_url), 'yellow'


def _patch_title_updated(data, hipchat_room):
    card = patch_update(data)
    return '''<p>Your JSS has received a new Patch Definition Update <i>(<a href='{}'>Click here to view the report</a>)</i></p>
    <p>Name: <b>{}</b> &nbsp;| &nbsp;Version: <b>{}</b></p>'''.format(
        data['reportUrl'], data['name'], data['latestVersion']
    ), card, 'yellow'


def _rest_api_operation(data, hipchat_room):
    if hipchat_room.jamf_auth and data['authorizedUsername'] != hipchat_room.jamf_auth[0]:
        message = '''<p>A REST API action has been performed on the Jamf Pro server:</p>
        <p><b>API Object Type</b> {} <b>Name:</b> {} <b>ID:</b> {}</p>
        <p><b>User:</b> {} <b>Action:</b> {} <b>Success?</b> {}</p>'''.format(
            data['objectTypeName'],
            data['objectName'],
            data['objectID'],
            data['authorizedUsername'],
            data['restAPIOperationType'],
            data['operationSuccessful']
        )
        card = rest_api(data)
    else:
        message = None
        card = None

    return message, card, 'yellow'


webhook_events = {
    'ComputerAdded': _computer_added,
    'ComputerCheckIn': _computer_checkin,
    'ComputerInventoryCompleted': _computer_inventory,
    'JSSShutdown': _jss_shutdown,
    'JSSStartup': _jss_startup,
    'MobileDeviceCheckIn': _mobile_checkin,
    'MobileDeviceEnrolled': _mobile_enrolled,
    'MobileDeviceUnEnrolled': _mobile_unenrolled,
    'PatchSoftwareTitleUpdated': _patch_title_updated,
    'RestAPIOperation': _rest_api_operation
}


def webhook_event(hipchat_room, webhook):
    event_type = webhook['webhook']['webhookEvent']
    if event_type in webhook_events:
        message, card, color = webhook_events[event_type](webhook['event'], hipchat_room)
        if message:
            send_notification(
                hipchat_room.hipchat_token,
                hipchat_room.hipchat_room_id,
                message, color=color, card=card, label='Jamf Pro Notification'
            )
