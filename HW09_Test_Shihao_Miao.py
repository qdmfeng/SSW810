"""
SSW810 Homework 8 Test FIle
Created on 10/22/2019
by Shihao Miao
"""

import unittest
from HW09_Shihao_Miao import *


class TestModuleGeneratorFile(unittest.TestCase):
    """Unit Test for HW09"""


    def test_Repository(self):
        """test case for Repository"""
        a = Repository('./test')
        self.assertEqual(a.students['10103'].classes_taken,
                         {'SSW 567': 'A', 'SSW 564': 'A-', 'SSW 687': 'B', 'CS 501': 'B'})
        self.assertEqual(a.students['10115'].name,
                         ' ')
        self.assertEqual(a.students['10172'].classes_taken,
                         {})
        self.assertEqual(a.instructors['98765'].name,
                         ' ')
        with self.assertRaises(FileNotFoundError):
            a = Repository('DoNotExist')


if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)
