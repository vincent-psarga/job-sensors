Job-sensors
===========

[![Build Status](https://travis-ci.org/vincent-psarga/job-sensors.svg?branch=master)](https://travis-ci.org/vincent-psarga/job-sensors)


A simple tool to display status of various jobs and alert in case of troubles.

Installing
----------

You'll need to have python, sqlite3 and git installed:

    git clone https://github.com/vincent-psarga/job-sensors.git
    cd job-sensors
    python bootstrap.py
    bin/buildout
    bin/setup_db


Configuring
-----------

Copy config_sample.py as config.py and edit it based on the comments.


