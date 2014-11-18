import os
import jobs
from notifiers.notifier import Notifier


def get_notifiers(all_jobs):
    notifiers = []
    for job in all_jobs:
        if isinstance(job, jobs.response.Response):
            notifiers.append(ResponseSoundNotifier(job))

    return notifiers


class ResponseSoundNotifier(Notifier):
    def _check(self):
        current = self.job.status
        current_error = current and current.error
        previous = self.job.previous_status
        previous_error = previous and previous.error

        if current_error and not previous_error:
            self.last_notified_id = current.id
            self.play('sounds/site-down.mp3')

        if previous_error and not current_error:
            self.last_notified_id = current.id
            self.play('sounds/site-back.mp3')

    def play(self, sound):
        os.system("mpg123 %s" % sound)
