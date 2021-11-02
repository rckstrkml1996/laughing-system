from peewee import *
from playhouse.shortcuts import ReconnectMixin
from playhouse.migrate import *


class DB(ReconnectMixin, MySQLDatabase):
    pass


base = DB(
    "bot",
    user="belicoff",
    password="belicoffdev",
    host="127.0.0.1",
    port=3306,
    charset="utf8mb4",  # for emoji and symbols)
)


migrator = MySQLMigrator(base)

service_id = IntegerField(default=0)
service_name = CharField(default="ХЗ Сервис")

migrate(
    migrator.rename_column("profit", "service", "service_id"),
    migrator.add_column("profit", "service_name", service_name),
)
