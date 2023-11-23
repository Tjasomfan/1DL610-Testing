from checkout_and_payment import Product, ShoppingCart
from logout import logout
import tempfile
import pytest
from pytest_mock import mocker
from unittest.mock import patch

# Fixture to mock the input function
@pytest.fixture
def mock_input(mocker):
    return mocker.patch('builtins.input')

# Test return for cart with 0 items
def test_no_items():
    cart = ShoppingCart()
    result = logout(cart)
    assert (result == True)
    

# Test return for cart with 1 item and input "Y"
def test_return_1_item(mock_input):
    mock_input.side_effect = ["Y"]
    
    cart = ShoppingCart()
    cart.add_item(Product("Car", 500, 2))
    result = logout(cart)
    
    assert (result == True)

# Test return for cart with 1 item and input "N"
def test_return_1_item_2(mock_input):
    mock_input.side_effect = ["N"]
    
    cart = ShoppingCart()
    cart.add_item(Product("Car", 500, 2))
    result = logout(cart)
    
    assert (result == False)

# Test return for cart with 1 item and input "hello"
def test_return_1_item_3(mock_input):
    mock_input.side_effect = ["hello"]
    
    cart = ShoppingCart()
    cart.add_item(Product("Car", 500, 2))
    result = logout(cart)
    
    assert (result == False)

# Test return for cart with 1 item and input "y"
def test_return_1_item_4(mock_input):
    mock_input.side_effect = ["y"]
    
    cart = ShoppingCart()
    cart.add_item(Product("Car", 500, 2))
    result = logout(cart)
    
    assert (result == True)

#Uses the patch block from unittest.mock to capture stdout since the pytest.mock gave us issues
# Test output for cart with 1 item
def test_output_1_item(mock_input):
    mock_input.side_effect = ["Y"]

    cart = ShoppingCart()
    cart.add_item(Product("Apple", 5, 5))
    with patch('sys.stdout', new_callable=tempfile.SpooledTemporaryFile, mode='w+t', create=True) as mock_stdout:
        logout(cart)
        mock_stdout.seek(0)
        captured_output = mock_stdout.read()
    
    expected_output = "Your cart is not empty.You have following items\n['Apple', 5.0, 5]\n"
    assert (captured_output == expected_output)
    
# Test output for cart with 3 items
def test_output_3_items(mock_input):
    mock_input.side_effect = ["Y"]


    cart = ShoppingCart()
    cart.add_item(Product("Apple", 5, 5))
    cart.add_item(Product("Blueberry", 15, 5))
    cart.add_item(Product("Watermelon", 50, 10))
    with patch('sys.stdout', new_callable=tempfile.SpooledTemporaryFile, mode='w+t', create=True) as mock_stdout:
        logout(cart)
        mock_stdout.seek(0)
        captured_output = mock_stdout.read()
    
    expected_output = "Your cart is not empty.You have following items\n['Apple', 5.0, 5]\n['Blueberry', 15.0, 5]\n['Watermelon', 50.0, 10]\n"
    assert (captured_output == expected_output)

# Test output for empty cart
def test_output_zero_items(mock_input):
    mock_input.side_effect = ["Y"]

    cart = ShoppingCart()
    with patch('sys.stdout', new_callable=tempfile.SpooledTemporaryFile, mode='w+t', create=True) as mock_stdout:
        logout(cart)
        mock_stdout.seek(0)
        captured_output = mock_stdout.read()
    
    expected_output = ""
    assert (captured_output == expected_output)

# Test length of content of cart with 1 item and input "Y"
def test_length_after_logout(mock_input):
    mock_input.side_effect = ["Y"]
    cart = ShoppingCart()
    cart.add_item(Product("Banana", 5, 5))
    assert(len(cart.items) == 1)
    result = logout(cart)
    assert (result)
    assert(len(cart.items) == 0)


# Test length of content of cart with 1 item and input "N"
def test_length_without_logout(mock_input):
    mock_input.side_effect = ["N"]
    cart = ShoppingCart()
    cart.add_item(Product("Banana", 5, 5))
    assert(len(cart.items) == 1)
    result = logout(cart)
    assert (not result)
    assert(len(cart.items) == 1)
    