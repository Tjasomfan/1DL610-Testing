import pytest
from unittest.mock import patch
import tempfile
from io import StringIO
from products import display_filtered_table

def create_temporary_file(content='', _suffix='.csv'):
    temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix=_suffix)
    temp_file.write(content)
    temp_file.close()
    return temp_file

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
