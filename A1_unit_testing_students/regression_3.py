from checkout_and_payment import *
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
def copy_csv_file():
    # Set up: Copy the CSV file 
    shutil.copy('products.csv','copy_products.csv') 
    yield
    # Teardown: Remove the copied CSV file 
    os.remove('copy_products.csv')

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

#Function to filter a product by name from the products list
def get_product_by_name(products, target_name):
    for product in products:
        if product.name == target_name:
            return product
    return None  # Return None if the product with the specified name is not found

# Fixture to mock the input function
@pytest.fixture
def mock_input(mocker):
    return mocker.patch('builtins.input')

## TEST check_cart tests: 1,2,8,9,10

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


#Test case for checking out non-empty cart with insufficient balance
def test_checkout_insufficient_balance(test_user, test_cart, test_products, capfd, mock_input):
    mock_input.side_effect = ["Y"]

    # Updates users balance
    test_user.wallet = 0.0

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
    expected_output = "['Banana', 1.0, 15]\n\n\nYou don't have enough money to complete the purchase.\nPlease try again!"

    #Asserts that the expected output matches the correct output
    assert expected_output == captured.out.strip()
    
    # Ensure that the user's wallet has been changed
    assert test_user.wallet == 0.0

#Test case for check_cart and emptying stock, then trying to re-add the item. Instead of cart being empty it shows None
def test_check_cart_to_empty_stock(test_user, test_cart, test_products, capfd, mock_input):
    mock_input.side_effect = ["Y"]
    # Updates users balance
    test_user.wallet = 30.0
    #Tests the users wallet amount
    assert test_user.wallet == 30.0

    salmon = get_product_by_name(test_products, "Salmon")

    #asserts correct number of item in stock.
    assert salmon.units == 2

    #Adds single item to cart
    test_cart.add_item(salmon)
    test_cart.add_item(salmon)

    # Ensure that the shopping cart has two salmons in it
    assert test_cart.items == [salmon, salmon]

    #Run check_cart function
    check_cart(test_user, test_cart, test_products)

    # Captured the print
    captured = capfd.readouterr()

    #Expected output
    expected_output = f"['Salmon', 10.0, 2]\n['Salmon', 10.0, 2]\n\n\nThank you for your purchase, {test_user.name}! Your remaining balance is {test_user.wallet}"

    #Asserts that the expected output matches the correct output
    assert expected_output == captured.out.strip()

    # Ensure that the user's wallet has been changed
    assert test_user.wallet == 10.0

    #assert that there has been one banana subtracted from stock
    assert salmon.units == 0
    
    # Ensure that the user's wallet has the correct balance
    assert test_user.wallet == 10.0

    # Ensure that the shopping cart is empty
    assert test_cart.items == []

    #extracts salmon again
    salmon = get_product_by_name(test_products, "Salmon")

    #checks that there is no item named salmon anymore in products list
    assert salmon == None

    test_cart.add_item(salmon)

    # Ensure that the shopping cart is empty
    assert not test_cart.items

#Test case for check_cart twice, after emptying the stock. Instead of cart being empty it shows None
def test_check_cart_twice_after_emptying_stock(test_user, test_cart, test_products, capfd, mock_input):
    mock_input.side_effect = ["Y","Y"]
    # Updates users balance
    test_user.wallet = 30.0
    #Tests the users wallet amount
    assert test_user.wallet == 30.0

    salmon = get_product_by_name(test_products, "Salmon")

    #asserts correct number of item in stock.
    assert salmon.units == 2

    #Adds single item to cart
    test_cart.add_item(salmon)
    test_cart.add_item(salmon)

    # Ensure that the shopping cart has two salmons in it
    assert test_cart.items == [salmon, salmon]

    #Run check_cart function
    check_cart(test_user, test_cart, test_products)

    # Captured the print
    captured = capfd.readouterr()

    #Expected output
    expected_output = f"['Salmon', 10.0, 2]\n['Salmon', 10.0, 2]\n\n\nThank you for your purchase, {test_user.name}! Your remaining balance is {test_user.wallet}"

    #Asserts that the expected output matches the correct output
    assert expected_output == captured.out.strip()

    # Ensure that the user's wallet has been changed
    assert test_user.wallet == 10.0

    #assert that there has been one banana subtracted from stock
    assert salmon.units == 0
    
    # Ensure that the user's wallet has the correct balance
    assert test_user.wallet == 10.0

    # Ensure that the shopping cart is empty
    assert test_cart.items == []

    #extracts salmon again
    salmon = get_product_by_name(test_products, "Salmon")

    #checks that there is no item named salmon anymore in products list
    assert salmon == None

    #adds salmon to cart, cart should remain empty
    test_cart.add_item(salmon)

    #Run check_cart function
    try: 
        check_cart(test_user, test_cart, test_products)
        # Captured the print
        captured = capfd.readouterr()

        #Expected output
        expected_output = f"Your basket is empty. Please add items before checking out."

        #Asserts that the expected output matches the correct output
        assert expected_output == captured.out.strip()
    except Exception as e:
        pytest.fail(f"Caught the correct exception: {e}")


