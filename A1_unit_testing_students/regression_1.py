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



## New tests

#Test case for item not existing in cart
def test_remove_item_not_in_cart(test_cart, capfd, test_products):

    #Extracts product
    banana = get_product_by_name(test_products, "Banana")
    salmon = get_product_by_name(test_products, "Salmon")

    #Adds single item to cart
    test_cart.add_item(banana)

    # Ensure that the shopping cart has a banana
    assert test_cart.items == [banana]

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
    

#Test case for item correctly removed from cart and added units updated
def test_remove_item_from_cart_increment(test_cart, capfd, test_products):

    #Extracts products
    banana = get_product_by_name(test_products, "Banana")
    salmon = get_product_by_name(test_products, "Salmon")

    #Initial units for Salmon
    initial_salmon_units = salmon.units

    #Adds items to cart
    test_cart.add_item(banana)
    test_cart.add_item(salmon)

    # Ensure that the shopping cart has a banana and a salmon
    assert test_cart.items == [banana, salmon]

    #Run remove_item function
    remove_item_from_cart(test_cart, salmon, test_products)

    # Captured the print
    captured = capfd.readouterr()
    
    #Expected output
    expected_output = "Remaining items in cart: \n['Banana', 1.0, 15]"

    #Updated salmon units
    salmon = get_product_by_name(test_products, "Salmon")
    final_salmon_units = salmon.units

    assert final_salmon_units == initial_salmon_units+1
    #Asserts that the expected output matches the correct output
    assert expected_output == captured.out.strip()
    

#Test case for item correctly removed from cart and added to products list
def test_remove_item_from_cart_added(test_cart, capfd, test_products):
    #Extracts product
    product = Product("Product", 10.0, 5)

    #Make sure it's not in products list
    assert product not in test_products

    #Adds single item to cart
    test_cart.add_item(product)

    # Ensure that the shopping cart has a product
    assert test_cart.items == [product]

    #Run remove_item function
    remove_item_from_cart(test_cart, product, test_products)

    # Ensure that the shopping cart has no product
    assert test_cart.items == []

    # Captured the print
    captured = capfd.readouterr()
    
    #Expected output
    expected_output = "No remaining products in cart."
    
    #Asserts that the expected output matches the correct output
    assert expected_output == captured.out.strip()

    #Make sure it's in products list
    assert product in test_products


## TEST check_cart tests: 1, 2, 3, 4, 5

#Test case for not checking out an empty cart
def test_no_checkout_empty_cart(test_user, test_cart, test_products, mock_input):
    mock_input.side_effect = ["N"]

    # Updates users balance
    test_user.wallet = 10.0

    # Ensure that the shopping cart is empty 
    assert not test_cart.items

    #Run check_cart function
    result = check_cart(test_user, test_cart, test_products)

    # Asserts false return
    assert result is False
    
    # Ensure that the user's wallet remains unchanged
    assert test_user.wallet == 10.0

#Test case for not checking out a non-empty cart
def test_no_checkout_non_empty_cart(test_user, test_cart, test_products, capfd, mock_input):
    mock_input.side_effect = ["N"]

    # Updates users balance
    test_user.wallet = 10.0

    #Extracts product
    banana = get_product_by_name(test_products, "Banana")

    #Adds single item to cart, banana costs 1
    test_cart.add_item(banana)

    # Ensure that the shopping cart has a banana
    assert test_cart.items == [banana]

    #Run check_cart function
    result = check_cart(test_user, test_cart, test_products)

    # Captured the print
    captured = capfd.readouterr()
    
    #Expected output
    expected_output = "['Banana', 1.0, 15]"

    # Asserts false return
    assert result is False

    #Asserts that the expected output matches the correct output
    assert expected_output == captured.out.strip()
    
    # Ensure that the user's wallet remains unchanged
    assert test_user.wallet == 10.0

#Test case for checking out a non-empty cart with sufficient balance
def test_checkout_non_empty_cart(test_user, test_cart, test_products, capfd, mock_input):
    mock_input.side_effect = ["Y"]

    # Updates users balance
    test_user.wallet = 10.0

    #Extracts product
    banana = get_product_by_name(test_products, "Banana")

    #Adds single item to cart, banana costs 1
    test_cart.add_item(banana)

    # Ensure that the shopping cart has a banana
    assert test_cart.items == [banana]

    #Run check_cart function
    check_cart(test_user, test_cart, test_products)

    # Captured the print
    captured = capfd.readouterr()
    
    #Expected output
    expected_output = f"['Banana', 1.0, 15]\n\n\nThank you for your purchase, {test_user.name}! Your remaining balance is {test_user.wallet}"

    #Asserts that the expected output matches the correct output
    assert expected_output == captured.out.strip()
    
    # Ensure that the user's wallet has been changed
    assert test_user.wallet == 9.0

