from checkout_and_payment import *
import pytest
import shutil
import tempfile
import os

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

# TEST CHECK_CART tests: 6, 7, 8, 9, 10

#Test case for  not checking out a cart, and then checking it out
def test_no_checkout_non_empty_cart_then_checkout(test_user, test_cart, test_products, capfd, mock_input):
    mock_input.side_effect = ["N","Y"]

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

    # Asserts false return
    assert result is False

    #Expected output
    expected_output = f"['Banana', 1.0, 15]"

    # Captured the print
    captured = capfd.readouterr()

    #Asserts that the expected output matches the correct output
    assert expected_output == captured.out.strip()

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

#Test case for random input
def test_random_input(test_user, test_cart, test_products, mock_input):
    mock_input.side_effect = ["asdasdahjwej"]

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


# TEST CHECKOUT tests: 6, 7, 8, 9, 10

#Test case for succesful checkout
def test_succesful_checkout(test_user, test_cart, test_products, capfd):
    # Updates users balance
    test_user.wallet = 1.0
    #Tests the users wallet amount
    assert test_user.wallet == 1.0

    #Extracts product
    banana = get_product_by_name(test_products, "Banana")

    #asserts correct number of item in stock.
    assert banana.units == 15

    #Adds single item to cart, banana costs 1
    test_cart.add_item(banana)

    #Checkout the cart
    checkout(test_user, test_cart, test_products)

    # Captured the print
    captured = capfd.readouterr()
    
    #Expected output
    expected_output = f"Thank you for your purchase, {test_user.name}! Your remaining balance is {test_user.wallet}"

    #Asserts that the expected output matches the correct output
    assert expected_output == captured.out.strip()

    #assert that there has been one banana subtracted from stock
    assert banana.units == 14
    
    # Ensure that the user's wallet has the correct balance
    assert test_user.wallet == 0.0

    # Ensure that the shopping cart is empty
    assert test_cart.items == []

#Test case for succesful checkout for several items
def test_2_items_checkout(test_user, test_cart, test_products, capfd):
    # Updates users balance
    test_user.wallet = 12.0
    #Tests the users wallet amount
    assert test_user.wallet == 12.0

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
    expected_output = f"Thank you for your purchase, {test_user.name}! Your remaining balance is {test_user.wallet}"

    #Asserts that the expected output matches the correct output
    assert expected_output == captured.out.strip()

    #assert that there has been one banana subtracted from stock
    assert banana.units == 14
    assert salmon.units == 1
    
    # Ensure that the user's wallet has the correct balance
    assert test_user.wallet == 1.0

    # Ensure that the shopping cart is empty
    assert test_cart.items == []

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


# TEST LOAD_PRODUCTS_FROM_CSV tests: 6, 7, 8, 9, 10


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

# Test 6: Loading products from a CSV file with empty values
def test_empty_string_value(valid_csv_file):
    # Create a CSV file with empty values
    with open(valid_csv_file, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Product', 'Price', 'Units'])
        csv_writer.writerow(['', 1.0, 10])  # Empty value

    # Check that row with missing value is not returned
    products = load_products_from_csv(valid_csv_file)
    assert len(products) == 0

# Test 7: Loading products from a CSV file with missing columns
def test_missing_columns(valid_csv_file):
    # Create a CSV file with missing columns
    with open(valid_csv_file, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Product', 'Units'])  # Missing 'Price' column

    # Execute the test
    products = load_products_from_csv(valid_csv_file)

    # Check the number of products loaded
    assert len(products) == 0  # No products should be loaded due to the missing column

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


# TEST DISPLAY_CSV_AS_TABLE tests: 6, 7, 8, 9, 10
    
import pytest
from unittest.mock import patch
import tempfile
from io import StringIO
from products import display_csv_as_table, display_filtered_table, searchAndBuyProduct

def create_temporary_file(content='', _suffix='.csv'):
    temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix=_suffix)
    temp_file.write(content)
    temp_file.close()
    return temp_file

def test_txt_file_with_header_and_row():
    txt_content = 'header1,header2,header3\nvalue1,value2,value3\n'
    temp_file = create_temporary_file(txt_content, '.txt')
    with patch('sys.stdout', new_callable=tempfile.SpooledTemporaryFile, mode='w+t', create=True) as mock_stdout:
        display_csv_as_table(temp_file.name)
        mock_stdout.seek(0)
        captured_output = mock_stdout.read()
    expected_output = "['header1', 'header2', 'header3']\n['value1', 'value2', 'value3']\n"
    assert captured_output == expected_output

def test_txt_file_no_header_one_row():
    txt_content = 'value1,value2,value3\n'
    temp_file = create_temporary_file(txt_content, '.txt')
    with patch('sys.stdout', new_callable=tempfile.SpooledTemporaryFile, mode='w+t', create=True) as mock_stdout:
        display_csv_as_table(temp_file.name)
        mock_stdout.seek(0)
        captured_output = mock_stdout.read()
    expected_output = "['value1', 'value2', 'value3']\n"
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


# TEST DISPLAY_FILTERED_TABLE tests: 6, 7, 8, 9, 10
            

# Test search not in 2 rows
def test_failed_search_two_rows():
    csv_content = 'Product,Price,Units\nApple,5,25\nOrange,13,6\n'
    # Create a temporary CSV file
    temp_file = create_temporary_file(csv_content, '.csv')
    # Test function with mock stdout
    with patch('sys.stdout', new_callable=tempfile.SpooledTemporaryFile, mode='w+t', create=True) as mock_stdout:
        display_filtered_table(temp_file.name, "banana")
        mock_stdout.seek(0)
        captured_output = mock_stdout.read()
    expected_output = "['Product', 'Price', 'Units']\n"
    assert captured_output == expected_output

# Test search in 1 of 2 rows
def test_successful_search_first_row():
    csv_content = 'Product,Price,Units\nApple,5,25\nOrange,13,6\n'
    # Create a temporary CSV file
    temp_file = create_temporary_file(csv_content, '.csv')
    # Test function with mock stdout
    with patch('sys.stdout', new_callable=tempfile.SpooledTemporaryFile, mode='w+t', create=True) as mock_stdout:
        display_filtered_table(temp_file.name, "Apple")
        mock_stdout.seek(0)
        captured_output = mock_stdout.read()
    expected_output = "['Product', 'Price', 'Units']\n['Apple', '5', '25']\n"
    assert captured_output == expected_output

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


# TEST SEARCH_AND_BUY_PRODUCT tests: 6, 7, 8, 9, 10
    

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


# TEST LOGIN tests: 6, 7, 8, 9, 10

from login import *

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
#Login as new user and create a new, with a password with uppercase characters but no special characters
def test_login_new_no_special(mock_input, mock_open):
    # Set the expected user input
    mock_input.side_effect = ["NewUser", "new", "Yes", "Cool1234"]

    result = login()

    # Assert that new user was not created because of the incorrect password
    assert result == None
#Login as new user and create a new, with a password with no uppercase characters or special characters
def test_login_new_no_uppercase_special(mock_input, mock_open):
    # Set the expected user input
    mock_input.side_effect = ["NewUser", "new", "Yes", "cool1234"]

    result = login()

    # Assert that new user was not created because of the incorrect password
    assert result == None
    
    #one more test needed

# TEST LOGOUT tests: 6, 7, 8, 9, 10

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
    
