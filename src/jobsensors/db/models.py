import datetime
from peewee import *

from db import BaseModel

class Job(BaseModel):
    name = CharField(null = True)

class Status(BaseModel):
    job = ForeignKeyField(Job, related_name = 'statuses')
    author = CharField(null = True)
    value = CharField(null = True)
    stable = BooleanField(default = True)
    date = DateTimeField(default = datetime.datetime.now)

    def as_dict(self):
        return {
            'author': self.author,
            'value': self.value,
            'stable': self.stable
        }
