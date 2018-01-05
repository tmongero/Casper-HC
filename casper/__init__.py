import flask
from . import config
from .capabilities import get_capabilties
from flask_sqlalchemy import SQLAlchemy
from .security import AESCipher

app = flask.Flask(__name__)
app.config.from_object(config)
# app.config.from_envvar('FLASK_CONFIG_FILE')

app.config['HIPCHAT_CAPABILITIES'] = get_capabilties(app.config['SERVER_DOMAIN'])

db = SQLAlchemy(app)

cipher = AESCipher(app.config['DATABASE_KEY'])
print(cipher)


from . import models
from . import views
