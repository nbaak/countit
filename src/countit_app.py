#!/usr/bin/env python3
from flask import Flask, jsonify, request
import logging
from countit.metrics import Metrics, Metric
from countit.countit_status_codes import StatusCodes
import random
from countit.token import read_token

app = Flask(__name__)
metrics = Metrics()
try:
    metrics.load()
except:
    pass

app.config["SECRET"] = read_token("auth.token")
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


@app.route("/countit_metrics", methods=["GET"])
def get_metrics() -> str:
    """
    Endpoint to get the current value of the counter.
    """
    headers = request.headers
    auth_header = headers.get('Authorization')

    return jsonify({"success": metrics.show_metrics()}), 200


@app.route("/new/<metric_name>", methods=["POST"])
def add_metric(metric_name:str):
    """
    Add new Metric if not already existing
    """
    metric: Metric = None
    status_code: int = None
    
    try:
        data = request.json
    except:
        data = {}
        
    headers = request.headers
    auth_header = headers.get('Authorization')
        
    password = data.get("password", "")
    metric, status_code = metrics.add_metric(metric_name, password=password)
    
    if status_code == StatusCodes.NEW:
        return jsonify({"success": f"{metric_name} was created"}), 201
    elif status_code == StatusCodes.EXISTING:
        return jsonify({"success": f"{metric_name} already exists"}), 201
    elif status_code == StatusCodes.ERROR:
        return jsonify({"error": f"something went wrong with {metric_name}"}), 400
    
    return jsonify({"error": f"{metric_name} could not be added"}), 400


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
        
    headers = request.headers
    auth_header = headers.get('Authorization')
        
    label = data.get("label", "__default_label__")
    value = data.get("value", 1)
    password = data.get("password", "")  # metric password
    
    metric:Metric = metrics.get_metric(metric_name)
    if not metric:
        return jsonify({"error": "Metric not found"}), 404
    
    if not validate(metric.config["password"], password) \
        or not validate(app.config["SECRET"], auth_header):
        return jsonify({"error": "Access Denied"}), 403
    
    # because lists are not hashable
    if type(label) == list:
        label = tuple(label)
    
    if not label:
        return jsonify({"error": "Missing label"}), 404
    
    if metric:
        metric.update(label, value)        
        return jsonify({"success": metric.get(label)}), 202

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
    
    password = data.get("password", "")
    
    metric:Metric = metrics.get_metric(metric_name)
    if not metric:
        return jsonify({"error": "Metric not found"}), 404
    
    if not validate(metric.config["password"], password) \
        or not validate(app.config["SECRET"], auth_header):
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
    
    password = data.get("password", "")
        
    label = data.get("label", "__default_label__")    
    metric:Metric = metrics.get_metric(metric_name)
    if not metric:
        return jsonify({"error": "Metric not found"}), 404
    
    if not validate(metric.config["password"], password) \
        or not validate(app.config["SECRET"], auth_header):
        return jsonify({"error": "Access Denied"}), 403
    
    if metric and label:
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
        
    password = data.get("password", "")
    
    metric:Metric = metrics.get_metric(metric_name)
    if not metric:
        return jsonify({"error": "Metric not found"}), 404
    
    if not validate(metric.config["password"], password) \
        or not validate(app.config["SECRET"], auth_header):
        return jsonify({"error": "Access Denied"}), 403
    
    if not validate(metric.config["password"], password):
        return jsonify({"error": "Access Denied"}), 403
    
    if metrics.remove_metric(metric_name):
        return jsonify({"success": f"removed {metric_name}"}), 201
            
    return jsonify({"error": "ERROR"}), 404       

        
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
