import os


DEBUG = True
SERVER_DOMAIN = 'jamfychat.ngrok.io'

DATABASE_KEY = '\x83\xa7\xb5\xda\x94\r\x8e_\x91\xf2\xb4u\xe7\xb5\x9e\xfe\xfb\xf2\xd8\\+\xe5\x91!w\x98%0\xecs\xce\xb6'
SECRET_KEY = '\xac\xa8\xe7\x85Q\xea\x96\x04\xefa\x9d\x18\xed\xfb2\xf1\xa5\xc20\xbc\xe5r\xe8v\xf3\xb0R\x85.!\x9a\xd5'

# MYSQL_SERVER = os.getenv('MYSQL_SERVER')
# MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')
# MYSQL_USER = os.getenv('MYSQL_USER')
# MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')

# HIPCHAT_OAUTH2_TOKEN = "bce28a0ee3a88149c0c9ec503402c9"

MYSQL_SERVER = 'localhost'
MYSQL_ROOT_PASSWORD = 'teejSQLok!'
MYSQL_DATABASE = 'casperHC'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'teejSQLok!'

SQLALCHEMY_DATABASE_URI = os.getenv(
    'SQLALCHEMY_DATABASE_URI',
    'mysql+pymysql://{}:{}@{}/{}?charset=utf8'.format(MYSQL_USER, MYSQL_PASSWORD, MYSQL_SERVER, MYSQL_DATABASE)
)
SQLALCHEMY_TRACK_MODIFICATIONS = False
