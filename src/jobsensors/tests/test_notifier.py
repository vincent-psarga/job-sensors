import unittest
from mock import Mock
from mock import call

from db.utils import setup_db, drop_db
from jobs.job import Job

from notifiers.notifier import Notifier


class NotifierTest(unittest.TestCase):
    def setUp(self):
        setup_db()

    def tearDown(self):
        drop_db()

    def test_check(self):
        notifier = Notifier(Job(1, 'My job'))
        notifier._check = Mock()

        # There is no status yet, so nothing to check
        notifier.check()
        self.assertEqual(notifier._check.call_args_list, [])

        notifier.job.set_status('Vincent', '', True)
        notifier.check()
        self.assertEqual(notifier._check.call_args_list, [
            call()
        ])

        # This status has already been checked, so no new notification
        # will be done.
        notifier.check()
        self.assertEqual(notifier._check.call_args_list, [
            call()
        ])

        # If a new status appears, we will perform a check.
        notifier.job.set_status('Vincent', '1', True)
        notifier.check()
        self.assertEqual(notifier._check.call_args_list, [
            call(),
            call()
        ])