## TEST checkout tests: 1,2,8,9,10
        
#Test case for checking out an empty cart
def test_checkout_empty_cart(test_user, test_cart, test_products, capfd):
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

#Test case for product being bought up and removed from products list
def test_remove_item_from_products(test_user, test_cart, test_products, capfd):
    # Updates users balance
    test_user.wallet = 30.0
    #Tests the users wallet amount
    assert test_user.wallet == 30.0

    salmon = get_product_by_name(test_products, "Salmon")

    #asserts correct number of item in stock.
    assert salmon.units == 2

    #Adds single item to cart
    test_cart.add_item(salmon)
    test_cart.add_item(salmon)

    #Checkout the cart
    checkout(test_user, test_cart, test_products)
    
   
    #assert that there has been one banana subtracted from stock
    assert salmon.units == 0
    
    # Ensure that the user's wallet has the correct balance
    assert test_user.wallet == 10.0

    # Ensure that the shopping cart is empty
    assert test_cart.items == []

    #extracts salmon again
    salmon = get_product_by_name(test_products, "Salmon")

    #checks that there is no item named salmon anymore in products list
    assert salmon == None

#Test case for insufficient units, shouldn't be able to check out when too many items are in cart, although this check isn't programmed
def test_checkout_with_insufficient_units(test_user, test_cart, test_products, capfd):
    # Updates users balance
    test_user.wallet = 30.0
    #Tests the users wallet amount
    assert test_user.wallet == 30.0

    salmon = get_product_by_name(test_products, "Salmon")

    #asserts correct number of item in stock.
    assert salmon.units == 2

    #Adds single item to cart
    test_cart.add_item(salmon)
    test_cart.add_item(salmon)
    test_cart.add_item(salmon)

    #Checkout the cart
    checkout(test_user, test_cart, test_products)
    
    # Captured the print
    captured = capfd.readouterr()

    #assert that there has been one banana subtracted from stock
    assert salmon.units == 0
    
    # Ensure that the user's wallet has the correct balance
    assert test_user.wallet == 10.0


#Test case for checking out non-existing product in products-list.
def test_checkout_non_existing_product(test_user, test_cart, test_products, capfd):
    # Updates users balance
    test_user.wallet = 30.0
    #Tests the users wallet amount
    assert test_user.wallet == 30.0

    product = Product("Product", 10.0, 5)


    #Adds single item to cart
    test_cart.add_item(product)

    #Checkout the cart
    checkout(test_user, test_cart, test_products)
    
    # Captured the print
    captured = capfd.readouterr()
    
    # Ensure that the user's wallet has the correct balance
    assert test_user.wallet == 30.0


## TEST load_products_from_csv tests: 1,2,8,9,10
    

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


# Test 1: Calling function with invalid input type int
def test_int_input():
    with pytest.raises(TypeError):
        load_products_from_csv(1)

# Test 2: Calling function with invalid input type float
def test_float_input():
    with pytest.raises(TypeError):
        load_products_from_csv(0.5)

# Test 8: Loading products from a valid CSV file
def test_valid_file_path(valid_csv_file):
    products = load_products_from_csv(valid_csv_file)

    # Check the number of products loaded
    assert len(products) == 3

    # Check the details of a specific product
    assert products[0].name == 'Apple'
    assert products[0].price == 1.00
    assert products[0].units == 10

