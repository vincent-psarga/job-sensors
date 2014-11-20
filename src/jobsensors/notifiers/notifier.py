def get_notifier(job, mapping):
    for cls in mapping.keys():
        if isinstance(job, cls):
            return mapping[cls](job)


def get_notifiers(jobs, base_mapping={}, custom_mapping={}):
    mapping = {}
    mapping.update(base_mapping)
    mapping.update(custom_mapping)

    return filter(None, [
        get_notifier(job, mapping)
        for job in jobs
    ])


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
