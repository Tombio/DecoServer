from app import app
from flask import Flask, jsonify, Response
import decotengu

@app.route('/')
@app.route('/index')
def index():
    return Response('Usage: /deco/air/[Depth]/[Time]')

# /deco/air/:depth/:time?algorithm&gradient_factor_min&gradient_factor_max
# /deco/ean/:oxygen/:depth/:time
# /deco/trimix/:oxygen/:helium/:depth/:time
# /deco/multigas/:depth/:time?gaslist
# - gaslist [oxygen;helium@depth]

# /phases/air/:depth/:time
# /phases/ean/:oxygen/:depth/:time
# /phases/trimix/:oxygen/:helium/:depth/:time
# /phases/multigas/:depth/:time?gaslist
# - gaslist [oxygen;helium@depth]


@app.route('/deco/trimix/<int:oxygen>/<int:helium>/<int:depth>/<int:time>')
def deco(oxygen, helium, depth, time):
    engine = decotengu.create()
    engine.add_gas(0, oxygen, helium)
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

@app.route('/deco/ean/<int:oxygen>/<int:depth>/<int:time>')
def deco_ean(oxygen, depth, time):
    return deco(oxygen, 0, depth, time)

@app.route('/deco/air/<int:depth>/<int:time>')
def deco_air(depth, time):
    return deco_ean(21, depth, time)


@app.route('/phases/air/<int:depth>/<int:time>')
def phases_air(depth, time):
    engine = decotengu.create()
    engine.add_gas(0, 21)
    engine.last_stop_6m = True

    profile = engine.calculate(depth, time)

    steps = []
    for step in profile:
        steps.append({'phase': step.phase, 'abs_p': step.abs_p, 'time': step.time, 'gas': step.gas, 'data': step.data})

    return jsonify(steps)
