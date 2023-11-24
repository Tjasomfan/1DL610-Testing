from checkout_and_payment import load_products_from_csv
import pytest
import tempfile
import csv
import os
import shutil

# ==============================================================================
# FIXTURE
# ==============================================================================

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

# ==============================================================================
# TEST SUITE
# ==============================================================================

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