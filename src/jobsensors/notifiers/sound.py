import os

import jobs
import config
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
            self.play('sounds/site-down.mp3')

        if previous_error and not current_error:
            self.play('sounds/site-back.mp3')

    def play(self, sound):
        os.system("mpg123 %s" % sound)


class CISoundNotifier(Notifier):
    def _check(self):
        current = self.job.status
        previous = self.job.previous_status

        if current.value == str(jobs.ci.STATUS_FAILURE):
            if previous and previous.value == str(jobs.ci.STATUS_SUCCESS):
                self.say_broke(current.author)

        if current.value == str(jobs.ci.STATUS_SUCCESS):
            if previous and previous.value == str(jobs.ci.STATUS_FAILURE):
                self.say_fixed(current.author)

    def substitute_author_name(self, name):
        return config.AUTHOR_NAMES_SUBSTITUTIONS.get(name, name)

    def say_broke(self, author):
        self.say(config.CI_BROKE_SENTENCE % {
            'author': self.substitute_author_name(author),
            'job': self.job.name
        })

    def say_fixed(self, author):
        self.say(config.CI_FIXED_SENTENCE % {
            'author': self.substitute_author_name(author),
            'job': self.job.name
        })

    def say(self, text):
        os.system('espeak %s "%s"' % (config.SPEAK_OPTS, text))
