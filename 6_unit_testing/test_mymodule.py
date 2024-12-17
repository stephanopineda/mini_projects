'''
This is a code for unit testing a code.
'''
import unittest
from mymodule import square, double, add

class TestSquare(unittest.TestCase):
    ''' This is a class for testing the square function from mymodule.py.
    '''
    def test_1(self):
        '''This function calls itself and tests different values.'''
        self.assertEqual(square(2), 4)
        self.assertEqual(square(3.0), 9.0)
        self.assertNotEqual(square(-3), -9)

class TestDouble(unittest.TestCase):
    ''' This is a class for testing the double function from mymodule.py.
    '''
    def test_1(self):
        '''This function calls itself and tests different values.'''
        self.assertEqual(double(2), 4)
        self.assertEqual(double(-3.1), -6.2)
        self.assertEqual(double(0), 0)

class TestAdd(unittest.TestCase):
    ''' This is a class for testing the add function from mymodule.py.
    '''
    def test_1(self):
        ''' This function calls itself and tests the add function. '''
        # When 2 and 4 are given as input the output must be 6.
        self.assertEqual(add(2, 4), 6)

        # When 0 and 0 are given as input the output must be 0.
        self.assertEqual(add(0, 0), 0)

        # When 2.3 and 3.6 are given as input the output must be 5.9.
        self.assertEqual(add(2.3, 3.6), 5.9)

        #When the strings ‘hello’ and ‘world’ are given as input the output must be ‘helloworld’.
        self.assertEqual(add('hello', 'world'), 'helloworld')

        # When 2.3000 and 4.300 are given as input the output must be 6.6.
        self.assertEqual(add(2.3000, 4.3000), 6.6)

        # When -2 and -2 are given as input the output must not be 0. (Hint : Use assertNotEqual)
        self.assertNotEqual(add(-2,-2), 0)

unittest.main()
