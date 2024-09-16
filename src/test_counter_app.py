#!/usr/bin/env python3

import requests
import inspect
from functools import wraps

BASE_URL = 'http://localhost:5000'
passed = 0
errors = 0


def try_except_decorator(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        global passed
        global errors
        try:
            func(*args, **kwargs)
            passed += 1
        except Exception as e:
            print(f"An error occurred in {func.__name__}: {e}")
            errors += 1

    return wrapper


@try_except_decorator
def test_home():

    response = requests.get(f'{BASE_URL}/')
    assert response.status_code == 200
    assert response.text == "Count It! - Because it counts!"


@try_except_decorator
def test_add_metric():

    response = requests.get(f'{BASE_URL}/new/test_counter')
    assert response.status_code == 201
    assert response.json() == {'message': 'test_counter added'}

    
@try_except_decorator
def test_show_metrics():

    response = requests.get(f'{BASE_URL}/countit_metrics')
    assert 'test_counter' in response.json()


@try_except_decorator
def test_update_counter():

    # Ensure metric exists first
    requests.get(f'{BASE_URL}/new/test_counter')

    # Update the counter - no label
    response = requests.post(f'{BASE_URL}/update/test_counter', json={'value': 5})
    assert response.status_code == 404, f"received: {response.status_code}"
    
    # Update the counter - no label
    response = requests.post(f'{BASE_URL}/update/test_counter', json={'label': 'test', 'value': 5})
    assert response.status_code == 200, f"received: {response.status_code}"    
    
    # Validate metric update
    response = requests.get(f'{BASE_URL}/countit_metrics')
    assert response.status_code == 200
    metrics = response.json()
    assert 'test_counter' in metrics
    # You might need to adapt this if there's a way to validate the exact counter value


@try_except_decorator
def test_update_metric_not_found():
    response = requests.post(f'{BASE_URL}/update/non_existent_metric', json={'label':'test_123', 'value': 10})
    assert response.status_code == 404
    assert response.json() == {'error': 'Metric not found'}


def main():
    test_home()
    test_add_metric()
    test_show_metrics()
    test_update_counter()
    # test_add_invalid_metric_type()
    test_update_metric_not_found()
    
    print(f"Passed: {passed}")
    print(f"Error(s): {errors}")


if __name__ == '__main__':
    main()

