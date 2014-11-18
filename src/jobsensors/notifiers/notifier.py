class Notifier(object):
    def __init__(self, job):
        self.job = job
        self.last_notified_id = None

    def check(self):
        current = self.job.status
        if current is None:
            return

        if self.last_notified_id == current.id:
            return

        self.last_notified_id = current.id
        self._check()

    def _check(self):
        raise NotImplementedError()
