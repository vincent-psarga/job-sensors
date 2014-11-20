import time
import config

import jobs
import notifiers
from web_frontend import app

def check_jobs():
    while True:
        for job in config.JOBS:
            job.update_status()
        time.sleep(config.SLEEP_TIME)


def current_statuses():
    for job in config.JOBS:
        current = job.status
        previous = job.previous_status

        print job.name
        print '-' * len(job.name)
        print ''
        if current is None:
            print 'No status ...'
        else:
            color = current.color
            print 'Latest status:'
            print ' - author: %s' % current.author
            print ' - value: %s' % current.value
            print ' - color: %s [%s - %s]' % (
                color.color,
                color.blink and 'v' or ' ',
                color.pulse and 'v' or ' '
            )
            print ' - stable: %s' % current.stable
            print ' - date: %s' % current.date
        print ''


def sound_notifications():
    sound_notifiers = notifiers.sound.get_notifiers(config.JOBS)

    while True:
        for notifier in sound_notifiers:
            notifier.check()


def color_notifications():
    color_notifiers = notifiers.colors.get_notifiers(config.JOBS)

    while True:
        for notifier in color_notifiers:
            notifier.check()

def web_frontend():
    app.run()