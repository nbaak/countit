#!/usr/bin/env python3
from flask import Flask, jsonify, request
import logging
from countit.metrics import Metrics, Metric
from countit.countit_status_codes import StatusCodes
from countit.transport_list import dict_as_transport_list
import random
from countit.token import read_token

app = Flask(__name__)
metrics = Metrics()
try:
    metrics.load()
except:
    pass

app.config["SECRET"] = read_token("auth.token").strip()
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def validate(secret:str, passphrase:str) -> bool:
    if not secret: return True
    if not passphrase: return False
    return secret == passphrase


# Define routes
@app.route("/", methods=["GET"])
def home():
    phrase = random.choice(["Because It counts!", "You can Count on It!", "Never stop counting!"])
    return f"Count It! - {phrase}"


@app.route("/test", methods=["GET"])
def connection_test():
    headers = request.headers
    auth_header = headers.get('Authorization')
    if not validate(app.config["SECRET"], auth_header):
        return jsonify({"error": "Access Denied"}), 403

    return jsonify({"success": metrics.show_metrics()}), 200


@app.route("/metrics", methods=["GET"])
def get_metrics() -> str:
    """
    Endpoint to get the current value of the counter.
    """
    headers = request.headers
    auth_header = headers.get('Authorization')
    if not validate(app.config["SECRET"], auth_header):
        return jsonify({"error": "Access Denied"}), 403
    
    return jsonify({"success": metrics.show_metrics()}), 200


@app.route("/new/<metric_name>", methods=["POST"])
def add_metric(metric_name:str):
    """
    Add new Metric if not already existing
    """
    metric:Metric = None
    status_code:int = None
    
    try:
        data = request.json
    except:
        data = {}
        
    headers = request.headers
    auth_header = headers.get('Authorization')
    if not validate(app.config["SECRET"], auth_header):
        return jsonify({"error": "Access Denied"}), 403
    
    overwrite = data.get("overwrite", False)
  
    metric, status_code = metrics.add_metric(metric_name, overwrite)
    
    if status_code == StatusCodes.NEW:
        return jsonify({"success": f"{metric_name} created"}), 201
    elif status_code == StatusCodes.EXISTING:
        return jsonify({"success": f"{metric_name} exists"}), 201
    elif status_code == StatusCodes.OVERWRITTEN:
        return jsonify({"success": f"{metric_name} overwritten"}), 201
    elif status_code == StatusCodes.ERROR:
        return jsonify({"error": f"{metric_name} error"}), 400
    
    return jsonify({"error": f"{metric_name} error"}), 400


@app.route("/inc/<metric_name>", methods=["POST"])
@app.route("/update/<metric_name>", methods=["POST"])
def update_metric(metric_name:str):
    """
    Update the specified metric.
    """
    try:
        data = request.json
    except:
        data = {}
        
    logging.info("UPDATE METRIC")
    headers = request.headers
    auth_header = headers.get('Authorization')
        
    label = data.get("label", "__default_label__")
    value = data.get("value", 1)
    metric:Metric = metrics.get_metric(metric_name)
    if not metric:
        return jsonify({"error": "Metric not found"}), 404
    
    if not validate(app.config["SECRET"], auth_header):
        return jsonify({"error": "Access Denied"}), 403

    # because lists are not hashable
    if isinstance(label, list):
        label = tuple(label)
    
    if not label:
        return jsonify({"error": "Missing label"}), 404
    
    if metric:
        new_value = metric.update(label, value)
        return jsonify({"success": new_value}), 202

    return jsonify({"error": "ERROR"}), 404


@app.route("/labels/<metric_name>", methods=["GET"])
def get_labels(metric_name:str):
    """
    Get Labels
    returns the labels of a metric
    """
    try:
        data = request.json
    except:
        data = {}
        
    headers = request.headers
    auth_header = headers.get('Authorization')
    
    metric:Metric = metrics.get_metric(metric_name)
    if not metric:
        return jsonify({"error": "Metric not found"}), 404
    
    if not validate(app.config["SECRET"], auth_header):
        return jsonify({"error": "Access Denied"}), 403
    
    if metric:
        labels = metric.labels()
        return jsonify({"success": labels}), 201
    
    return jsonify({"error": "ERROR"}), 404


@app.route("/get/<metric_name>", methods=["POST"])
def get_metric_label_value(metric_name:str):
    try:
        data = request.json
    except:
        data = {}
        
    headers = request.headers
    auth_header = headers.get('Authorization')
       
    label = data.get("label", "__default_label__")    
    metric:Metric = metrics.get_metric(metric_name)
    if not metric:
        return jsonify({"error": "Metric not found"}), 404
    
    if not validate(app.config["SECRET"], auth_header):
        return jsonify({"error": "Access Denied"}), 403
    
    # because lists are not hashable
    if isinstance(label, list):
        label = tuple(label)
        
    if metric and label:
        metric.load()
        value = metric.get(label)
        if value != None: return jsonify({"success": value}), 201
        else: return jsonify({"error": "Label not found"}), 404
            
    return jsonify({"error": "ERROR"}), 404   


@app.route("/delete/<metric_name>", methods=["POST"])
def delete_metric(metric_name:str):
    try:
        data = request.json
    except:
        data = {}
        
    headers = request.headers
    auth_header = headers.get('Authorization')
    
    metric:Metric = metrics.get_metric(metric_name)
    if not metric:
        return jsonify({"error": "Metric not found"}), 404
    
    if not validate(app.config["SECRET"], auth_header):
        return jsonify({"error": "Access Denied"}), 403
     
    if metrics.remove_metric(metric_name):
        return jsonify({"success": f"{metric_name} removed"}), 201
            
    return jsonify({"error": "ERROR"}), 404


@app.route("/sum/<metric_name>", methods=["GET"])
def sum_labels(metric_name:str) -> str:
    """
    Sum all values in metric
    """
    except_default = request.args.get("except_default")  # true/false as str

    headers = request.headers
    auth_header = headers.get('Authorization')
    if not validate(app.config["SECRET"], auth_header):
        return jsonify({"error": "Access Denied"}), 403
    
    metric:Metric = metrics.get_metric(metric_name)
    if not metric:
        return jsonify({"error": "Metric not found"}), 404
    
    if except_default == "true":
        default_label = metric.config["default_label"]
        sum_value = sum([v for k, v in metric.data.items() if not k == default_label])
    else:
        sum_value = sum([v for v in metric.data.values()])
    
    return jsonify({"success": sum_value}), 201


@app.route("/data/<metric_name>", methods=["GET"])
def get_metric_data(metric_name:str):
    """
    Get Labels
    returns the labels of a metric
    """        
    headers = request.headers
    auth_header = headers.get('Authorization')
    
    metric:Metric = metrics.get_metric(metric_name)
    if not metric:
        return jsonify({"error": "Metric not found"}), 404
    
    if not validate(app.config["SECRET"], auth_header):
        return jsonify({"error": "Access Denied"}), 403
    
    if metric:
        data = dict_as_transport_list(metric.data)
        return jsonify({"success": data}), 201
    
    return jsonify({"error": "ERROR"}), 404

        
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=False)
