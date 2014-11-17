import unittest
from mock import Mock

import jenkins

from db.utils import setup_db, drop_db
from jobs import ci


class CITest(unittest.TestCase):
    def setUp(self):
        setup_db()
        self.sut = ci.CI(1, 'Whatever')

    def tearDown(self):
        drop_db()

    def test_current_build(self):
        with self.assertRaises(NotImplementedError):
            self.sut.current_build()

    def test_build_author(self):
        with self.assertRaises(NotImplementedError):
            self.sut.build_author(None)

    def test_build_status(self):
        with self.assertRaises(NotImplementedError):
            self.sut.build_status(None)

    def test_build_stable(self):
        with self.assertRaises(NotImplementedError):
            self.sut.build_stable(None)

    def test_check(self):
        build = object()

        self.sut.current_build = Mock(return_value=build)
        self.sut.build_author = Mock(return_value='An author')
        self.sut.build_status = Mock(return_value='Any status')
        self.sut.build_stable = Mock(return_value='True or False')

        # It returns the current builds author, status and stability
        self.assertEqual(self.sut.check(), {
            'author': 'An author',
            'value': 'Any status',
            'stable': 'True or False'
        })
        self.sut.build_author.assert_called_with(build)
        self.sut.build_status.assert_called_with(build)
        self.sut.build_stable.assert_called_with(build)


class JenkinsTest(unittest.TestCase):
    def setUp(self):
        setup_db()
        self.sut = ci.Jenkins(1, 'Jenkins', 'My job', 'http://www.example.com')

    def tearDown(self):
        drop_db()

    def test_get_jenkins(self):
        # We test it via the instance initialization.
        jenkins.Jenkins = Mock()

        # An example of public Jenkins
        ci.Jenkins(1, 'Jenkins', 'My job', 'http://www.example.com')
        jenkins.Jenkins.assert_called_with('http://www.example.com')

        # A Jenkins with authentication
        ci.Jenkins(1, 'Jenkins', 'My job', 'http://www.example.com',
                   {'username': 'Cookie', 'password': 'Doe'})
        jenkins.Jenkins.assert_called_with(
            'http://www.example.com', 'Cookie', 'Doe')

    def test_current_build(self):
        self.sut.jenkins.get_job_info = Mock(
            return_value={'lastBuild': {'number': 1234}})
        self.sut.jenkins.get_build_info = Mock(
            return_value='Forty two')

        current_build = self.sut.current_build()

        # It first fetches the job infos on Jenkins
        self.sut.jenkins.get_job_info.assert_called_with('My job')
        # And then get the latest build info
        self.sut.jenkins.get_build_info.assert_called_with('My job', 1234)
        self.assertEqual(current_build, 'Forty two')

    def test_build_author(self):
        build = {'culprits': []}

        # If there is no culprits, it returns an empty string
        # This happens with a manually started build or a build
        # triggered by another one.
        self.assertEqual(self.sut.build_author(build), '')

        build['culprits'] = [
            {'fullName': 'John Doe'},
            {'fullName': 'John Doh!'},
        ]
        # If there are culprits, it returns the fullName property
        # of the last one
        self.assertEqual(self.sut.build_author(build), 'John Doh!')

    def test_build_status(self):
        build = {}

        # By default, it considers the job failed
        self.assertEqual(self.sut.build_status(build), ci.STATUS_FAILURE)

        build['result'] = 'PASSED'
        # Except if result equals 'PASSED'
        self.assertEqual(self.sut.build_status(build), ci.STATUS_FAILURE)

    def test_build_stable(self):
        build = {}
        # Any build is considered as stable
        self.assertTrue(self.sut.build_stable(build))

        # Except if it is specified that it is building
        build['building'] = True
        self.assertFalse(self.sut.build_stable(build))
