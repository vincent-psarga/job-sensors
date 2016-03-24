from peewee import DoesNotExist

from db import models


class Job(object):
    def __init__(self, id, name):
        self.db_job = models.Job.get_or_create(id=id)[0]
        self.db_job.name = name
        self.db_job.save()

    def update_status(self):
        try:
            new_status = self.check()
        except Exception as e:
            self.set_status(
                author='',
                value='Exception: %s' % str(e),
                stable=True,
                error=True
            )
            return

        current = self.status
        if (current is None) or (current.as_dict() != new_status):
            self.set_status(**new_status)

    def check(self):
        pass

    @property
    def id(self):
        return self.db_job.id

    @property
    def name(self):
        return self.db_job.name

    @property
    def status(self):
        try:
            return self.statuses.get()
        except DoesNotExist:
            return None

    def set_status(self, author, value, stable, error=False):
        models.Status.create(
            job=self.db_job,
            author=author,
            value=value,
            stable=stable,
            error=error
        )

    @property
    def previous_status(self):
        current = self.status
        if current is None:
            return None

        try:
            return self.statuses.where(models.Status.date < current.date, models.Status.stable == True).get()
        except DoesNotExist:
            return None

    @property
    def statuses(self):
        return self.db_job.statuses.order_by(models.Status.date.desc())
