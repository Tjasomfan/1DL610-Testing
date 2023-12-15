import pytest
from unittest.mock import patch
import tempfile
from io import StringIO
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

def test_int_input():
    csv_content = ''
    temp_file = create_temporary_file(csv_content, '.csv')
    with pytest.raises(Exception):
        display_csv_as_table(15)

def test_float_input():
    csv_content = ''
    temp_file = create_temporary_file(csv_content, '.csv')
    with pytest.raises(Exception):
        display_csv_as_table(5003.5)

def test_list_input():
    csv_content = ''
    temp_file = create_temporary_file(csv_content, '.csv')
    with pytest.raises(Exception):
        display_csv_as_table([temp_file.name, "hello.csv", "products.csv", "login.py"])