#Test case for checking out an empty cart lower case y
def test_case_sensitivity(test_user, test_cart, test_products, capfd, mock_input):
    mock_input.side_effect = ["y"]

    # Updates users balance
    test_user.wallet = 10.0

    #Extracts product
    banana = get_product_by_name(test_products, "Banana")

    #Adds single item to cart, banana costs 1
    test_cart.add_item(banana)

    # Ensure that the shopping cart has a banana
    assert test_cart.items == [banana]

    #Run check_cart function
    check_cart(test_user, test_cart, test_products)

    # Captured the print
    captured = capfd.readouterr()
    
    #Expected output
    expected_output = f"['Banana', 1.0, 15]\n\n\nThank you for your purchase, {test_user.name}! Your remaining balance is {test_user.wallet}"

    #Asserts that the expected output matches the correct output
    assert expected_output == captured.out.strip()
    
    # Ensure that the user's wallet has been changed
    assert test_user.wallet == 9.0

#Test case for checking out an empty cart
def test_checkout_empty_cart(test_user, test_cart, test_products, capfd, mock_input):
    mock_input.side_effect = ["Y"]

    # Updates users balance
    test_user.wallet = 10.0

    # Ensure that the shopping cart is empty 
    assert not test_cart.items

    #Run check_cart function
    check_cart(test_user, test_cart, test_products)

    # Captured the print
    captured = capfd.readouterr()
    
    #Expected output
    expected_output = f"Your basket is empty. Please add items before checking out."

    #Asserts that the expected output matches the correct output
    assert expected_output == captured.out.strip()
    
    # Ensure that the user's wallet remains unchanged
    assert test_user.wallet == 10.0

# TEST CHECKOUT tests: 1, 2, 3, 4, 5

#Test case for checking out an empty cart
def test_checkout_empty_cart_checkout(test_user, test_cart, test_products, capfd):
    # Updates users balance
    test_user.wallet = 10.0

    #Checkout the cart
    checkout(test_user, test_cart, test_products)

    # Captured the print
    captured = capfd.readouterr()
    
    #Expected output
    expected_output = "Your basket is empty. Please add items before checking out."

    #Asserts that the expected output matches the correct output
    assert expected_output == captured.out.strip()
    
    # Ensure that the user's wallet remains unchanged
    assert test_user.wallet == 10.0

    # Ensure that the shopping cart remains empty
    assert not test_cart.items

#Test case for checking out an empty cart and empty wallet
def test_checkout_empty_cart_and_wallet(test_user, test_cart, test_products, capfd):
    #Checkout the cart
    checkout(test_user, test_cart, test_products)

    # Captured the print
    captured = capfd.readouterr()
    
    #Expected output
    expected_output = "Your basket is empty. Please add items before checking out."

    #Asserts that the expected output matches the correct output
    assert expected_output == captured.out.strip()
    
    # Ensure that the user's wallet remains unchanged
    assert test_user.wallet == 0.0

    # Ensure that the shopping cart remains empty
    assert not test_cart.items

#Test case for checking out a cart with user having a balance of zero
def test_zero_wallet_balance(test_user, test_cart, test_products, capfd):
    #Extracts product
    banana = get_product_by_name(test_products, "Banana")

    #Adds single item to cart
    test_cart.add_item(banana)

    #Checkout the cart
    checkout(test_user, test_cart, test_products)

    # Captured the print
    captured = capfd.readouterr()
    
    #Expected output
    expected_output = "You don't have enough money to complete the purchase.\nPlease try again!"

    #Asserts that the expected output matches the correct output
    assert expected_output == captured.out.strip()
    
    # Ensure that the user's wallet remains unchanged
    assert test_user.wallet == 0.0

    # Ensure that the shopping cart remains unchanged
    assert test_cart.items == [banana]

