from db import db
from models import Job, Status


def setup_db(*args):
    db.connect()
    db.create_tables([Job, Status])


def drop_db(*args):
    db.connect()
    db.drop_tables([Job, Status])
