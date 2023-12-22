from checkout_and_payment import *
from edit_user import edit_user
from products import display_csv_as_table, display_filtered_table, searchAndBuyProduct
from login import *
import pytest
import tempfile
import shutil
import os
from unittest.mock import patch
from io import StringIO

# Fixture to create a temporary directory for the test
@pytest.fixture
def temp_dir(tmp_path):
    return tmp_path / "temp_test_dir"

@pytest.fixture
def test_user():
    return User("TestUser", 0.0)

@pytest.fixture
def test_cart():
    cart = ShoppingCart()
    return cart

@pytest.fixture
def test_products():
    testproducts = load_products_from_csv("products.csv")
    return testproducts

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

#Function to filter a product by name from the products list
def get_product_by_name(products, target_name):
    for product in products:
        if product.name == target_name:
            return product
    return None  # Return None if the product with the specified name is not found

@pytest.fixture
def valid_csv_file():
    # Create a temporary CSV file for testing
    csv_file = tempfile.NamedTemporaryFile(mode='w', delete=False)

    # Write sample data to the temporary CSV file with correct data types
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Product', 'Price', 'Units'])
    csv_writer.writerow(['Apple', 1, 10]) # Int in the 'Price' column
    csv_writer.writerow(['Banana', 0.75, 8])
    csv_writer.writerow(['Orange', 1.25, 12])

    # Print the content of the CSV file
    csv_file.seek(0)
    print(csv_file)

    # The point where the test function can use the fixture before it is teared down
    yield csv_file.name

    # Clean up: Close and remove the temporary CSV file
    csv_file.close()
    os.remove(csv_file.name)

@pytest.fixture
def copy_csv_file():
    # Set up: Copy the CSV file 
    shutil.copy('products.csv','copy_products.csv') 

    yield

    # Teardown: Remove the copied CSV file 
    os.remove('copy_products.csv')

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

# Fixture to mock the open function to use the copied users.json file
@pytest.fixture
def mock_open(copied_users_json, mocker):
    return mocker.patch('builtins.open', mocker.mock_open(read_data=open(copied_users_json).read()))

    # Smoketest #8
def test_eight_smoke_test(mock_input, test_cart, test_products, capfd, mock_open):
    # Set the expected user input
    mock_input.side_effect = ["Ramanathan", "Notaproblem23*"]

    # Call the login function
    result = login()

    # Captured the print
    captured = capfd.readouterr()

    # Assert that the login was successful and returned the expected user data
    assert result == {"username": "Ramanathan", "wallet": 100}
    user = User(result["username"], 0)

    # Test user wallet
    assert user.wallet == 0

    #Extracts product
    banana = get_product_by_name(test_products, "Banana")

    # Add items
    test_cart.add_item(banana)

    # Ensure that the shopping cart has one banana in it
    assert test_cart.items == [banana]

    #assert that there has been one banana subtracted from stock
    assert banana.units == 15

    # Ensure that the shopping cart has a banana
    assert test_cart.items == [banana]

    # Set the expected user input
    mock_input.side_effect = ["street", "070", "mail@mail.com", "n"]
    
    #Edit user info without any cards
    new_user = edit_user(result)

    assert new_user["address"] == "street"
    assert new_user["phone"] == "070"
    assert new_user["email"] == "mail@mail.com"
    assert new_user["cards"] == []
    
    # Captured the print
    captured = capfd.readouterr()
    
    #Checkout the cart
    checkout(user, test_cart, test_products)

    # Captured the print
    captured = capfd.readouterr()

    #Expected output
    expected_output = "You don't have enough money to complete the purchase.\nPlease try again!"
    
    #Asserts that the expected output matches the correct output
    assert expected_output == captured.out.strip()

    #assert that there has been one banana subtracted from stock
    assert banana.units == 15
    
    # Ensure that the user's wallet has the correct balance
    assert user.wallet == 0

    # Ensure that the shopping cart is not empty
    assert test_cart.items == [banana]

    # Set the expected user input
    mock_input.side_effect = ["y"]

    # Log out user
    result = logout(test_cart)

    # Ensure that the shopping cart is empty
    assert test_cart.items == []

    # Check to see if user is logged out
    assert (result == True)


    # Smoketest #9
