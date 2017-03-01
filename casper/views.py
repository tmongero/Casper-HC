from . import app, db
from .models import HipchatRoom
from .notifications import *
from .utilities import verify_jwt, validate_room_jwt
import flask


@app.errorhandler(400)
def error_400(error):
    return flask.jsonify({'Error': {'code': 400, 'message': 'bad request'}}), 400


@app.errorhandler(401)
def error_401(error):
    return flask.jsonify({'Error': {'code': 401, 'message': 'unauthorized'}}), 401


@app.errorhandler(403)
def error_403(error):
    return flask.jsonify({'Error': {'code': 403, 'message': 'forbidden'}}), 403


@app.errorhandler(404)
def error_404(error):
    return flask.jsonify({'Error': {'code': 404, 'message': 'not found'}}), 404


@app.route("/")
def hello():
    return "The friendly ghost..."


@app.route('/hipchat/capabilities')
def hipchat_capabilities():
    return flask.jsonify(**app.config['HIPCHAT_CAPABILITIES'])


@app.route('/hipchat/installable', methods=['POST'])
def hipchat_installable():
    data = flask.request.get_json()
    new_hipchat_room = HipchatRoom(data)
    db.session.add(new_hipchat_room)
    db.session.commit()

    message = '''<p>Casper has been installed for this room! To receive notifications point webhooks to this URL:</p>
    <p><b>https://{}/jss/{}</b></p><br>
    <p>Type <b>'casper help'</b> to learn more about using this plugin.</p>'''.format(
        app.config['SERVER_DOMAIN'], new_hipchat_room.jamf_webhook_id
    )

    send_notification(
        new_hipchat_room.hipchat_token, new_hipchat_room.hipchat_room_id,
        message, color='purple', notify=True
    )
    return '', 200


@app.route('/hipchat/installable/<oauth_id>', methods=['DELETE'])
def hipchat_uninstall(oauth_id):
    hipchat_room = HipchatRoom.query.filter(HipchatRoom.hipchat_oauth_id == oauth_id).first()
    if hipchat_room:
        db.session.delete(hipchat_room)
        db.session.commit()
    return '', 204


@app.route('/hipchat/configure')
def hipchat_configure():
    return flask.render_template('configure.html')


@app.route('/hipchat/configure/update', methods=['POST'])
def hipchat_configure_update():
    signed_token = flask.request.args.get('signed_request')
    installed_room = verify_jwt(signed_token)
    try:
        installed_room.jamf_auth = (
            flask.request.values.get('jamf_url'),
            flask.request.values.get('jamf_username'),
            flask.request.values.get('jamf_password')
        )
        db.session.commit()
    except:
        flask.flash('The service account could not be validated. Please verify the URL, username and password.', 'error')
    else:
        flask.flash('The service account has been validated and saved!', 'success')
        send_notification(
            installed_room.hipchat_token, installed_room.hipchat_room_id,
            '''<p><b>A Jamf Pro service account has been configured!</b></p>
            <p>You may now search your Jamf Pro server's inventory from this room.''',
            color='purple', notify=True
        )

    return flask.redirect(flask.url_for('hipchat_configure'))


@app.route('/message/help', methods=['POST'])
@validate_room_jwt(requires_jamf_configured=False)
def message_help(hipchat_room):
    return flask.jsonify(help_message(hipchat_room, flask.request.get_json()))


@app.route('/message/version', methods=['POST'])
@validate_room_jwt
def message_version(hipchat_room):
    return flask.jsonify(jamf_version(hipchat_room))


@app.route('/message/computers', methods=['POST'])
@validate_room_jwt
def message_computers(hipchat_room):
    return flask.jsonify(search_computers(hipchat_room, flask.request.get_json()))


@app.route('/message/mobiledevices', methods=['POST'])
@validate_room_jwt
def message_mobiledevices(hipchat_room):
    return flask.jsonify(search_mobile_devices(hipchat_room, flask.request.get_json()))


@app.route('/message/users', methods=['POST'])
@validate_room_jwt
def message_users(hipchat_room):
    return flask.jsonify(search_users(hipchat_room, flask.request.get_json()))


@app.route('/jss/<webhook_id>', methods=['POST'])
def jamf_inbound_webhook(webhook_id):
    hipchat_room = HipchatRoom.query.filter(HipchatRoom.jamf_webhook_id == webhook_id).first_or_404()
    webhook_event(hipchat_room, flask.request.get_json())
    return '', 204
