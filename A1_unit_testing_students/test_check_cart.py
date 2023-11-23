from checkout_and_payment import *
import pytest
import shutil
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

#Test case for checking out an empty cart
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

#Test case for checking out an empty cart
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

#Test case for checking out an empty cart
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

#Test case for checking out not checking out a cart, and then checking it out
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


#Test case for updating cart and then checking out
def test_no_checkout_non_empty_cart_then_checkout(test_user, test_cart, test_products, capfd, mock_input):
    mock_input.side_effect = ["N","Y"]

    # Updates users balance
    test_user.wallet = 50.0

    #Extracts product
    banana = get_product_by_name(test_products, "Banana")
    salmon = get_product_by_name(test_products, "Salmon")
    pb = get_product_by_name(test_products, "Peanut Butter")

    #Adds items to cart
    test_cart.add_item(banana)
    test_cart.add_item(salmon)
    test_cart.add_item(pb)

    # Ensure that the shopping cart has the correct items
    assert test_cart.items == [banana, salmon, pb]

    #Run check_cart function
    result = check_cart(test_user, test_cart, test_products)

    # Asserts false return
    assert result is False

    #Expected output
    expected_output = f"['Banana', 1.0, 15]\n['Salmon', 10.0, 2]\n['Peanut Butter', 3.0, 6]"

    # Captured the print
    captured = capfd.readouterr()

    #Asserts that the expected output matches the correct output
    assert expected_output == captured.out.strip()

    #Removes salmon from cart
    test_cart.remove_item(salmon)

    # Ensure that the shopping cart has the correct items
    assert test_cart.items == [banana, pb]

    #Run check_cart function
    check_cart(test_user, test_cart, test_products)

    # Captured the print
    captured = capfd.readouterr()

    #Expected output
    expected_output = f"['Banana', 1.0, 15]\n['Peanut Butter', 3.0, 6]\n\n\nThank you for your purchase, {test_user.name}! Your remaining balance is {test_user.wallet}"

    #Asserts that the expected output matches the correct output
    assert expected_output == captured.out.strip()
    
    # Ensure that the user's wallet has been changed
    assert test_user.wallet == 46.0

#Test case for check_cart twice
def test_check_cart_twice(test_user, test_cart, test_products, capfd, mock_input):
    mock_input.side_effect = ["Y","Y"]

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

    #Run check_cart function
    check_cart(test_user, test_cart, test_products)

    # Captured the print
    captured = capfd.readouterr()

    #Expected output
    expected_output = f"Your basket is empty. Please add items before checking out."

    #Asserts that the expected output matches the correct output
    assert expected_output == captured.out.strip()
    
    # Ensure that the user's wallet has been changed
    assert test_user.wallet == 9.0

#Test case for check_cart three times with a random input
def test_check_cart_three_times(test_user, test_cart, test_products, capfd, mock_input):
    mock_input.side_effect = ["Y", "adasdafADasdaw23!", "Y"]

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


    # Ensure that the shopping cart is empty
    assert not test_cart.items 
    #Run check_cart function
    result = check_cart(test_user, test_cart, test_products)
    # Asserts false return
    assert result is False
    #Expected output
    expected_output = f""
    # Captured the print
    captured = capfd.readouterr()
    #Asserts that the expected output matches the correct output
    assert expected_output == captured.out.strip()

    #Run check_cart function
    check_cart(test_user, test_cart, test_products)
    # Captured the print
    captured = capfd.readouterr()
    #Expected output
    expected_output = f"Your basket is empty. Please add items before checking out."
    #Asserts that the expected output matches the correct output
    assert expected_output == captured.out.strip()
    # Ensure that the user's wallet has been changed
    assert test_user.wallet == 9.0

#Test case for check_cart and emptying stock, then trying to re-add the item. Instead of cart being empty it shows None
def test_check_cart_to_empty_stock(test_user, test_cart, test_products, capfd, mock_input):
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

    test_cart.add_item(salmon)

    # Ensure that the shopping cart is empty
    assert not test_cart.items

#Test case for check_cart twice, after emptying the stock. Instead of cart being empty it shows None
def test_check_cart_twice(test_user, test_cart, test_products, capfd, mock_input):
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

