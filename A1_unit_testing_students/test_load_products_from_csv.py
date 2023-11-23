from checkout_and_payment import load_products_from_csv
import pytest
import tempfile
import csv
import os
import shutil

# Function to load products from a CSV file

# Potential issues:
# - Missing or misspelled keys (e.g., 'Product', 'Price', 'Units') in the CSV file
# - Values in 'Price' and 'Units' columns that are not convertible to the expected types (e.g., '1.00' as 'Price' should be convertible to float)
# - The 'Product', 'Price', or 'Units' key may not exist in the current row
# - The values may be empty or contain unexpected characters

# ==============================================================================
# FIXTURE
# ==============================================================================

@pytest.fixture
def valid_csv_file():
    # Create a temporary CSV file for testing
    csv_file = tempfile.NamedTemporaryFile(mode='w', delete=False)

    # Write sample data to the temporary CSV file with correct data types
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Apple', '1.00', '10'])
    csv_writer.writerow(['Banana', '0.75', '8'])
    csv_writer.writerow(['Orange', '1.25', '12'])

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
def test_load_products_from_csv_incorrect_file_path():
    non_existent_file = 'non_existent_file.csv'

    with pytest.raises(FileNotFoundError):
        load_products_from_csv(non_existent_file)

# Test 5: Loading products from a valid CSV file
def test_load_products_from_csv_valid_input(valid_csv_file):
    products = load_products_from_csv(valid_csv_file)

    # Check the number of products loaded
    assert len(products) == 3

    # Check the details of a specific product
    assert products[0].name == 'Apple'
    assert products[0].price == 1.00
    assert products[0].units == 10

# Test 6: Loading products from a CSV file with different data types (string, float, integer)
def test_load_products_from_csv_different_data_types(valid_csv_file):
    # Create a CSV file with mixed data types
    with open(valid_csv_file, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Product', 'Price', 'Units'])
        csv_writer.writerow(['Apple', '1.00', '10'])
        csv_writer.writerow(['Banana', '0.75', '8'])
        csv_writer.writerow(['Orange', '1.25', '12.5'])  # Float in the 'Units' column

    # Execute the test
    products = load_products_from_csv(valid_csv_file)

    # Check the number of products loaded
    assert len(products) == 3

    # Check the details of a specific product
    assert products[2].name == 'Orange'
    assert products[2].price == '1.25'
    assert products[2].units == '12.5'

# Test 7: Loading products from a CSV file with special characters in the values
def test_load_products_from_csv_special_characters(valid_csv_file):
    # Create a CSV file with special characters
    with open(valid_csv_file, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Product', 'Price', 'Units'])
        csv_writer.writerow(['Apple', '1.00', '!@#$%^&*()'])  # Special characters in the 'Units' column

    # Execute the test
    products = load_products_from_csv(valid_csv_file)

    # Check the number of products loaded
    assert len(products) == 1

    # Check the details of the product
    assert products[0].name == 'Apple'
    assert products[0].price == '1.00'
    assert products[0].units == '!@#$%^&*()'

# Test 8: Loading products from a CSV file with empty values
def test_load_products_from_csv_empty_values(valid_csv_file):
    # Create a CSV file with empty values
    with open(valid_csv_file, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Product', 'Price', 'Units'])
        csv_writer.writerow(['', '', ''])  # Empty values in all columns

    # Execute the test
    products = load_products_from_csv(valid_csv_file)

    # Check the number of products loaded
    assert len(products) == 1

    # Check that all fields are empty strings
    assert all(not product.name and not product.price and not product.units for product in products)

# Test 9: Loading products from a CSV file with missing columns
def test_load_products_from_csv_missing_columns(valid_csv_file):
    # Create a CSV file with missing columns
    with open(valid_csv_file, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Product', 'Units'])  # Missing 'Price' column

    # Execute the test
    products = load_products_from_csv(valid_csv_file)

    # Check the number of products loaded
    assert len(products) == 0  # No products should be loaded due to the missing column

# Test 10: Loading products from a CSV file with extra columns
def test_load_products_from_csv_extra_columns(valid_csv_file):
    # Create a CSV file with extra columns
    with open(valid_csv_file, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Product', 'Price', 'Units', 'ExtraColumn'])  # Extra 'ExtraColumn'

    # Execute the test
    products = load_products_from_csv(valid_csv_file)

    # Check the number of products loaded
    assert len(products) == 0  # No products should be loaded due to the extra column

# Test 11: Loading products from a CSV file with a large number of entries
def test_load_products_from_csv_large_number_of_entries(valid_csv_file):
    # Create a CSV file with a large number of entries
    with open(valid_csv_file, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Product', 'Price', 'Units'])
        for i in range(10000):
            csv_writer.writerow([f'Product{i}', '1.00', '10'])

    # Execute the test
    products = load_products_from_csv(valid_csv_file)

    # Check the number of products loaded
    assert len(products) == 10000

# Test 12: Loading products from an empty CSV file
def test_load_products_from_csv_empty_file(valid_csv_file):
    # Create an empty CSV file
    with open(valid_csv_file, 'w', newline='') as csvfile:
        pass  # Empty file

    # Execute the test
    products = load_products_from_csv(valid_csv_file)

    # Check the number of products loaded
    assert len(products) == 0  # No products should be loaded from an empty file

# Test 13: Loading products from a CSV file with invalid file format
def test_load_products_from_csv_invalid_file_format(valid_csv_file):
    # Create a CSV file with invalid format (e.g., not a CSV file)
    with open(valid_csv_file, 'w') as text_file:
        text_file.write("This is not a CSV file")

    # Execute the test
    with pytest.raises(csv.Error):  # Expecting a csv.Error for invalid format
        load_products_from_csv(valid_csv_file)