import datetime
from peewee import *

from db import BaseModel


class Job(BaseModel):
    name = CharField(null=True)


class Status(BaseModel):
    job = ForeignKeyField(Job, related_name='statuses')
    author = CharField(null=True)
    value = CharField(null=True)
    stable = BooleanField(default=True)
    error = BooleanField(default=False)
    date = DateTimeField(default=datetime.datetime.now)

    def as_dict(self):
        return {
            'author': self.author,
            'value': self.value,
            'stable': self.stable
        }

    @property
    def color(self):
        try:
            return self.colors.get()
        except DoesNotExist:
            return None


class StatusColor(BaseModel):
    status = ForeignKeyField(Status, related_name='colors')
    color = CharField(default='000000')
    blink = BooleanField(default=False)
    pulse = BooleanField(default=False)
