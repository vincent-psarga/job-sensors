from db import db
from models import Job, Status, StatusColor


def setup_db(*args):
    db.connect()
    db.create_tables([Job, Status, StatusColor])


def drop_db(*args):
    db.connect()
    db.drop_tables([Job, Status, StatusColor])