#Test case for 2 items insufficient wallet balance
def test_2_items_insufficient_checkout(test_user, test_cart, test_products, capfd):
    # Updates users balance
    test_user.wallet = 10.0
    #Tests the users wallet amount
    assert test_user.wallet == 10.0

    #Extracts products
    banana = get_product_by_name(test_products, "Banana")
    salmon = get_product_by_name(test_products, "Salmon")

    #asserts correct number of item in stock.
    assert banana.units == 15
    assert salmon.units == 2

    #Adds single item to cart
    test_cart.add_item(banana)
    test_cart.add_item(salmon)

    #Checkout the cart
    checkout(test_user, test_cart, test_products)

    # Captured the print
    captured = capfd.readouterr()
    
    #Expected output
    expected_output = "You don't have enough money to complete the purchase.\nPlease try again!"

    #Asserts that the expected output matches the correct output
    assert expected_output == captured.out.strip()

    #assert that there has been one banana subtracted from stock
    assert banana.units == 15
    assert salmon.units == 2
    
    # Ensure that the user's wallet has the correct balance
    assert test_user.wallet == 10.0

    # Ensure that the shopping cart remains unchanged
    assert test_cart.items == [banana, salmon]

#Test case for checking out a cart with user having a negative balance
def test_negative_wallet_balance(test_user, test_cart, test_products, capfd):
    # Updates users balance
    test_user.wallet = -10

    #Extracts product
    banana = get_product_by_name(test_products, "Banana")

    #Adds single item to cart, banana costs 1
    test_cart.add_item(banana)

    #Checkout the cart
    checkout(test_user, test_cart, test_products)

    # Captured the print
    captured = capfd.readouterr()
    
    #Expected output
    expected_output = "You don't have enough money to complete the purchase.\nPlease try again!"

    #Asserts that the expected output matches the correct output
    assert expected_output == captured.out.strip()
    
    # Ensure that the user's wallet remains unchanged
    assert test_user.wallet == -10.0

    # Ensure that the shopping cart remains unchanged
    assert test_cart.items == [banana]

# TEST LOAD_PRODUCTS_FROM_CSV tests: 1, 2, 3, 4, 5
# Test 1: Calling function with invalid input type int
def test_int_input():
    with pytest.raises(TypeError):
        load_products_from_csv(1)

# Test 2: Calling function with invalid input type float
def test_float_input():
    with pytest.raises(TypeError):
        load_products_from_csv(0.5)

# Test 3: Calling function with invalid input type list
def test_list_input():
    with pytest.raises(TypeError):
        load_products_from_csv([1])

# Test 4: Loading products from a CSV file with incorrect file path
def test_incorrect_file_path():
    with pytest.raises(FileNotFoundError):
        load_products_from_csv('non_existent_file.csv')

# Test 5: Loading products from a CSV file with wrong data type of a value
def test_invalid_values_in_file(valid_csv_file):
    # Create a CSV file with mixed data types
    with open(valid_csv_file, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Product', 'Price', 'Units'])
        csv_writer.writerow(['Apple', 1.00, 10])
        csv_writer.writerow(['Banana', 0.75, 8])
        csv_writer.writerow(['Orange', 1.25, 12.5]) # Float in the 'Units' column

    # Check that exception was thrown
    with pytest.raises(ValueError):
        load_products_from_csv(valid_csv_file)

# TEST DISPLAY_CSV_AS_TABLE tests: 1, 2, 3, 4, 5
def create_temporary_file(content='', _suffix='.csv'):
    temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix=_suffix)
    temp_file.write(content)
    temp_file.close()
    return temp_file

def test_empty_csv_file_table():
    csv_content = ''
    temp_file = create_temporary_file(csv_content, '.csv')
    with pytest.raises(Exception):
        display_csv_as_table(temp_file.name)

def test_csv_file_with_only_header():
    csv_content = 'header1,header2,header3\n'
    temp_file = create_temporary_file(csv_content, '.csv')
    with patch('sys.stdout', new_callable=tempfile.SpooledTemporaryFile, mode='w+t', create=True) as mock_stdout:
        display_csv_as_table(temp_file.name)
        mock_stdout.seek(0)
        captured_output = mock_stdout.read()
    expected_output = "['header1', 'header2', 'header3']\n"
    assert captured_output == expected_output

def test_csv_file_with_header_and_one_row():
    csv_content = 'header1,header2,header3\nvalue1,value2,value3\n'
    temp_file = create_temporary_file(csv_content, '.csv')
    with patch('sys.stdout', new_callable=tempfile.SpooledTemporaryFile, mode='w+t', create=True) as mock_stdout:
        display_csv_as_table(temp_file.name)
        mock_stdout.seek(0)
        captured_output = mock_stdout.read()
    expected_output = "['header1', 'header2', 'header3']\n['value1', 'value2', 'value3']\n"
    assert captured_output == expected_output

