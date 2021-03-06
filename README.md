Job-sensors
===========

[![Build Status](https://travis-ci.org/vincent-psarga/job-sensors.svg?branch=master)](https://travis-ci.org/vincent-psarga/job-sensors)


A simple tool to display status of various jobs and alert in case of troubles.

Pre-requisites
--------------

You'll need the following tools installed:

 - python
 - sqlite3
 - espeak
 - mpg123


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

You will have to add ome notifications sounds in the sounds folder, called ``site-down.mp3`` and ``site-back.mp3`` that will be played when a monitored site stops working.
(note: that should be fixed as soon as I find correct open-source sounds for that)

Starting the tool:
------------------

We use supervisor for managing the various process. Start them all using the following command:

    bin/supervisord
