#!/usr/bin/env python3
from flask import Flask, jsonify, request
from countit.metrics import Metrics, Metric
from countit.countit_status_codes import StatusCodes

app = Flask(__name__)
metrics = Metrics()
try:
    metrics.load()
except:
    pass


# Define routes
@app.route('/')
def home():
    return "Count It! - Because it counts!"


@app.route('/countit_metrics', methods=['GET'])
def get_metrics() -> str:
    """
    Endpoint to get the current value of the counter.
    """    
    return jsonify({'success': metrics.show_metrics()}), 200


@app.route('/new/<metric_name>')
def add_metric(metric_name:str):
    """
    Add new Metric if not already existing
    """
    metric: Metric = None
    status_code: int = None
    metric, status_code = metrics.add_metric(metric_name)
    
    if status_code == StatusCodes.NEW:
        return jsonify({'success': f'{metric_name} was created'}), 201
    elif status_code == StatusCodes.EXISTING:
        return jsonify({'success': f'{metric_name} already exists'}), 201
    elif status_code == StatusCodes.ERROR:
        return jsonify({'error': f'something went wrong with {metric_name}'}), 400
    
    return jsonify({'error': f'{metric_name} could not be added'}), 400


@app.route('/inc/<metric_name>', methods=['POST'])
@app.route('/update/<metric_name>', methods=['POST'])
def update_metric(metric_name:str):
    """
    Update the specified metric.
    """
    try:
        data = request.json
    except:
        data = {}
        
    label = data.get('label', "__default_label__")
    value = data.get('value', 1)
    
    metric:Metric = metrics.get_metric(metric_name)
    
    # because lists are not hashable
    if type(label) == list:
        label = tuple(label)
    
    if not label:
        return jsonify({'error': 'Missing label'}), 404
    
    if metric:
        metric.update(label, value)        
        return jsonify({'success': metric.get(label)}), 202

    return jsonify({'error': 'Metric not found'}), 404


@app.route("/labels/<metric_name>", methods=["GET"])
def get_labels(metric_name:str):
    metric:Metric = metrics.get_metric(metric_name)
    
    if metric:
        labels = metric.labels()
        return jsonify({"success": labels}), 201
    
    return jsonify({'error': 'Metric not found'}), 404


@app.route("/get/<metric_name>", methods=["POST"])
def get_metric_label_value(metric_name:str):
    try:
        data = request.json
    except:
        data = {}
        
    label = data.get('label', "__default_label__")    
    metric:Metric = metrics.get_metric(metric_name)
    
    if metric and label:
        value = metric.get(label)
        if value != None: return jsonify({"success": value}), 201
        else: return jsonify({'error': 'Label not found'}), 404
            
    return jsonify({'error': 'Metric not found'}), 404   


@app.route("/delete/<metric_name>", methods=["POST"])
def delete_metric(metric_name:str):
    try:
        data = request.json
    except:
        data = {}
    
    if metrics.remove_metric(metric_name):
        return jsonify({"success": f'removed {metric_name}'}), 201
            
    return jsonify({'error': 'Metric not found'}), 404       

        
if __name__ == '__main__':
    app.run(debug=True)
