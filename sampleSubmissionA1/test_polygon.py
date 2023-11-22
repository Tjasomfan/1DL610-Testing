from polygon import *
import pytest
#IMPORTANT: You must install pytest-mock to run this test file. Make sure you do "pip install pytest-mock" before running this test file.

@pytest.fixture
def triangle_stub1(mocker):
    return mocker.patch('polygon.triang', return_value="Scale")

@pytest.fixture
def quadrilateral_stub1(mocker):
    return mocker.patch('polygon.quadrilateral', return_value="IrrQuad")

@pytest.fixture
def output_fixture(capsys):
    polygon([1,2,2,4,5,3,5,4])
    out, err = capsys.readouterr()
    return out.strip()

def test_open_file():
    try:
        with open("sampleSubmissionA1/README.md", 'r') as file:
            content = file.read()
        assert True is True
    except Exception as e:
        assert True is False

def test_int_input():
    assert polygon(1)== "Input is not a list"

def test_float_input():
    assert polygon(0.5)== "Input is not a list"

def test_string_input():
    assert polygon("notPoly")== "Input is not a list"

def test_EC1():
    assert polygon([1])== "Not a polygon"

def test_EC2_with_triangle_stub(triangle_stub1, mocker):
    # Call the polygon function, which will use the stubbed triang function
    result = polygon([1, 2, 3])

    # Assert that the triang function was called with the correct arguments
    triangle_stub1.assert_called_once_with(1, 2, 3)

def test_EC3_with_quadrilateral_stub(quadrilateral_stub1, mocker):
    # Call the polygon function, which will use the stubbed quadrilateral function
    result = polygon([1, 2, 3, 4])

    # Assert that the quadrilateral function was called with the correct arguments
    quadrilateral_stub1.assert_called_once_with(1, 2, 3, 4)


def test_EC4():
    assert polygon([1, 2, 3, 4, 5])== "Large Polygon"

def test_EC4_with_output(output_fixture, capsys):
    assert output_fixture == "This is a large polygon"