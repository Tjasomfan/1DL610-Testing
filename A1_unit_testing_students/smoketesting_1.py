from checkout_and_payment import *
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

# Smoketest #1, remove non-existing item
def test_first_smoke_test(mock_input, test_cart, test_products, capfd):
    # Set the expected user input
    mock_input.side_effect = ["Ramanathan", "Notaproblem23*"]

    # Call the login function
    result = login()

    # Captured the print
    captured = capfd.readouterr()

    # Assert that the login was successful and returned the expected user data
    assert result == {"username": "Ramanathan", "wallet": 100}
    user = User(result["username"], result["wallet"])

    # Test user wallet
    assert user.wallet == 100

    #Extracts product
    banana = get_product_by_name(test_products, "Banana")
    salmon = get_product_by_name(test_products, "Salmon")

    # Add items
    test_cart.add_item(banana)

    # Ensure that the shopping cart has one banana in it
    assert test_cart.items == [banana]

    #assert that there has been one banana subtracted from stock
    assert banana.units == 15

    #Run remove_item function
    remove_item_from_cart(test_cart, salmon, test_products)

    # Captured the print
    captured = capfd.readouterr()
    
    #Expected output
    expected_output = "You don't have this item in your cart."

    #Asserts that the expected output matches the correct output
    assert expected_output == captured.out.strip()

    # Ensure that the shopping cart has a banana
    assert test_cart.items == [banana]

    #Checkout the cart
    checkout(user, test_cart, test_products)

    # Captured the print
    captured = capfd.readouterr()

    #Expected output
    expected_output = f"Thank you for your purchase, {user.name}! Your remaining balance is {user.wallet}"

    #Asserts that the expected output matches the correct output
    assert expected_output == captured.out.strip()

    #assert that there has been one banana subtracted from stock
    assert banana.units == 14
    
    # Ensure that the user's wallet has the correct balance
    assert user.wallet == 99.0

    # Ensure that the shopping cart is empty
    assert test_cart.items == []

    # Log out user
    result = logout(test_cart)

    # Check to see if user is logged out
    assert (result == True)

# Smoketest #2, remove existing item in stock
def test_second_smoke_test(mock_input, test_cart, test_products, capfd):
    # Set the expected user input
    mock_input.side_effect = ["Ramanathan", "Notaproblem23*"]

    # Call the login function
    result = login()

    # Captured the print
    captured = capfd.readouterr()

    # Assert that the login was successful and returned the expected user data
    assert result == {"username": "Ramanathan", "wallet": 100}
    user = User(result["username"], result["wallet"])

    # Test user wallet
    assert user.wallet == 100

    #Extracts product
    banana = get_product_by_name(test_products, "Banana")
    salmon = get_product_by_name(test_products, "Salmon")

    # Adds items to cart
    test_cart.add_item(banana)
    test_cart.add_item(salmon)

    # Ensure that the shopping cart has one banana in it
    assert test_cart.items == [banana, salmon]

    # assert that there has been one banana subtracted from stock
    assert banana.units == 15

    # Run remove_item function
    remove_item_from_cart(test_cart, salmon, test_products)

    # Captured the print
    captured = capfd.readouterr()
    
    #Expected output
    expected_output = "Remaining items in cart: \n['Banana', 1.0, 15]"

    #Asserts that the expected output matches the correct output
    assert expected_output == captured.out.strip()

    # Ensure that the shopping cart has a banana
    assert test_cart.items == [banana]

    #Checkout the cart
    checkout(user, test_cart, test_products)

    # Captured the print
    captured = capfd.readouterr()

    #Expected output
    expected_output = f"Thank you for your purchase, {user.name}! Your remaining balance is {user.wallet}"

    #Asserts that the expected output matches the correct output
    assert expected_output == captured.out.strip()

    #assert that there has been one banana subtracted from stock
    assert banana.units == 14
    
    # Ensure that the user's wallet has the correct balance
    assert user.wallet == 99.0

    # Ensure that the shopping cart is empty
    assert test_cart.items == []

    # Log out user
    result = logout(test_cart)

    # Check to see if user is logged out
    assert (result == True)

# Smoketest #3, remove non-existing item in stock
def test_third_smoke_test(mock_input, test_cart, test_products, capfd):
    # Set the expected user input
    mock_input.side_effect = ["Ramanathan", "Notaproblem23*"]

    # Call the login function
    result = login()

    # Captured the print
    captured = capfd.readouterr()

    # Assert that the login was successful and returned the expected user data
    assert result == {"username": "Ramanathan", "wallet": 100}
    user = User(result["username"], result["wallet"])

    # Test user wallet
    assert user.wallet == 100

    #Extracts product
    banana = get_product_by_name(test_products, "Banana")
    orange = Product("orange", 5.0, 3)

    #Make orange is not in products list
    assert orange not in test_products

    # Adds items to cart
    test_cart.add_item(banana)
    test_cart.add_item(orange)

    # Ensure that the shopping cart has one banana in it
    assert test_cart.items == [banana, orange]

    # Run remove_item function
    remove_item_from_cart(test_cart, orange, test_products)

    #Make orange is in products list
    assert orange in test_products

    # Captured the print
    captured = capfd.readouterr()
    
    #Expected output
    expected_output = "Remaining items in cart: \n['Banana', 1.0, 15]"

    #Asserts that the expected output matches the correct output
    assert expected_output == captured.out.strip()

    # Ensure that the shopping cart has a banana
    assert test_cart.items == [banana]

    #Checkout the cart
    checkout(user, test_cart, test_products)

    # Captured the print
    captured = capfd.readouterr()

    #Expected output
    expected_output = f"Thank you for your purchase, {user.name}! Your remaining balance is {user.wallet}"

    #Asserts that the expected output matches the correct output
    assert expected_output == captured.out.strip()

    #assert that there has been one banana subtracted from stock
    assert banana.units == 14
    
    # Ensure that the user's wallet has the correct balance
    assert user.wallet == 99.0

    # Ensure that the shopping cart is empty
    assert test_cart.items == []

    # Log out user
    result = logout(test_cart)

    # Check to see if user is logged out
    assert (result == True)