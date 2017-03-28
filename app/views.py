from app import app
from flask import Flask, jsonify, Response
import decotengu

@app.route('/')
@app.route('/index')
def index():
    return Response('Usage: /deco-air/[Depth]/[Time]')

@app.route('/deco-ean/<int:ean>/<int:depth>/<int:time>')
def deco_ean(ean, depth, time):
    engine = decotengu.create()
    engine.add_gas(0, ean)
    engine.last_stop_6m = True

    profile = engine.calculate(depth, time)

    stops = []
    print(engine.deco_table.total)
    for step in profile:
        # Just stupidly exhaust iterator
        # of dive profile
        pass

    for stop in engine.deco_table:
        print(stop)
        stops.append({'depth': stop.depth, 'time': stop.time})

    return jsonify(stops)
    #return Response(json.dumps(engine.deco_table), mimetype='application/json')

@app.route('/deco-air/<int:depth>/<int:time>')
def deco_air(depth, time):
    return deco_ean(21, depth, time)


@app.route('/phases-air/<int:depth>/<int:time>')
def phases_air(depth, time):
    engine = decotengu.create()
    engine.add_gas(0, 21)
    engine.last_stop_6m = True

    profile = engine.calculate(depth, time)

    steps = []
    for step in profile:
        steps.append({'phase': step.phase, 'abs_p': step.abs_p, 'time': step.time, 'gas': step.gas, 'data': step.data})

    return jsonify(steps)
