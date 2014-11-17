import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="jobsensors",
    version="0.0.1",
    author="V. Pretre",
    author_email="",
    description=(""),
    license="GPL",
    keywords="",
    url="",
    packages=[],
    install_requires=[
        'peewee',
        'python-jenkins',
        'travispy'
    ],
    entry_points={
        'console_scripts': [
            'setup_db = db.utils:setup_db',
            'check_jobs = scripts:check_jobs',
            'current_statuses = scripts:current_statuses',
            'sound_notifications = scripts:sound_notifications'
        ]
    },
    long_description="",
    classifiers=[],
)
