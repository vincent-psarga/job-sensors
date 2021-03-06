import jenkins
from travispy.travispy import TravisPy

from jobs.job import Job

STATUS_PENDING = 'pending'
STATUS_SUCCESS = 'success'
STATUS_FAILURE = 'failure'


class CI(Job):
    def current_build(self):
        raise NotImplementedError()

    def build_author(self, build):
        raise NotImplementedError()

    def build_status(self, build):
        raise NotImplementedError()

    def build_stable(self, build):
        raise NotImplementedError()

    def check(self):
        build = self.current_build()
        return {
            'author': self.build_author(build),
            'value': self.build_status(build),
            'stable': self.build_stable(build)
        }


class Jenkins(CI):
    def __init__(self, id, name, job_name, url, auth=None):
        super(Jenkins, self).__init__(id, name)

        self.job_name = job_name
        self.jenkins = self.get_jenkins(url, auth)

    def get_jenkins(self, url, auth):
        params = [url]
        if auth is not None:
            params.append(auth['username'])
            params.append(auth['password'])

        return jenkins.Jenkins(*params)

    def current_build(self):
        job = self.jenkins.get_job_info(self.job_name)
        return self.jenkins.get_build_info(
            self.job_name,
            job['lastBuild']['number']
        )

    def build_author(self, build):
        if build.get('culprits'):
            return build['culprits'][-1]['fullName']

        return ''

    def build_status(self, build):
        if build.get('result') == 'SUCCESS':
            return STATUS_SUCCESS

        return STATUS_FAILURE

    def build_stable(self, build):
        return not build.get('building')


class TravisCI(CI):
    def __init__(self, id, name, repo_slug):
        super(TravisCI, self).__init__(id, name)
        self.repo_slug = repo_slug
        self.travis = TravisPy()

    def current_build(self):
        builds = self.travis.builds(slug=self.repo_slug)
        return builds[0]

    def build_author(self, build):
        return build.commit.author_name

    def build_status(self, build):
        if build.pending:
            return STATUS_PENDING

        if build.passed:
            return STATUS_SUCCESS

        return STATUS_FAILURE

    def build_stable(self, build):
        return not build.running
