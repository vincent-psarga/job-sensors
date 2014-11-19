import unittest
from mock import Mock
from mock import call

from db.utils import setup_db, drop_db
from jobs.job import Job

from notifiers import notifier
from notifiers.notifier import Notifier


class NotifierTest(unittest.TestCase):
    def setUp(self):
        setup_db()

    def tearDown(self):
        drop_db()

    def test_check(self):
        n = Notifier(Job(1, 'My job'))
        n._check = Mock()

        # There is no status yet, so nothing to check
        n.check()
        self.assertEqual(n._check.call_args_list, [])

        n.job.set_status('Vincent', '', True)
        n.check()
        self.assertEqual(n._check.call_args_list, [
            call()
        ])

        # This status has already been checked, so no new notification
        # will be done.
        n.check()
        self.assertEqual(n._check.call_args_list, [
            call()
        ])

        # If a new status appears, we will perform a check.
        n.job.set_status('Vincent', '1', True)
        n.check()
        self.assertEqual(n._check.call_args_list, [
            call(),
            call()
        ])
