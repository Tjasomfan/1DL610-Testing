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



#Test case for checking out an empty cart
def test_checkout_empty_cart(test_user, test_cart, test_products, capfd):
    # Updates users balance
    test_user.wallet = 10.0

    #Creates empty cart
    cart = ShoppingCart()

    #Checkout the cart
    checkout(test_user, cart, test_products)

    # Captured the print
    captured = capfd.readouterr()
    
    #Expected output
    expected_output = "Your basket is empty. Please add items before checking out."

    #Asserts that the expected output matches the correct output
    assert expected_output == captured.out.strip()
    
    # Ensure that the user's wallet remains unchanged
    assert test_user.wallet == 10.0

    # Ensure that the shopping cart remains empty
    assert not cart.items

#Test case for checking out an empty cart and empty wallet
def test_checkout_empty_cart_and_wallet(test_user, test_cart, test_products, capfd):
    #Creates empty cart
    cart = ShoppingCart()

    #Checkout the cart
    checkout(test_user, cart, test_products)

    # Captured the print
    captured = capfd.readouterr()
    
    #Expected output
    expected_output = "Your basket is empty. Please add items before checking out."

    #Asserts that the expected output matches the correct output
    assert expected_output == captured.out.strip()
    
    # Ensure that the user's wallet remains unchanged
    assert test_user.wallet == 0.0

    # Ensure that the shopping cart remains empty
    assert not cart.items

#Function to filter a product by name from the products list
def get_product_by_name(products, target_name):
    for product in products:
        if product.name == target_name:
            return product
    return None  # Return None if the product with the specified name is not found


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

#Test case for insufficient wallet balance
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

    # Ensure that the shopping cart remains unchanged
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

    # Ensure that the shopping cart remains unchanged
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
    
    # Captured the print
    captured = capfd.readouterr()
    
    #assert that there has been one banana subtracted from stock
    assert salmon.units == 0
    
    # Ensure that the user's wallet has the correct balance
    assert test_user.wallet == 10.0

    # Ensure that the shopping cart remains unchanged
    assert test_cart.items == []

    #extracts salmon again
    salmon = get_product_by_name(test_products, "Salmon")

    #checks that there is no item named salmon anymore in products list
    assert salmon == None

#Test case for insufficient units, shouldn't be able to check out when too many items are in cart? Although this check isn't programmed
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
    assert salmon.units == -1
    
    # Ensure that the user's wallet has the correct balance
    assert test_user.wallet == 0.0

    # Ensure that the shopping cart remains unchanged
    assert test_cart.items == []

#Test case for multiple checkouts and large balance
def test_checkout_purchase_more_checkout_and_large_balance(test_user, test_cart, test_products, capfd):
    # Updates users balance
    test_user.wallet = 1000000.0
    #Tests the users wallet amount
    assert test_user.wallet == 1000000.0

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
    assert test_user.wallet == 999989.0

    # Ensure that the shopping cart remains unchanged
    assert test_cart.items == []

    #Adds single item to cart
    test_cart.add_item(banana)
    test_cart.add_item(banana)
    test_cart.add_item(salmon)
    assert banana.units == 14
    assert salmon.units == 1

    #Checkout the cart
    checkout(test_user, test_cart, test_products)

    # Captured the print
    captured = capfd.readouterr()
    
    #Expected output
    expected_output = f"Thank you for your purchase, {test_user.name}! Your remaining balance is {test_user.wallet}"

    #Asserts that the expected output matches the correct output
    assert expected_output == captured.out.strip()

    #assert that there has been one banana subtracted from stock
    assert banana.units == 12
    assert salmon.units == 0
    
    # Ensure that the user's wallet has the correct balance
    assert test_user.wallet == 999977.0

    # Ensure that the shopping cart remains unchanged
    assert test_cart.items == []