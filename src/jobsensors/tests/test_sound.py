import unittest
from mock import Mock
from mock import call

import os
import urllib2
from time import sleep

from db.utils import setup_db, drop_db
from jobs import response
from notifiers import sound


class ResponseSoundNotifierTest(unittest.TestCase):
    def setUp(self):
        setup_db()

    def tearDown(self):
        drop_db()

    def test_check(self):
        pass

    def test_play(self):
        os.system = Mock()

        notifier = sound.ResponseSoundNotifier(None)
        notifier.play('something.mp3')

        # It plays the given file using mpg123
        os.system.assert_called_with('mpg123 something.mp3')

    def test_check(self):
        job = response.Response(1, 'My site', 'http://www.example.com')
        notifier = sound.ResponseSoundNotifier(job)

        notifier.play = Mock()

        # There is no status yet, so nothing to play
        notifier.check()
        self.assertEqual(notifier.play.call_args_list, [])

        job.set_status('', 0.1, True)
        notifier.check()
        self.assertEqual(notifier.play.call_args_list, [])

        # The site is down: a notification is played
        job.set_status('', '', True, True)
        notifier.check()
        self.assertEqual(notifier.play.call_args_list, [
            call('sounds/site-down.mp3')
        ])

        # The notifier knows it already notified this error, so it does not
        # play the sound again.
        notifier.check()
        self.assertEqual(notifier.play.call_args_list, [
            call('sounds/site-down.mp3')
        ])

        # The site is still down but we do not play a new notification
        # (otherwise no one will be able to concentrate and put the site back)
        job.set_status('', '', True, True)
        notifier.check()
        self.assertEqual(notifier.play.call_args_list, [
            call('sounds/site-down.mp3')
        ])

        # The site is back, a sound is played
        job.set_status('', '0.1', True)
        notifier.check()
        self.assertEqual(notifier.play.call_args_list, [
            call('sounds/site-down.mp3'),
            call('sounds/site-back.mp3')
        ])

        # But it is played only once.
        job.set_status('', '0.1', True)
        notifier.check()
        self.assertEqual(notifier.play.call_args_list, [
            call('sounds/site-down.mp3'),
            call('sounds/site-back.mp3')
        ])
