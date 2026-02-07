from peewee import *
from playhouse.migrate import *
from models import base


migrator = MySQLMigrator(base)

visible = BooleanField(default=True)

migrate(migrator.add_column("casinouser", "visible", visible))