# Test 9: Loading products from a empty CSV file 
def test_empty_file(valid_csv_file):
    # Create a CSV file with special characters
    with open(valid_csv_file, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Product', 'Price', 'Units'])

    # Execute the test
    products = load_products_from_csv(valid_csv_file)

    # Check that int was converted to float correctly
    assert len(products) == 0

# Test 10: Loading products from a CSV file with extra columns
def test_extra_columns(valid_csv_file):
    # Create a CSV file with extra columns
    with open(valid_csv_file, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Product', 'Price', 'Units', 'ExtraColumn'])  # Extra 'ExtraColumn'
        csv_writer.writerow(['Apple', 1.00, 10, 'Extra data'])
        csv_writer.writerow(['Banana', 0.75, 8, 'Extra data'])

    # Execute the test
    products = load_products_from_csv(valid_csv_file)

    # Check the number of products loaded
    assert len(products) == 2


## TEST display_csv_as_table tests: 1,2,8,9,10
    
from products import display_csv_as_table

def create_temporary_file(content='', _suffix='.csv'):
    temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix=_suffix)
    temp_file.write(content)
    temp_file.close()
    return temp_file


def test_empty_csv_file():
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

def test_txt_file_with_header_no_rows():
    txt_content = 'header1,header2,header3\n'
    temp_file = create_temporary_file(txt_content, '.txt')
    with patch('sys.stdout', new_callable=tempfile.SpooledTemporaryFile, mode='w+t', create=True) as mock_stdout:
        display_csv_as_table(temp_file.name)
        mock_stdout.seek(0)
        captured_output = mock_stdout.read()
    expected_output = "['header1', 'header2', 'header3']\n"
    assert captured_output == expected_output

def test_non_file_string():
    with patch('builtins.open', return_value=StringIO()):
        with pytest.raises(Exception):
            display_csv_as_table('not_a_file')

def test_empty_string():
    with patch('builtins.open', return_value=StringIO()):
        with pytest.raises(Exception):
            display_csv_as_table('')


## TEST display_filtered_table tests: 1,2,8,9,10
from products import display_filtered_table

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

# Test search in 2 of 2 rows
def test_successful_search_all_rows():
    csv_content = 'Product,Price,Units\nOrange,5,25\nOrange,13,6\n'
    # Create a temporary CSV file
    temp_file = create_temporary_file(csv_content, '.csv')
    # Test function with mock stdout
    with patch('sys.stdout', new_callable=tempfile.SpooledTemporaryFile, mode='w+t', create=True) as mock_stdout:
        display_filtered_table(temp_file.name, "Orange")
        mock_stdout.seek(0)
        captured_output = mock_stdout.read()
    expected_output = "['Product', 'Price', 'Units']\n['Orange', '5', '25']\n['Orange', '13', '6']\n"
    assert captured_output == expected_output

# Test search in only 2nd out of 2 rows
def test_successful_search_last_row():
    csv_content = 'Product,Price,Units\nApple,5,25\nOrange,13,6\n'
    # Create a temporary CSV file
    temp_file = create_temporary_file(csv_content, '.csv')
    # Test function with mock stdout
    with patch('sys.stdout', new_callable=tempfile.SpooledTemporaryFile, mode='w+t', create=True) as mock_stdout:
        display_filtered_table(temp_file.name, "Orange")
        mock_stdout.seek(0)
        captured_output = mock_stdout.read()
    expected_output = "['Product', 'Price', 'Units']\n['Orange', '13', '6']\n"
    assert captured_output == expected_output

# Test search in 2 of 2 rows with different product names
def test_successful_search_all_rows_2():
    csv_content = 'Product,Price,Units\ncar,5,25\ncart,13,6\n'
    # Create a temporary CSV file
    temp_file = create_temporary_file(csv_content, '.csv')
    # Test function with mock stdout
    with patch('sys.stdout', new_callable=tempfile.SpooledTemporaryFile, mode='w+t', create=True) as mock_stdout:
        display_filtered_table(temp_file.name, "cart")
        mock_stdout.seek(0)
        captured_output = mock_stdout.read()
    expected_output = "['Product', 'Price', 'Units']\n['cart', '13', '6']\n"
    assert captured_output == expected_output


## TEST login tests: 1,2,6,7,8

from login import login

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

#Login as new user and create a new, with a password with more than 8 characters
def test_login_new_long_password(mock_input, mock_open):
    # Set the expected user input
    mock_input.side_effect = ["NewUser", "new", "Yes", "CoolGuys123!"]

    result = login()

    # Assert that new user was created succesfully
    assert result == {"username": "NewUser", "wallet": 0}
#Login as new user and create a new, with a password with 8 characters
def test_login_new_just_enough_password(mock_input, mock_open):
    # Set the expected user input
    mock_input.side_effect = ["NewUser", "new", "Yes", "Cool123!"]

    result = login()

    # Assert that new user was created succesfully
    assert result == {"username": "NewUser", "wallet": 0}
#Login as new user and create a new, with a password with special characters but no uppercase characters
def test_login_new_no_uppercase(mock_input, mock_open):
    # Set the expected user input
    mock_input.side_effect = ["NewUser", "new", "Yes", "cool123!"]

    result = login()

    # Assert that new user was not created because of the incorrect password
    assert result == None



## TEST logout tests: 1,2,8,9,10
from logout import logout    

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

#Tests for search_and_buy_product() : 1, 4, 5, 6, 7,
from products import searchAndBuyProduct 

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

#1: Test searching for all
def test_all(mock_input, login_stub, checkoutAndPayment_stub, display_csv_as_table_stub, display_filtered_table_stub):
    mock_input.side_effect = ["all", "y"]
    res = searchAndBuyProduct()

    display_csv_as_table_stub.assert_called_once_with("products.csv")
    assert display_filtered_table_stub.call_count == 0

#4: Test searching for orange and apple
def test_orange_and_apple(mock_input, login_stub, checkoutAndPayment_stub, display_csv_as_table_stub, display_filtered_table_stub):
    mock_input.side_effect = ["orange", "n", "apple", "y"]
    res = searchAndBuyProduct()

    assert display_filtered_table_stub.call_count == 2
    assert display_csv_as_table_stub.call_count == 0

#5: Test searching for orange and apple
def test_login_called(mock_input, login_stub, checkoutAndPayment_stub, display_csv_as_table_stub, display_filtered_table_stub):
    mock_input.side_effect = ["orange", "n", "apple", "y"]
    res = searchAndBuyProduct()

    assert login_stub.call_count == 1
    
#6: Test searching for orange and apple
def test_checkout_called(mock_input, login_stub, checkoutAndPayment_stub, display_csv_as_table_stub, display_filtered_table_stub):
    mock_input.side_effect = ["orange", "n", "apple", "y"]
    res = searchAndBuyProduct()

    assert checkoutAndPayment_stub.call_count == 1

#7: Test answer hello instead of y/n
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
    
