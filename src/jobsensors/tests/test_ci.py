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


class MockTravisCommit(object):
    def __init__(self):
        self.author_name = ''


class MockTravisBuild(object):
    def __init__(self):
        self.commit = MockTravisCommit()
        self.pending = False
        self.passed = False
        self.running = False


class TravisCITest(unittest.TestCase):
    def setUp(self):
        setup_db()
        self.sut = ci.TravisCI(1, 'Job sensors', 'vincent-psarga/job-sensors')

    def tearDown(self):
        drop_db()

    def test_current_build(self):
        self.sut.travis.builds = Mock(return_value=[3, 1, 4])

        build = self.sut.current_build()

        # If fetches the builds from the slug given at creation
        self.sut.travis.builds.assert_called_with(
            slug='vincent-psarga/job-sensors')
        # and returns the first one
        self.assertEqual(build, 3)

    def test_build_author(self):
        build = MockTravisBuild()
        build.commit.author_name = 'John Doe'

        # It simply returns the authors name for the commit
        # that triggered the build
        self.assertEqual(self.sut.build_author(build), 'John Doe')

    def test_build_status(self):
        build = MockTravisBuild()

        # If build.pending is true, it returns STATUS_PENDING
        build.pending = True
        self.assertEqual(self.sut.build_status(build), ci.STATUS_PENDING)

        # If build.passed is true, it returns STATUS_PASSED
        build.pending = False
        build.passed = True
        self.assertEqual(self.sut.build_status(build), ci.STATUS_SUCCESS)

        # Otherwise, it returns STATUS_FAILURE
        build.passed = False
        self.assertEqual(self.sut.build_status(build), ci.STATUS_FAILURE)

    def test_build_stable(self):
        build = MockTravisBuild()
        build.running = True

        # The build is considered as unstable as long as it is building
        self.assertFalse(self.sut.build_stable(build))

        build.running = False
        self.assertTrue(self.sut.build_stable(build))