def test_nineth_smoke_test(mock_input, test_cart, test_products, capfd, mock_open):
    # Set the expected user input
    mock_input.side_effect = ["Ramanathan", "Notaproblem23*"]

    # Call the login function
    result = login()

    # Captured the print
    captured = capfd.readouterr()

    # Assert that the login was successful and returned the expected user data
    assert result == {"username": "Ramanathan", "wallet": 100}
    user = User(result["username"], 0)

    # Test user wallet
    assert user.wallet == 0

    #Extracts product
    banana = get_product_by_name(test_products, "Banana")

    # Add items
    test_cart.add_item(banana)

    # Ensure that the shopping cart has one banana in it
    assert test_cart.items == [banana]

    #assert that there has been one banana subtracted from stock
    assert banana.units == 15

    # Ensure that the shopping cart has a banana
    assert test_cart.items == [banana]

    # Set the expected user input
    mock_input.side_effect = ["street", "070", "mail@mail.com", "y", "0", "1", "debit", "5000", "n"]
    
    #Edit user info without any cards
    new_user = edit_user(result)

    assert new_user["address"] == "street"
    assert new_user["phone"] == "070"
    assert new_user["email"] == "mail@mail.com"
    card = {"number" : "0", "expirationdate" : "1", "name" : "debit", "ccv" : "5000"}
    assert new_user["cards"] == [card]
    
    # Captured the print
    captured = capfd.readouterr()
    
    #Checkout the cart
    checkout(user, test_cart, test_products)

    # Captured the print
    captured = capfd.readouterr()

    #Expected output
    expected_output = "You don't have enough money to complete the purchase.\nPlease try again!"
    
    #Asserts that the expected output matches the correct output
    assert expected_output == captured.out.strip()

    #assert that there has been one banana subtracted from stock
    assert banana.units == 15
    
    # Ensure that the user's wallet has the correct balance
    assert user.wallet == 0

    # Ensure that the shopping cart is not empty
    assert test_cart.items == [banana]

    # Set the expected user input
    mock_input.side_effect = ["y"]

    # Log out user
    result = logout(test_cart)

    # Ensure that the shopping cart is empty
    assert test_cart.items == []

    # Check to see if user is logged out
    assert (result == True)


    # Smoketest #10
def test_tenth_smoke_test(mock_input, test_cart, test_products, capfd, mock_open):
    # Set the expected user input
    mock_input.side_effect = ["Ramanathan", "Notaproblem23*"]

    # Call the login function
    result = login()

    # Captured the print
    captured = capfd.readouterr()

    # Assert that the login was successful and returned the expected user data
    assert result == {"username": "Ramanathan", "wallet": 100}
    user = User(result["username"], 0)

    # Test user wallet
    assert user.wallet == 0

    #Extracts product
    banana = get_product_by_name(test_products, "Banana")

    # Add items
    test_cart.add_item(banana)

    # Ensure that the shopping cart has one banana in it
    assert test_cart.items == [banana]

    #assert that there has been one banana subtracted from stock
    assert banana.units == 15

    # Ensure that the shopping cart has a banana
    assert test_cart.items == [banana]

    # Set the expected user input
    mock_input.side_effect = ["street", "070", "mail@mail.com", "y", "0", "1", "debit", "5000", "y", "543", "10/27/13", "credit", "123", "n"]
    
    #Edit user info without any cards
    new_user = edit_user(result)

    assert new_user["address"] == "street"
    assert new_user["phone"] == "070"
    assert new_user["email"] == "mail@mail.com"
    card1 = {"number" : "0", "expirationdate" : "1", "name" : "debit", "ccv" : "5000"}
    card2 = {"number" : "543", "expirationdate" : "10/27/13", "name" : "credit", "ccv" : "123"}
    assert new_user["cards"] == [card1, card2]
    
    # Captured the print
    captured = capfd.readouterr()
    
    #Checkout the cart
    checkout(user, test_cart, test_products)

    # Captured the print
    captured = capfd.readouterr()

    #Expected output
    expected_output = "You don't have enough money to complete the purchase.\nPlease try again!"
    
    #Asserts that the expected output matches the correct output
    assert expected_output == captured.out.strip()

    #assert that there has been one banana subtracted from stock
    assert banana.units == 15
    
    # Ensure that the user's wallet has the correct balance
    assert user.wallet == 0

    # Ensure that the shopping cart is not empty
    assert test_cart.items == [banana]

    # Set the expected user input
    mock_input.side_effect = ["y"]

    # Log out user
    result = logout(test_cart)

    # Ensure that the shopping cart is empty
    assert test_cart.items == []

    # Check to see if user is logged out
    assert (result == True)

