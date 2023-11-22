This folder contains four files: 

1. polygon.py which contains the function polygon to be tested
2. test_polygon.py which contains the unit tests for the polygon function
3. polygon function testing document 15 nov 2023.docx which is the test function document filled in for this function
4. unitTestingOfPolygonFunction.docx which explains how the input domain modelling was carried out, what the unit testing of the polygon function is supposed to check, how the test requirements were arrived at, how test cases were created.

Please note that the polygon function does not do anything with the result obtained from calling triangle. If, for example, the triangle function returns the three angles of the triangle and the polygon function then does some arithmetic eg checks if any of the angles is more than 90 degrees, then you also have to check this functionality. This means that you dont just check that triang got called, you have to take the value returned by it and do some more checks. Even if your tests dont run perfectly, it is important to have your own version of file 4, which explains your thought process and what exactly you are doing to go about testing. 

#IMPORTANT: You must install pytest-mock to run this test file. Make sure you do "pip install pytest-mock" before running the test file.
