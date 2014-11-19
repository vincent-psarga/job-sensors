import unittest
from mock import Mock
from mock import call

import os

from db.utils import setup_db, drop_db
from jobs.job import Job
from jobs import ci
from jobs import response

from notifiers import notifier
from notifiers import sound


class GetNotifierTests(unittest.TestCase):
    def setUp(self):
        setup_db()

    def tearDown(self):
        drop_db()

    def test_get_notifiers(self):
        notifier.get_notifiers = Mock()

        sound.get_notifiers([])
        notifier.get_notifiers.assert_called_with(
            [],
            sound.SOUND_NOTIFIER_MAPPING,
            sound.config.CUSTOM_SOUND_NOTIFIERS
        )

    def test_check_mapping(self):
        # Just to be sure we have the correct values ;)

        job = Job(1, 'Whatever')
        ci_job = ci.CI(2, 'My job')
        response_job = response.Response(3, 'My job', 'http://www.example.com')

        notifiers = sound.get_notifiers([job, ci_job, response_job])

        self.assertEqual(len(notifiers), 2)
        self.assertIsInstance(
            notifiers[0],
            sound.CISoundNotifier
        )
        self.assertIsInstance(
            notifiers[1],
            sound.ResponseSoundNotifier
        )

class ResponseSoundNotifierTest(unittest.TestCase):
    def setUp(self):
        setup_db()

    def tearDown(self):
        drop_db()

    def test_play(self):
        os.system = Mock()

        notifier = sound.ResponseSoundNotifier(None)
        notifier.play('something.mp3')

        # It plays the given file using mpg123
        os.system.assert_called_with('mpg123 something.mp3')

    def test__check(self):
        job = response.Response(1, 'My site', 'http://www.example.com')
        notifier = sound.ResponseSoundNotifier(job)

        notifier.play = Mock()

        job.set_status('', 0.1, True)
        notifier._check()
        self.assertEqual(notifier.play.call_args_list, [])

        # The site is down: a notification is played
        job.set_status('', '', True, True)
        notifier._check()
        self.assertEqual(notifier.play.call_args_list, [
            call('sounds/site-down.mp3')
        ])

        # The site is still down but we do not play a new notification
        # (otherwise no one will be able to concentrate and put the site back)
        job.set_status('', '', True, True)
        notifier._check()
        self.assertEqual(notifier.play.call_args_list, [
            call('sounds/site-down.mp3')
        ])

        # The site is back, a sound is played
        job.set_status('', '0.1', True)
        notifier._check()
        self.assertEqual(notifier.play.call_args_list, [
            call('sounds/site-down.mp3'),
            call('sounds/site-back.mp3')
        ])


class CISoundNotifierTest(unittest.TestCase):
    def setUp(self):
        setup_db()

    def tearDown(self):
        drop_db()

    def test__check(self):
        job = Job(1, 'Some job')
        notifier = sound.CISoundNotifier(job)
        notifier.say = Mock()

        # If the first build passes, nothing happens
        job.set_status('Vincent', ci.STATUS_SUCCESS, True)
        notifier._check()
        self.assertEqual(notifier.say.call_args_list, [])

        # If it fails, a notification is triggered
        job.set_status('Vincent', ci.STATUS_FAILURE, True)
        notifier._check()
        self.assertEqual(notifier.say.call_args_list, [
            call('Vincent has broken Some job')
        ])

        # If it is fixed, another notification is trigerred
        job.set_status('Vincent', ci.STATUS_SUCCESS, True)
        notifier._check()
        self.assertEqual(notifier.say.call_args_list, [
            call('Vincent has broken Some job'),
            call('Vincent has fixed Some job')
        ])

    def test_substitute_author_name(self):
        notifier = sound.CISoundNotifier(None)

        # If no substitution is defined, nothing happens
        self.assertEqual(
            notifier.substitute_author_name('v.pretre'),
            'v.pretre'
        )

        sound.config.AUTHOR_NAMES_SUBSTITUTIONS['v.pretre'] = 'Vincent'
        self.assertEqual(
            notifier.substitute_author_name('v.pretre'),
            'Vincent'
        )

        # partial substitutions do not work yet
        self.assertEqual(
            notifier.substitute_author_name('v.pretre@example.com'),
            'v.pretre@example.com'
        )
        sound.config.AUTHOR_NAMES_SUBSTITUTIONS = {}

    def test_say_broke(self):
        notifier = sound.CISoundNotifier(Job(1, 'Some job'))
        notifier.say = Mock()

        notifier.say_broke('Vincent')
        notifier.say.assert_called_with('Vincent has broken Some job')

        # Message can be overriden in config
        sound.config.CI_BROKE_SENTENCE = '%(job)s broke by %(author)s, damn'
        notifier.say_broke('someone')
        notifier.say.assert_called_with('Some job broke by someone, damn')

        # Username can also be substituted if needed
        notifier.substitute_author_name = Mock(return_value='King Arthur')
        notifier.say_broke('someone')
        notifier.say.assert_called_with('Some job broke by King Arthur, damn')
        notifier.substitute_author_name.assert_called_with('someone')

    def test_say_fixed(self):
        notifier = sound.CISoundNotifier(Job(1, 'Some job'))
        notifier.say = Mock()

        notifier.say_fixed('Vincent')
        notifier.say.assert_called_with('Vincent has fixed Some job')

        # Message can be overriden in config
        sound.config.CI_FIXED_SENTENCE = '%(job)s fixed by %(author)s, hurray'
        notifier.say_fixed('someone')
        notifier.say.assert_called_with('Some job fixed by someone, hurray')

        # Username can also be substituted if needed
        notifier.substitute_author_name = Mock(return_value='King Arthur')
        notifier.say_fixed('someone')
        notifier.say.assert_called_with(
            'Some job fixed by King Arthur, hurray')
        notifier.substitute_author_name.assert_called_with('someone')

    def test_say(self):
        os.system = Mock()
        notifier = sound.CISoundNotifier(None)

        sound.config.SPEAK_OPTS = '-v english'
        notifier.say('Hi, how do you do ?')

        os.system.assert_called_with('espeak -v english "Hi, how do you do ?"')
