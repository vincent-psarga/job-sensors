from time import time
from urllib2 import urlopen


from jobs.job import Job

class Response(Job):
    def __init__(self, id, name, url, count = 10):
        super(Response, self).__init__(id, name)
        self.url = url
        self.count = count

    def check(self):
        responses = []
        status = {
            'author': '',
            'value': '',
            'stable': True
        }

        for i in range(0, self.count + 1):
            now = time()

            try:
                index = urlopen(self.url)
            except:
                status['value'] = 'failure'
                return status

            if index.getcode() != 200:
                status['value'] = 'failure'
                return status

            responses.append(time() - now)

        status['value'] = sum(responses) / self.count
        return status
