import unittest
from mock import Mock
from mock import call

import config
from db.utils import setup_db, drop_db
from jobs.job import Job
from jobs import ci
from jobs import response

from notifiers import colors


class ColorNotifierTest(unittest.TestCase):
    def setUp(self):
        setup_db()

    def tearDown(self):
        drop_db()

    def test__check(self):
        job = Job(1, 'My job')
        notifier = colors.ColorNotifier(job)
        notifier.assign_color = Mock()

        # If the status is in error, we get a blinking error color.
        job.set_status('Author', 'Some status', True, True)
        notifier.check()
        self.assertEqual(job.status.color.color, config.ERROR_COLOR)
        self.assertTrue(job.status.color.blink)
        self.assertFalse(job.status.color.pulse)
        notifier.assign_color.assertNotCalled()

        # If there is no error, assign_color is called with the current status
        job.set_status('Author', 'Some status', True)
        notifier.check()
        notifier.assign_color.assert_called_with(job.status)

    def test_assign_color(self):
        # This must be implemented by sub classes
        with self.assertRaises(NotImplementedError):
            colors.ColorNotifier(None).assign_color(None)

    def test_set_color(self):
        job = Job(1, 'My job')
        job.set_status('Author', 'Some status', True)
        notifier = colors.ColorNotifier(job)

        self.assertIsNone(job.status.color)

        notifier.set_color('ABCDEF')
        color = job.status.color
        self.assertEqual(color.color, 'ABCDEF')
        self.assertFalse(color.blink)
        self.assertFalse(color.pulse)


class ResponseColorNotifierTest(unittest.TestCase):
    def setUp(self):
        setup_db()

    def tearDown(self):
        drop_db()

    def test_assign_color(self):
        job = response.Response(1, 'My site', 'http://example.com', min_time = 0, max_time = 1)
        notifier = colors.ResponseColorNotifier(job)

        # When the response is close to the minimum one, we get the color
        # for fast response.
        job.set_status('', '0', True)
        notifier.assign_color(job.status)
        self.assertEqual(job.status.color.color, config.RESPONSE_FAST_COLOR)
        self.assertFalse(job.status.color.blink)
        self.assertFalse(job.status.color.pulse)

        # When we are over the slow limit, we get the other one.
        job.set_status('', '1.5', True)
        notifier.assign_color(job.status)
        self.assertEqual(job.status.color.color, config.RESPONSE_SLOW_COLOR)
        self.assertFalse(job.status.color.blink)
        self.assertFalse(job.status.color.pulse)


        # And in the middle we get something in between those colors.
        job.set_status('', '0.5', True)
        notifier.assign_color(job.status)
        self.assertEqual(job.status.color.color, '7f4000')
        self.assertFalse(job.status.color.blink)
        self.assertFalse(job.status.color.pulse)


class CIColorNotifierTest(unittest.TestCase):
    def setUp(self):
        setup_db()

    def tearDown(self):
        drop_db()

    def test_assign_color(self):
        job = ci.CI(1, 'My job')
        notifier = colors.CIColorNotifier(job)

        # When the build fails, we get the failure color
        job.set_status('', ci.STATUS_FAILURE, True)
        notifier.assign_color(job.status)
        self.assertEqual(job.status.color.color, config.CI_FAILURE_COLOR)
        self.assertFalse(job.status.color.blink)
        self.assertFalse(job.status.color.pulse)

        job.set_status('', ci.STATUS_SUCCESS, True)
        notifier.assign_color(job.status)
        self.assertEqual(job.status.color.color, config.CI_SUCCESS_COLOR)
        self.assertFalse(job.status.color.blink)
        self.assertFalse(job.status.color.pulse)

        job.set_status('', ci.STATUS_PENDING, True)
        notifier.assign_color(job.status)
        self.assertEqual(job.status.color.color, config.CI_PENDING_COLOR)
        self.assertFalse(job.status.color.blink)
        self.assertFalse(job.status.color.pulse)

        # If the status is not stable, the color should pulse.
        job.set_status('', ci.STATUS_PENDING, False)
        notifier.assign_color(job.status)
        self.assertEqual(job.status.color.color, config.CI_PENDING_COLOR)
        self.assertFalse(job.status.color.blink)
        self.assertTrue(job.status.color.pulse)