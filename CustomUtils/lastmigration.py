import os

from peewee import *
from playhouse.migrate import *

from customutils.confparse import Config


path = os.path.normpath(os.path.join(os.getcwd(), "../config.cfg"))
config = Config("Settings", path, {"migrate": "1"})

base = MySQLDatabase(
    config("base_name"),
    user=config("base_user"),
    password=config("base_password"),
    host="127.0.0.1",
    port=3306,
    charset="utf8mb4",  # for emoji and symbols)
)

migrator = MySQLMigrator(base)

username = CharField(default="Без юзернейма", null=True)

migrate(migrator.add_column("escortuser", "username", username))
