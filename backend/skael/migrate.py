from flask_migrate import MigrateCommand, Migrate
from flask_script import Manager
from skael.skael import create_app

app = create_app(None)

from skael.models import db
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

manager.run()