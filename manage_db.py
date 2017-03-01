from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from casper import app, db

migrate = Migrate(app, db, '/var/web-app/migrations')

manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    '''
    $ python manage_db.py db init
    $ python manage_db.py db migrate
    $ python manage_db.py db upgrade
    $ python manage_db.py db --help
    '''
    manager.run()
