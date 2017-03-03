import json
import requests


def send_notification(token, room, message, message_format='html', color='gray', card=None, label='', notify=False):
    """
    Send a notification to a HipChat chat room

    :param token: HipChat API access token
    :param room: HipChat room ID
    :param message: HTML message (or string if message_format='text')
    :param message_format: 'html' or 'text'
    :param color: Message background color
    :param card: HipChat card view JSON string
    :param label: Optional label for displayed message
    :param notify: Notify chat room 'True' or 'False'
    """
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(token)
    }

    data = notification(message, message_format, color, card, label, notify)

    response = requests.post(
        'https://api.hipchat.com/v2/room/{}/notification'.format(room),
        headers=headers, data=json.dumps(data)
    )

    if not response.ok:
        print response.text
        response.raise_for_status()


def notification(message, message_format='html', color='gray', card=None, label='', notify=False):
    message_format = message_format if message_format in ('html', 'text') else 'html'
    color = color if color in ('yellow', 'green', 'red', 'purple', 'gray', 'random') else 'gray'
    data = {
        'card': card,
        "color": color,
        'from': label,
        "message": message,
        'message_format': message_format,
        'notify': notify
    }
    return data
