from login import *
import pytest
import shutil

# Fixture to create a temporary directory for the test
@pytest.fixture
def temp_dir(tmp_path):
    return tmp_path / "temp_test_dir"

# Fixture to provide the path to the original users.json file
@pytest.fixture
def original_users_json():
    # Adjust the path accordingly based on the actual location of your original users.json file
    original_file_path = "users.json"
    return original_file_path

# Fixture to provide the path to the copied users.json file in the temporary directory
@pytest.fixture
def copied_users_json(temp_dir, original_users_json):
    # Create the temporary directory and copy the original file to it
    temp_dir.mkdir()
    copied_file_path = temp_dir / "copied_users.json"
    shutil.copy(original_users_json, copied_file_path)
    return copied_file_path

# Fixture to mock the input function
@pytest.fixture
def mock_input(mocker):
    return mocker.patch('builtins.input')

# Fixture to mock the open function to use the copied users.json file
@pytest.fixture
def mock_open(copied_users_json, mocker):
    return mocker.patch('builtins.open', mocker.mock_open(read_data=open(copied_users_json).read()))

# Test case for successful login
def test_login_successful(mock_input, mock_open):
    # Set the expected user input
    mock_input.side_effect = ["Ramanathan", "Notaproblem23*"]

    # Call the login function
    result = login()

    # Assert that the login was successful and returned the expected user data
    assert result == {"username": "Ramanathan", "wallet": 100}

# Test case for unsuccessful login for existing user
def test_login_unsuccessful(mock_input, mock_open):
    # Set the expected user input
    mock_input.side_effect = ["Ramanathan", "wrongpassword"]

    # Call the login function with incorrect password
    result = login()

    # Assert that the login was unsuccessful and returned None
    assert result is None
#Login as a new user but dont create a new
#Login as new user and create a new, with a password that is acceptable
#Login as new user and create a new, with a password with less than 8 characters
#Login as new user and create a new, with a password with more than 8 characters
#Login as new user and create a new, with a password with 8 characters
#Login as new user and create a new, with a password with special characters but no uppercase characters
#Login as new user and create a new, with a password with uppercase characters but no special characters
#Login as new user and create a new, with a password with no uppercase characters or special characters
