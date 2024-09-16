#!/usr/bin/env python3
from flask import Flask, jsonify, request
from metrics import Metrics, Metric

app = Flask(__name__)
metrics = Metrics()


# Define routes
@app.route('/')
def home():
    return "Hello, World!"


@app.route('/metrics', methods=['GET'])
def get_metrics() -> str:
    """
    Endpoint to get the current value of the counter.
    """
    
    return jsonify(metrics.show_metrics()), 200


@app.route('/new/<metric_name>')
@app.route('/new/<metric_name>/<metric_type>')
def add_metric(metric_name:str, metric_type:str="Counter"):
    """
    Add new Metric if not already existing
    """
    
    metric:Metric = metrics.add_metric(metric_name)
    if metric:
        return jsonify({'message': f'{metric_name} added'}), 201
    
    return jsonify({'error': f'{metric_name} could not be added'}), 400


@app.route('/inc/<metric_name>', methods=['POST'])
@app.route('/update/<metric_name>', methods=['POST'])
def update_metric(metric_name:str):
    """
    Update the specified metric.
    """
    data = request.json
    label = data.get('label')
    value = data.get('value', 1)
    metric:Metric = metrics.get_metric(metric_name)
    
    if metric and label:
        metric.update(label, value)        
        return jsonify({'message': f'Metric {metric_name} incremented by {value}'}), 200
    
    if not label:
        return jsonify({'error': 'Missing label'}), 404

    return jsonify({'error': 'Metric not found'}), 404
    
        
if __name__ == '__main__':
    app.run(debug=True)