def test_csv_file_no_header_one_row():
    csv_content = 'value1,value2,value3\n'
    temp_file = create_temporary_file(csv_content, '.csv')
    with patch('sys.stdout', new_callable=tempfile.SpooledTemporaryFile, mode='w+t', create=True) as mock_stdout:
        display_csv_as_table(temp_file.name)
        mock_stdout.seek(0)
        captured_output = mock_stdout.read()
    expected_output = "['value1', 'value2', 'value3']\n"
    assert captured_output == expected_output

def test_csv_file_with_header_and_several_rows():
    csv_content = 'header1,header2,header3\nvalue1,value2,value3\nvalue4,value5,value6\n'
    temp_file = create_temporary_file(csv_content, '.csv')
    with patch('sys.stdout', new_callable=tempfile.SpooledTemporaryFile, mode='w+t', create=True) as mock_stdout:
        display_csv_as_table(temp_file.name)
        mock_stdout.seek(0)
        captured_output = mock_stdout.read()
    expected_output = "['header1', 'header2', 'header3']\n['value1', 'value2', 'value3']\n['value4', 'value5', 'value6']\n"
    assert captured_output == expected_output

# TEST DISPLAY_FILTERED_TABLE tests: 1, 2, 3, 4, 5
# Test empty csv file
def test_empty_csv_file():
    csv_content = ''
    # Create a temporary CSV file
    temp_file = create_temporary_file(csv_content, '.csv')
    with pytest.raises(Exception):
        display_filtered_table(temp_file.name, "search")

# Test non-file string
def test_non_file_string():
    with patch('builtins.open', return_value=StringIO()) as mock_open:
        with pytest.raises(Exception):
            display_filtered_table('not_a_file', "search")

# Test empty search no rows
def test_empty_search_no_rows():
    csv_content = 'Product,Price,Units\n'
    # Create a temporary CSV file
    temp_file = create_temporary_file(csv_content, '.csv')
    # Test function with mock stdout
    with patch('sys.stdout', new_callable=tempfile.SpooledTemporaryFile, mode='w+t', create=True) as mock_stdout:
        display_filtered_table(temp_file.name, "")
        mock_stdout.seek(0)
        captured_output = mock_stdout.read()
    expected_output = "['Product', 'Price', 'Units']\n"
    assert captured_output == expected_output

# Test empty search 1 row
def test_empty_search_one_row():
    csv_content = 'Product,Price,Units\nApple,5,25\n'
    # Create a temporary CSV file
    temp_file = create_temporary_file(csv_content, '.csv')
    # Test function with mock stdout
    with patch('sys.stdout', new_callable=tempfile.SpooledTemporaryFile, mode='w+t', create=True) as mock_stdout:
        display_filtered_table(temp_file.name, "")
        mock_stdout.seek(0)
        captured_output = mock_stdout.read()
    expected_output = "['Product', 'Price', 'Units']\n"
    assert captured_output == expected_output

# Test search not in 1 row
def test_failed_search_one_row():
    csv_content = 'Product,Price,Units\nApple,5,25\n'
    # Create a temporary CSV file
    temp_file = create_temporary_file(csv_content, '.csv')
    # Test function with mock stdout
    with patch('sys.stdout', new_callable=tempfile.SpooledTemporaryFile, mode='w+t', create=True) as mock_stdout:
        display_filtered_table(temp_file.name, "banana")
        mock_stdout.seek(0)
        captured_output = mock_stdout.read()
    expected_output = "['Product', 'Price', 'Units']\n"
    assert captured_output == expected_output

# TEST SEARCH_AND_BUY_PRODUCT tests: 1, 2, 3, 4, 5
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

# TEST LOGIN tests: 1, 2, 3, 4, 5
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
def test_login_new_dont_create(mock_input, mock_open):
    # Set the expected user input
    mock_input.side_effect = ["NewUser", "doesntmatter", "No"]

    result = login()

    # Assert that a new user was not created
    assert result is None
#Login as new user and create a new, with a password that is acceptable
def test_login_new_create(mock_input, mock_open):
    # Set the expected user input
    mock_input.side_effect = ["NewUser", "new", "Yes", "CorrectPassword!"]

    result = login()

    # Assert that new user was created succesfully
    assert result == {"username": "NewUser", "wallet": 0}
#Login as new user and create a new, with a password with less than 8 characters
def test_login_new_short_password(mock_input, mock_open):
    # Set the expected user input
    mock_input.side_effect = ["NewUser", "new", "Yes", "Cool12!"]

    result = login()

    # Assert that the creation was unsuccessful and returned None
    assert result == None

# TEST LOGOUT tests: 1, 2, 3, 4, 5
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
