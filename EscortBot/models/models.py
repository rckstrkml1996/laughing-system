import peewee

from data.config import DATABASE_FILE

base = peewee.SqliteDatabase(DATABASE_FILE)



class BaseModel(peewee.Model):
	class Meta:
		database = base

class User(BaseModel):
	cid = peewee.IntegerField(unique=True)
	balance = peewee.IntegerField(default=0)
	refer = peewee.IntegerField(default=1)
	username = peewee.CharField(default="Юзернейм скрыт")
	fullname = peewee.CharField(default="Без имени")

	def __str__(self):
		return f'#{self.id} {self.cid}'


class Payment(BaseModel):
	cid = peewee.IntegerField()
	done = peewee.BooleanField(default=False)

class Girl(BaseModel):
	photos = peewee.CharField()
	info = peewee.CharField(default="Без описания")
	price = peewee.IntegerField(default=1500)


base.connect()
base.create_tables([User, Payment, Girl])
