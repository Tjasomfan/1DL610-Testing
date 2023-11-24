import pytest
from unittest.mock import patch
from products import searchAndBuyProduct

# Fixture to mock the input function
@pytest.fixture
def mock_input(mocker):
    return mocker.patch('builtins.input')

@pytest.fixture
def login_stub(mocker):
    return mocker.patch('products.login', return_value={"username": "Joe", "wallet": 100})

@pytest.fixture
def checkoutAndPayment_stub(mocker):
    return mocker.patch('products.checkoutAndPayment')

@pytest.fixture
def display_csv_as_table_stub(mocker):
    return mocker.patch('products.display_csv_as_table')

@pytest.fixture
def display_filtered_table_stub(mocker):
    return mocker.patch('products.display_filtered_table')

# Test searching for all
def test_all(mock_input, login_stub, checkoutAndPayment_stub, display_csv_as_table_stub, display_filtered_table_stub):
    mock_input.side_effect = ["all", "y"]
    res = searchAndBuyProduct()

    display_csv_as_table_stub.assert_called_once_with("products.csv")
    assert display_filtered_table_stub.call_count == 0

# Test searching for all
def test_all_upper(mock_input, login_stub, checkoutAndPayment_stub, display_csv_as_table_stub, display_filtered_table_stub):
    mock_input.side_effect = ["ALL", "y"]
    res = searchAndBuyProduct()

    display_csv_as_table_stub.assert_called_once_with("products.csv")
    assert display_filtered_table_stub.call_count == 0

# Test searching for apple
def test_apple(mock_input, login_stub, checkoutAndPayment_stub, display_csv_as_table_stub, display_filtered_table_stub):
    mock_input.side_effect = ["apple", "y"]
    res = searchAndBuyProduct()

    display_filtered_table_stub.assert_called_once_with("products.csv", "apple")
    assert display_csv_as_table_stub.call_count == 0

# Test searching for orange and apple
def test_orange_and_apple(mock_input, login_stub, checkoutAndPayment_stub, display_csv_as_table_stub, display_filtered_table_stub):
    mock_input.side_effect = ["orange", "n", "apple", "y"]
    res = searchAndBuyProduct()

    assert display_filtered_table_stub.call_count == 2
    assert display_csv_as_table_stub.call_count == 0

# Test searching for orange and apple
def test_login_called(mock_input, login_stub, checkoutAndPayment_stub, display_csv_as_table_stub, display_filtered_table_stub):
    mock_input.side_effect = ["orange", "n", "apple", "y"]
    res = searchAndBuyProduct()

    assert login_stub.call_count == 1
    
# Test searching for orange and apple
def test_checkout_called(mock_input, login_stub, checkoutAndPayment_stub, display_csv_as_table_stub, display_filtered_table_stub):
    mock_input.side_effect = ["orange", "n", "apple", "y"]
    res = searchAndBuyProduct()

    assert checkoutAndPayment_stub.call_count == 1

# Test answer hello instead of y/n
def test_hello(mock_input, login_stub, checkoutAndPayment_stub, display_csv_as_table_stub, display_filtered_table_stub):
    mock_input.side_effect = ["orange", "hello", "apple", "y"]
    res = searchAndBuyProduct()

    assert display_filtered_table_stub.call_count == 2

# Test searching for orange and all
def test_orange_and_all(mock_input, login_stub, checkoutAndPayment_stub, display_csv_as_table_stub, display_filtered_table_stub):
    mock_input.side_effect = ["orange", "N", "all", "y"]
    res = searchAndBuyProduct()

    assert display_filtered_table_stub.call_count == 1
    assert display_csv_as_table_stub.call_count == 1