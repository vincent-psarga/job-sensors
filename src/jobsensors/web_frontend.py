from flask import Flask
from flask import jsonify
from flask.ext.assets import Environment, Bundle

import config
app = Flask('Job sensor frontend')


def data():
    data = []
    for job in config.JOBS:
        data.append({
            'id': job.id,
            'name': job.name,
        })

        current = job.status
        if current:
            data[-1]['status'] = {
                'author': current.author,
                'value': current.value,
                'color': {
                    'color': current.color.color,
                    'blink': current.color.blink,
                    'pulse': current.color.pulse
                },
                'stable': current.stable,
                'date': current.date
            }
    return data

@app.route('/')
def index():
    return open('static/index.html', 'r').read()


@app.route('/api')
def api():
    return jsonify(jobs = data())
