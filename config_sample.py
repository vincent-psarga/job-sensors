import jobs

# Time to wait after all jobs are checked. In seconds
SLEEP_TIME = 3

# The list of monitored jobs
JOBS = [
#  A Jenkins job, no authentication
#  jobs.ci.Jenkins(1, 'My first project', 'first-project', 'http://myjenkins.example.com'),
#  A Jenkins job, with authentication
#  jobs.ci.Jenkins(2, 'My secret project', 'secret-project', 'https://myjenkins.example.com', {'username': 'john', 'password': 'doe'}),
#  A public Travis-CI job (private ones not handled yet)
#  jobs.ci.TravisCi(3, 'Job sensors', 'vincent-psarga/job-sensors')
#  A website: monitors the time to answer (note: does not take into account CSS, assets etc, simply get the HTML page)
#  jobs.response.Response(4, 'My website', 'http://www.example.com')
]
