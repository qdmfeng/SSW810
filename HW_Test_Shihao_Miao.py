"""
SSW810 Homework 10 Test FIle
Created on 11/4/2019
by Shihao Miao
"""

import unittest
from HW_Shihao_Miao import *


class TestModuleGeneratorFile(unittest.TestCase):
    """Unit Test for HW10"""


    def test_Repository(self):
        """test case for Repository"""
        a = Repository('.')
        self.assertEqual(a._major['SFEN'].r_courses,['SSW 540', 'SSW 564', 'SSW 555', 'SSW 567'])
        self.assertEqual(a._major['SFEN'].e_courses,['CS 501', 'CS 513', 'CS 545'])
        self.assertEqual(a._major['SYEN'].r_courses,['SYS 671', 'SYS 612', 'SYS 800'])
        self.assertEqual(a._major['SYEN'].e_courses,['SSW 810', 'SSW 565', 'SSW 540'])
        self.assertEqual(a._students['10103'].classes_remain['E'],['CS 513', 'CS 545'])
        self.assertEqual(a._students['10103'].classes_remain['R'],['SSW 540', 'SSW 555'])

        with self.assertRaises(FileNotFoundError):
            a = Repository('DoNotExist')


if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)
