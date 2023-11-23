import pytest
from unittest.mock import patch
import tempfile
from io import StringIO
from products import searchAndBuyProduct
import shutil


# Fixture to create a temporary directory for the test
@pytest.fixture
def temp_dir(tmp_path):
    return tmp_path / "temp_test_dir"

# Fixture to provide the path to the original users.json file
@pytest.fixture
def original_products_csv():
    # Adjust the path accordingly based on the actual location of your original users.json file
    original_file_path = "products.csv"
    return original_file_path

# Fixture to provide the path to the copied users.json file in the temporary directory
@pytest.fixture
def copied_products_csv(temp_dir, original_products_csv):
    # Create the temporary directory and copy the original file to it
    temp_dir.mkdir()
    copied_file_path = temp_dir / "copied_products.csv"
    shutil.copy(original_products_csv, copied_file_path)
    return copied_file_path

# Fixture to mock the open function to use the copied users.json file
@pytest.fixture
def mock_open(copied_products_csv, mocker):
    return mocker.patch('builtins.open', mocker.mock_open(read_data=open(copied_products_csv).read()))


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

# Test searching for all
def test_all(mock_input, login_stub, checkoutAndPayment_stub, mock_open):
    mock_input.side_effect = ["all", "y"]
    res = searchAndBuyProduct()

# Test searching for value in no rows

# Test searching for value in one row

# Test searching for value in two rows

# Test saying Y right away

# Test saying N then Y

# Test saying something other than y/n

# Test that login() is called

# Test that checkoutAndPayment is called

# Test that test times out if login always fails