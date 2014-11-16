import unittest
from mock import Mock

from db.utils import setup_db, drop_db
from db.models import Job as JobDb

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
