from peewee import *
from playhouse.shortcuts import ReconnectMixin
from playhouse.migrate import *
from models import Worker, base


migrator = MySQLMigrator(base)

owner = ForeignKeyField(
    model=Worker, field=Worker.id, null=True, related_name="referals"
)

migrate(
    # migrator.drop_column("worker", "owner_id", owner),
    migrator.add_column("worker", "owner_id", owner)
)
