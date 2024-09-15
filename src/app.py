#!/usr/bin/env python3
from flask import Flask, jsonify, request
from metrics import Counter, Dictionary

app = Flask(__name__)
known_metrics = {}


# Define routes
@app.route('/')
def home():
    return "Hello, World!"


@app.route('/metrics', methods=['GET'])
def get_metrics() -> str:
    """
    Endpoint to get the current value of the counter.
    """
    # print([(k,v) for k,v in known_metrics.items()])
    return jsonify(list(known_metrics.keys())), 200


@app.route('/new-metric/<metric_name>')
@app.route('/new-metric/<metric_name>/<metric_type>')
def add_metric(metric_name:str, metric_type:str="Counter"):
    """
    Add new Metric if not already existing
    Known Metric types are:
        - Counter
        - Dictionary
    """
    if metric_name in known_metrics:
        return jsonify({'error': 'Metric exists'}), 400

    if metric_type.lower() == "counter":
        known_metrics[metric_name] = Counter(metric_name)
        
    elif metric_type.lower() == "dictionary":
        known_metrics[metric_name] = Dictionary(metric_name)
        
    else:
        return jsonify({'error': 'Invalid type'}), 400

    return jsonify({'message': f'{metric_name} added'}), 201


@app.route('/update-metric/<metric_name>', methods=['POST'])
def update_metric(metric_name:str):
    """
    Update the specified metric.
    For Counter, increments by 'value'.
    For Dictionary, requires 'label' and 'value' to update.
    """
    data = request.json
    value = int(data.get('value', 1))
    label = data.get('label')

    if metric_name in known_metrics:
        metric = known_metrics[metric_name]

        if type(metric) == Dictionary:
            if label:
                metric.update(label, value)
                return jsonify({'message': f'Metric {metric_name} updated with label {label}'}), 200
            return jsonify({'error': 'Label required for Dictionary'}), 400

        elif type(metric) == Counter:
            metric.inc(value)
            return jsonify({'message': f'Metric {metric_name} incremented by {value}'}), 200
        
        else:
            jsonify({'error': 'Metric type not found'}), 404
            

    return jsonify({'error': 'Metric not found'}), 404
    
        
if __name__ == '__main__':
    app.run(debug=True)
