from checkout_and_payment import *
import pytest

def test_int_input():
    try:
        load_products_from_csv(1)
        assert True is True
    except Exception as e:
        assert True is False

def test_float_input():
    try:
        load_products_from_csv(0.5)
        assert True is True
    except Exception as e:
        assert True is False

def test_list_input():
    try:
        load_products_from_csv([1])
        assert True is True
    except Exception as e:
        assert True is False
