#!/usr/bin/env python3

from countit_client import CountItClient

passed = 0
errors = 0

cic = CountItClient("http://localhost", 5050, token_file="./auth.token")


def test_case(func):

    def wrapper(*args, **kwargs):
        global passed
        global errors
        try:
            func(*args, **kwargs)
            passed += 1
            print(f"'{func.__name__}' passed")
        except Exception as e:
            print(f"'{func.__name__}' failed: {e}")
            errors += 1

    return wrapper


@test_case 
def test_connection():
    response = cic.test_connection()
    expected = True
    assert expected == response


@test_case
def test_add_metric():
    metric_name = "test_counter"    
    response = cic.add_metric(metric_name)
    expected = f'{metric_name} created'
    assert expected == response
    
    response = cic.add_metric(metric_name)
    expected = f'{metric_name} exists'
    assert expected == response

    
@test_case
def test_show_metrics():
    metric_name = "test_counter"    
    response = cic.metrics()
    expected = "test_counter"
    assert expected in response, f"received: {response}"


@test_case
def test_update_counter():
    metric_name = "test_counter"    
    response = cic.update(metric_name)
    expected = 1    
    assert response == expected, f"received: {response}"
    
    response = cic.update(metric_name, label='test_1')
    expected = 1
    assert response == expected, f"received: {response}"
    
    response = cic.inc(metric_name, label='test_1', value=2)
    expected = 3
    assert response == expected, f"received: {response}"

    
@test_case    
def test_inc_with_tuples():
    metric_name = "test_counter"    
    response = cic.inc(metric_name, label=("1.2.3.4", 'DE'), value=5)
    expected = 5
    assert response == expected, f"received: {response}"
    
    response = cic.inc(metric_name, label=('172.18.0.1', 'FASEL'), value=7)
    expected = 7
    assert response == expected, f"received: {response}"

    
@test_case
def test_sum_of_value():
    metric_name = "test_counter"
    response = cic.sum(metric_name)
    expected = 16
    assert response == expected, f"received: {response} expected {expected}"
    
    response = cic.sum(metric_name, no_default=True)
    expected = 15
    assert response == expected, f"received: {response} expected {expected}"

    
@test_case
def test_delete_metric():
    metric_name = "test_counter"
    
    response = cic.delete(metric_name)
    expected = f"{metric_name} removed"
    assert expected == response
        
    response = cic.metrics()
    expected = "test_counter"
    assert expected not in response
    
  
def main():
    test_connection()
    
    test_add_metric()
    test_show_metrics()
    test_update_counter()
    test_inc_with_tuples()
    test_sum_of_value()
    
    test_delete_metric()
    
    print(f"Passed: {passed}")
    print(f"Error(s): {errors}")


if __name__ == '__main__':
    main()

