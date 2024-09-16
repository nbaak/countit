#!/usr/bin/env python3

import requests
import inspect

BASE_URL = 'http://localhost:5000'


def test_home():
    print(f"running {inspect.stack()[0][3]}")
    response = requests.get(f'{BASE_URL}/')
    assert response.status_code == 200
    assert response.text == 'Hello, World!'


def test_add_metric():
    print(f"running {inspect.stack()[0][3]}")
    response = requests.get(f'{BASE_URL}/new/test_counter')
    assert response.status_code == 201
    assert response.json() == {'message': 'test_counter added'}
    

def test_show_metrics():
    print(f"running {inspect.stack()[0][3]}")
    response = requests.get(f'{BASE_URL}/metrics')
    assert 'test_counter' in response.json()


def test_update_counter():
    print(f"running {inspect.stack()[0][3]}")
    # Ensure metric exists first
    requests.get(f'{BASE_URL}/new/test_counter')

    # Update the counter
    response = requests.post(f'{BASE_URL}/update/test_counter', json={'value': 5})
    assert response.status_code == 200, f"received: {response.status_code}"

    # Validate metric update
    response = requests.get(f'{BASE_URL}/metrics')
    assert response.status_code == 200
    metrics = response.json()
    assert 'test_counter' in metrics
    # You might need to adapt this if there's a way to validate the exact counter value


def test_add_invalid_metric_type():
    print(f"running {inspect.stack()[0][3]}")
    response = requests.get(f'{BASE_URL}/new/test_invalid/InvalidType')
    assert response.status_code == 400
    assert response.json() == {'error': 'Invalid type'}


def test_update_metric_not_found():
    print(f"running {inspect.stack()[0][3]}")
    response = requests.post(f'{BASE_URL}/update/non_existent_metric', json={'value': 10})
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

