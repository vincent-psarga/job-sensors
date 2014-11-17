import unittest
from mock import Mock

from db.utils import setup_db, drop_db
from db.models import Job as JobDb
from db.models import Status

from jobs.job import Job


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

    def test_status(self):
        job = Job(1, 'My job')

        # By default there is no status
        self.assertEqual(job.status, None)

        job.set_status('Vincent', 'success', True)
        self.assertEqual(job.status.value, 'success')

        job.set_status('Laurent', 'building', False)
        self.assertEqual(job.status.value, 'building')

    def test_set_status(self):
        job = Job(1, 'My job')

        # At startup, there is no statuses
        self.assertEqual(Status.select().count(), 0)

        job.set_status('Vincent', 'failure', True)
        # Set status create a new entry in the database
        self.assertEqual(Status.select().count(), 1)

    def test_previous_status(self):
        job = Job(1, 'My job')

        # By default there is previous status
        self.assertEqual(job.previous_status, None)

        # We need at least two statuses to get a previous one
        job.set_status('Vincent', 'success', True)
        self.assertEqual(job.previous_status, None)

        job.set_status('Laurent', 'building', False)
        self.assertEqual(job.previous_status.value, 'success')

        # Previous status only fetches the previous stable one
        job.set_status('Laurent', 'building', False)
        job.set_status('Laurent', 'building', False)
        job.set_status('Laurent', 'building', False)
        self.assertEqual(job.previous_status.value, 'success')

    def test_update_status(self):
        job = Job(1, 'My job')
        job.check = Mock(return_value={
            'author': 'Vincent',
            'value': 'building',
            'stable': False
        })

        self.assertEqual(job.status, None)

        job.update_status()
        # The result of 'check' is added as the new status
        self.assertEqual(job.status.as_dict(), {
            'author': 'Vincent',
            'value': u'building',
            'stable': False
        })

        job.update_status()
        # If the result did not change, there is no new insertion
        # in the database
        self.assertEqual(Status.select().count(), 1)

        job.check = Mock(return_value={
            'author': 'Vincent',
            'value': 'failure',
            'stable': True
        })

        job.update_status()
        self.assertEqual(job.status.as_dict(), {
            'author': 'Vincent',
            'value': 'failure',
            'stable': True
        })
        self.assertFalse(job.status.error)

        job.check = Mock(side_effect=KeyError('oups, got an error'))

        # If any exception is raised, an error status is created
        job.update_status()
        self.assertEqual(job.status.as_dict(), {
            'author': '',
            'value': "Exception: 'oups, got an error'",
            'stable': True
        })
        self.assertTrue(job.status.error)
