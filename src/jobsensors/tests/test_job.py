import unittest

from db.utils import setup_db, drop_db
from db.models import Job as JobDb

from jobs.job import Job
from jobs.ci import TravisCI

class JobTest(unittest.TestCase):

    def setUp(self):
        setup_db()

    def tearDown(self):
        drop_db()

    def test_creation(self):
        self.assertEqual(JobDb.select().count(), 0)

        # A model with the correct name is created if needed
        job = Job(10, 'My job')
        self.assertEqual(JobDb.select().count(), 1)
        self.assertEqual(JobDb.get(JobDb.id == 10).name, 'My job')

        # If the id is already in use, the db entry is updated
        job = Job(10, 'Ho hi')
        self.assertEqual(JobDb.select().count(), 1)
        self.assertEqual(JobDb.get(JobDb.id == 10).name, 'Ho hi')


    def test_status_update(self):
        job = Job(1, 'My job')

        # By default there is no status
        self.assertEqual(job.status, None)

        # Nor previous status
        self.assertEqual(job.previous_status, None)

        job.set_status('Vincent', 'success', True)
        self.assertEqual(job.status.value, 'success')
        self.assertEqual(job.previous_status, None)

        job.set_status('Laurent', 'building', False)
        self.assertEqual(job.status.value, 'building')
        self.assertEqual(job.previous_status.value, 'success')

        # Previous status only fetches the previous stable one
        job.set_status('Laurent', 'building', False)
        job.set_status('Laurent', 'building', False)
        job.set_status('Laurent', 'building', False)
        self.assertEqual(job.previous_status.value, 'success')
