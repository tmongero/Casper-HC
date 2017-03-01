from .models import HipchatRoom
from .notifications import send_notification
import flask
import functools
import jwt


def verify_jwt(signed_token):
    unvalidated_token = jwt.decode(signed_token, verify=False)
    hipchat_room = HipchatRoom.query.filter(HipchatRoom.hipchat_oauth_id == unvalidated_token['iss']).first_or_404()
    try:
        jwt.decode(signed_token, hipchat_room.hipchat_oauth_secret)
    except jwt.exceptions.DecodeError:
        flask.flash('Unable to decode the Java Web Token provided', 'error')
        flask.abort(401)
    except jwt.ExpiredSignatureError:
        flask.flash('The provided Java Web Token is expired: try refreshing the page', 'error')
        flask.abort(401)
    else:
        return hipchat_room


def validate_room_jwt(function=None, requires_jamf_configured=True):
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            try:
                token = flask.request.headers.get('Authorization').split()[1]
            except:
                flask.abort(401)

            hipchat_room = verify_jwt(token)

            if requires_jamf_configured and not hipchat_room.jamf_configured:
                message = "You must first configure a Jamf Pro service account to use this feature."
                send_notification(hipchat_room.hipchat_token, hipchat_room.hipchat_room_id, message, color='yellow')
                flask.abort(400)

            return f(hipchat_room, *args, **kwargs)

        return wrapper

    return decorator(function) if function else decorator
