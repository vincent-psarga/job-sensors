import jenkins
from travispy.travispy import TravisPy

from jobs.job import Job

class Jenkins(Job):
    def __init__(self, id, name, job_name, url, auth = None):
        super(Jenkins, self).__init__(id, name)

        self.job_name = job_name
        if auth is None:
            self.jenkins = jenkins.Jenkins(url)
        else:
            self.jenkins = jenkins.Jenkins(url, auth['username'], auth['password'])

    def check(self):
        job = self.jenkins.get_job_info(self.job_name)
        build = self.jenkins.get_build_info(self.job_name, job['lastBuild']['number'])

        return {
            'author': build['culprits'] and build['culprits'][-1]['fullName'] or '',
            'value': build['result'].lower(),
            'stable': not build['building']
        }

class TravisCI(Job):
    def __init__(self, id, name, repo_slug):
        super(TravisCI, self).__init__(id, name)
        self.repo_slug = repo_slug
        self.travis = TravisPy()

    def check(self):
        builds = self.travis.builds(slug = self.repo_slug)
        build = builds[0]

        return {
            'author': builds[0].commit.author_name,
            'value': builds[0].passed and 'success' or 'failure',
            'stable': builds[0].running
        }
