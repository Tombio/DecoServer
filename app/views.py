from app import app
from flask import Flask, jsonify, Response
import decotengu
import json

@app.route('/')
@app.route('/index')
def index():
    engine = decotengu.create()
    engine.add_gas(0, 21)

    profile = engine.calculate(35, 40)

    steps = []
    for step in profile:
        steps.append({'phase': step.phase, 'abs_p': step.abs_p, 'time': step.time, 'gas': step.gas, 'data': step.data})

    return Response(json.dumps(steps), mimetype='application/json')
