from time import time
from urllib2 import urlopen

from jobs.job import Job

class Response(Job):
    def __init__(self, id, name, url, count = 10):
        super(Response, self).__init__(id, name)
        self.url = url
        self.count = count

    def open_page(self):
        try:
            page =  urlopen(self.url)
        except:
            raise Exception('Unable to open page')

        if page.getcode() != 200:
            raise Exception('Got error: %s' % page.getcode())

        return page

    def get_time(self, func):
        now = time()
        value = func()
        return {
            'result': value,
            'time': time() - now
        }

    def check(self):
        responses = []
        status = {
            'author': '',
            'value': '',
            'stable': True
        }

        for i in range(0, self.count):
            responses.append(self.get_time(self.open_page)['time'])

        status['value'] = sum(responses) / len(responses)
        return status
