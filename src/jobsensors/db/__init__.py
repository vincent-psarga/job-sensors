from peewee import *


db = SqliteDatabase('jobs.db', threadlocals=True)


class BaseModel(Model):
    class Meta:
        database = db
