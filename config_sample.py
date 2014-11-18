smport jobs

# Time to wait after all jobs are checked. In seconds
SLEEP_TIME = 30

# The list of monitored jobs
JOBS = [
#  A Jenkins job, no authentication
#  jobs.ci.Jenkins(1, 'My first project', 'first-project', 'http://myjenkins.example.com'),
#  A Jenkins job, with authentication
#  jobs.ci.Jenkins(2, 'My secret project', 'secret-project', 'https://myjenkins.example.com', {'username': 'john', 'password': 'doe'}),
#  A public Travis-CI job (private ones not handled yet)
#  jobs.ci.TravisCI(3, 'Job sensors', 'vincent-psarga/job-sensors')
#  A website: monitors the time to answer (note: does not take into account CSS, assets etc, simply get the HTML page)
#  jobs.response.Response(4, 'My website', 'http://www.example.com')
]

# Options passed to espeak when reading notifications.
SPEAK_OPTS = "-s 125 -a 200"

# Substitution to get speakable names when needed
AUTHOR_NAMES_SUBSTITUTIONS = {
    # 'v.pretre' : 'Vincent',
    # 'Vincent Pretre': 'Vincent'
}

# Sentence said when a build fails
CI_BROKE_SENTENCE = "%(author)s has broken %(job)s"

# Sentence said when a build is fixed
CI_FIXED_SENTENCE = "%(author)s has fixed %(job)s"