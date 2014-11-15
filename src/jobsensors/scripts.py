import time
import config

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
            print 'Latest status:'
            print ' - author: %s' % current.author
            print ' - value: %s' % current.value
            print ' - stable: %s' % current.stable
            print ' - date: %s' % current.date
        print ''