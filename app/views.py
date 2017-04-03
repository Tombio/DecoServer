from app import app
from flask import Flask, jsonify, Response, render_template, request
import decotengu

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')
    #return Response('Usage: /deco/air/[Depth]/[Time]')

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


@app.route('/deco/trimix/<int:oxygen>/<int:helium>/<int:depth>/<int:time>', methods=['GET', 'POST'])
def deco(oxygen, helium, depth, time):
    last_stop_6m = True

    engine = decotengu.create()
    engine.add_gas(0, oxygen, helium)
    engine.last_stop_6m = last_stop_6m

    profile = engine.calculate(depth, time)

    stops = []
    abs_p = []

    print(engine.deco_table.total)
    for step in profile:
        # Just stupidly exhaust iterator
        pass

    for stop in engine.deco_table:
        print(stop)
        stops.append({'depth': stop.depth, 'time': stop.time})

    return jsonify(stops)
    #return Response(json.dumps(engine.deco_table), mimetype='application/json')

@app.route('/deco/ean/<int:oxygen>/<int:depth>/<int:time>', methods=['GET', 'POST'])
def deco_ean(oxygen, depth, time):
    return deco(oxygen, 0, depth, time)

@app.route('/deco/air/<int:depth>/<int:time>', methods=['GET', 'POST'])
def deco_air(depth, time):
    return deco_ean(21, depth, time)


@app.route('/phases/air/<int:depth>/<int:time>')
def phases_air(depth, time):
    engine = decotengu.create()
    engine.add_gas(0, 21)
    engine.last_stop_6m = True

    profile = engine.calculate(depth, time)

    time = []
    data = [[] for y in range(3)]
    for step in profile:
        print(max(step.data.tissues, key = lambda x: x[0])[0])
        time.append(step.time)
        data[0].append(step.abs_p)

        leading_tissue = max(step.data.tissues, key=lambda x: x[0])[0]
        data[1].append(step.data.gf * leading_tissue)
        data[2].append(1.0 * leading_tissue)
        # steps.append({'phase': step.phase, 'abs_p': step.abs_p, 'time': step.time, 'gas': step.gas, 'data': step.data})

    return jsonify(labels = time, series = data)
