import unittest
from mock import Mock

import urllib2
from time import sleep

from db.utils import setup_db, drop_db
from jobs import response

class MockResponse(object):
    def __init__(self, code):
      self.code = code

    def getcode(self):
      return self.code

class ResponseTest(unittest.TestCase):

    def setUp(self):
        setup_db()

    def tearDown(self):
        drop_db()

    def test_check(self):
        sut = response.Response(1, 'My site', 'http://whatever')
        sut.open_page = Mock()
        result = sut.check()

        self.assertEqual(result['author'], '')
        self.assertEqual(result['stable'], True)

        # This one is pretty hard to really test now, see test_time_computing below
        self.assertTrue(result['value'] < 0.1)

    def test_open_page(self):
        # As tests are ran on Travis, it should work ... I guess
        page = response.Response(1, 'My site', 'http://travis-ci.org').open_page()
        self.assertIsInstance(page, urllib2.addinfourl)

        sut = response.Response(2, 'My site', 'http://whatever')
        with self.assertRaises(Exception):
            sut.open_page()

        sut = response.Response(3, 'My site', 'http://google.com')
        response.urlopen = Mock(return_value = MockResponse(404))

        # Other responses than 200 are also considered as errors as we
        # usually check the homepage.
        with self.assertRaises(Exception):
            sut.open_page()

    def test_get_time(self):
        def sleep_two():
          sleep(2)
          return 'Slept two seconds'

        sut = response.Response(2, 'My site', 'http://whatever')
        result = sut.get_time(sleep_two)
        self.assertEqual(int(result['time']), 2)
        self.assertEqual(result['result'], 'Slept two seconds')

    def test_time_computing(self):
        sut = response.Response(2, 'My site', 'http://whatever', 1)
        sut.get_time = Mock(return_value = {'time': 3.14})

        self.assertEqual(sut.check()['value'], 3.14)

        sut.count = 10
        self.assertEqual(sut.check()['value'], 3.14)

        def mock_get_time(func):
            if not hasattr(self, 'call_index'):
              self.call_index = 0

            self.call_index += 1
            return {'time': float(self.call_index)}

        sut._get_time = sut.get_time
        sut.get_time = mock_get_time
        # 5.5 is the average of 1, 2, 3 ... 10
        self.assertEqual(sut.check()['value'], 5.5)
        sut.get_time = sut._get_time