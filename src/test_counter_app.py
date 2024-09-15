#!/usr/bin/env python3

import requests

BASE_URL = 'http://localhost:5000'


def test_home():
    response = requests.get(f'{BASE_URL}/')
    assert response.status_code == 200
    assert response.text == 'Hello, World!'


def test_add_metric():
    response = requests.get(f'{BASE_URL}/new-metric/test_counter')
    assert response.status_code == 201
    assert response.json() == {'message': 'test_counter added'}
    

def test_show_metrics():
    response = requests.get(f'{BASE_URL}/metrics')
    assert 'test_counter' in response.json()


def test_update_counter():
    # Ensure metric exists first
    requests.get(f'{BASE_URL}/new-metric/test_counter')

    # Update the counter
    response = requests.post(f'{BASE_URL}/update-metric/test_counter', json={'value': 5})
    assert response.status_code == 200

    # Validate metric update
    response = requests.get(f'{BASE_URL}/metrics')
    assert response.status_code == 200
    metrics = response.json()
    assert 'test_counter' in metrics
    # You might need to adapt this if there's a way to validate the exact counter value


def test_add_invalid_metric_type():
    response = requests.get(f'{BASE_URL}/new-metric/test_invalid/InvalidType')
    assert response.status_code == 400
    assert response.json() == {'error': 'Invalid type'}


def test_update_metric_not_found():
    response = requests.post(f'{BASE_URL}/update-metric/non_existent_metric', json={'value': 10})
    assert response.status_code == 404
    assert response.json() == {'error': 'Metric not found'}


def main():
    test_home()
    test_add_metric()
    test_show_metrics()
    test_update_counter()
    test_add_invalid_metric_type()
    test_update_metric_not_found()


if __name__ == '__main__':
    main()

