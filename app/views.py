from app import app
from flask import Flask, jsonify, Response, render_template, request, abort
import decotengu

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/deco', methods=['GET', 'POST'])
def deco():
    try :
        profile = create_profile(request.get_json(force=True))
    except:
        abort(400)

    stops = []
    abs_p = []

    print(profile[0].deco_table.total)
    for step in profile[1]:
        # Just stupidly exhaust iterator
        pass

    for stop in profile[0].deco_table:
        print(stop)
        stops.append({'depth': stop.depth, 'time': stop.time})

    return jsonify(stops)
    #return Response(json.dumps(engine.deco_table), mimetype='application/json')

@app.route('/phases', methods=['GET', 'POST'])
def phases_air():

    profile = create_profile(request.get_json(force=True))

    steps = []
    for step in profile[1]:
        steps.append({'phase': step.phase, 'abs_p': step.abs_p, 'time': step.time, 'gas': step.gas, 'data': step.data})

    return jsonify(steps)

@app.route('/chart', methods=['GET', 'POST'])
def chart():
    print(request.get_json(force=True))
    profile = create_profile(request.get_json())

    time = []
    data = [[] for y in range(6)]

    data[0].append("x")
    data[1].append("absolute_pressure")
    data[2].append("gradient_factor")
    data[3].append("gf_ceiling_limit")
    data[4].append("absolute_ceiling_limit")
    data[5].append("leading_inert_gas_pressure")

    for step in profile[1]:
        data[0].append(round(step.time))
        data[1].append(round(step.abs_p, 2))
        data[2].append(round(step.data.gf, 2))

        gf_ceiling_limit = profile[0].model.ceiling_limit(step.data, step.data.gf)
        data[3].append(round(gf_ceiling_limit, 2))

        absolute_ceiling_limit = profile[0].model.ceiling_limit(step.data, 1.0)
        data[4].append(round(absolute_ceiling_limit, 2))

        leading_tissue_n2 = max(step.data.tissues, key=lambda x: x[0])[0] # Nitrogen
        leading_tissue_he = max(step.data.tissues, key=lambda x: x[0])[1] # Helium
        data[5].append(round(leading_tissue_he + leading_tissue_n2, 2))

    return jsonify(x = "x", columns = data)

def create_profile(plan):

    print(plan)

    engine = decotengu.create()
    deco_model = plan["deco_model"]
    if "ZH_L16B_GF" == deco_model["algorithm"]:
        engine.model = decotengu.ZH_L16B_GF()
    elif "ZH-L16C-GF" == deco_model["algorithm"]:
        engine.model = decotengu.ZH_L16C_GF()
    else:
        engine.model = decotengu.ZH_L16C_GF()

    # depth – Switch depth of gas mix.
    # o2 – O2 percentage, i.e. 80.
    # he – Helium percentage, i.e. 18.
    # travel – Travel gas mix if true.
    gas_list = plan["gas_list"]
    for gas in gas_list:
        engine.add_gas(gas["depth"], gas["oxygen"], gas["helium"], gas["travel_gas"])

    # Always at 6 meters... So silly to hover in 3 meters :D
    engine.last_stop_6m = True

    # Depth and time
    depth = plan["dive_plan"]["maximum_depth"]
    time = plan["dive_plan"]["bottom_time"]
    profile = engine.calculate(depth, time)

    print(profile)

    return (engine, profile)
