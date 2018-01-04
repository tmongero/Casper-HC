from . import cipher, db
import datetime
import json
import os
import requests
import uuid


def _new_uuid():
    """Wrapper to return string format of uuid.uuid4() for jamf_webhook_id attribute"""
    return str(uuid.uuid4())


class HipChatRoom(db.Model):
    __tablename__ = 'HipChatRooms'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    hipchat_oauth_id = db.Column(db.String(255), unique=True)
    _hipchat_oauth_secret = db.Column(db.String(255), unique=True)

    hipchat_room_id = db.Column(db.Integer)
    hipchat_group_id = db.Column(db.Integer)

    _jamf_username = db.Column(db.String(255), nullable=True)
    _jamf_password = db.Column(db.String(255), nullable=True)
    jamf_url = db.Column(db.String(128), nullable=True)
    jamf_configured = db.Column(db.Boolean, default=False)

    jamf_webhook_id = db.Column(db.String(36), unique=True, default=_new_uuid)

    _hipchat_access_token = db.Column(db.String(255))
    _hipchat_token_expiration = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, hipchat_data):
        """
        Instantiate a new HipChat Room object
        :param hipchat_data: HipChat Access Token (JSON) object
        """
        self.hipchat_oauth_id = hipchat_data['oauthId']
        self.hipchat_oauth_secret = hipchat_data['oauthSecret']

        self.hipchat_room_id = hipchat_data['roomId']
        self.hipchat_group_id = hipchat_data['groupId']

        self._generate_hipchat_token()

    def __repr__(self):
        return "<HipChatRoom: {}>".format(self.hipchat_oauth_id)

    def _generate_hipchat_token(self):
        data = {'grant_type': 'client_credentials', 'scope': 'send_notification'}
        headers = {'content-type': 'application/json'}
        auth = (
            self.hipchat_oauth_id,
            self.hipchat_oauth_secret
        )

        r = requests.post('https://api.hipchat.com/v2/oauth/token', data=json.dumps(data), headers=headers, auth=auth)

        if not r.ok:
            r.raise_for_status()

        new_access_token = r.json()
        # self._hipchat_access_token = cipher.encrypt(new_access_token['access_token'])
        self._hipchat_access_token = new_access_token['access_token']
        self._hipchat_token_expiration = datetime.datetime.utcnow() + datetime.timedelta(
            seconds=int(new_access_token['expires_in'])
        )
        db.session.commit()

    @property
    def hipchat_oauth_secret(self):
        # return cipher.decrypt(self._hipchat_oauth_secret)
        return self._hipchat_oauth_secret

    @hipchat_oauth_secret.setter
    def hipchat_oauth_secret(self, value):
        # self._hipchat_oauth_secret = cipher.encrypt(value)
        self._hipchat_oauth_secret = value

    @property
    def hipchat_token(self):
        if datetime.datetime.utcnow() > self._hipchat_token_expiration:
            self._generate_hipchat_token()

        # return cipher.decrypt(self._hipchat_access_token)
        return self._hipchat_access_token

    @property
    def jamf_auth(self):
        if self._jamf_username and self._jamf_password:
            # return cipher.decrypt(self._jamf_username), cipher.decrypt(self._jamf_password)
            return self._jamf_username, self._jamf_password
        else:
            return None

    @jamf_auth.setter
    def jamf_auth(self, value):
        if not isinstance(value, (list, tuple)):
            raise TypeError("'value' must be a list or tuple: (url, username, password)")

        url, username, password = value
        headers = {'Accept': 'application/json'}

        r = requests.get(os.path.join(url, 'JSSResource/jssuser'), headers=headers, auth=(username, password))
        if not r.ok:
            r.raise_for_status()

        self.jamf_url = url
        # self._jamf_username = cipher.encrypt(username)
        # self._jamf_password = cipher.encrypt(password)
        self._jamf_username = username
        self._jamf_password = password
        self.jamf_configured = True
        db.session.commit()
