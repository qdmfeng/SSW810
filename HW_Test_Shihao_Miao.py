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
        self.assertEqual(a._major['SFEN'].r_courses, {'SSW 540', 'SSW 555', 'SSW 810'})
        self.assertEqual(a._major['SFEN'].e_courses, {'CS 501', 'CS 546'})
        self.assertEqual(a._major['CS'].r_courses, {'CS 546', 'CS 570'})
        self.assertEqual(a._major['CS'].e_courses, {'SSW 565', 'SSW 810'})
        self.assertEqual(a._students['10103'].classes_remain['E'], set())
        self.assertEqual(a._students['10103'].classes_remain['R'], {'SSW 540', 'SSW 555'})

        r = [['98764', 'Cohen, R', 'SFEN', 'CS 546', 1],
             ['98762', 'Hawking, S', 'CS', 'CS 501', 1],
             ['98762', 'Hawking, S', 'CS', 'CS 546', 1],
             ['98762', 'Hawking, S', 'CS', 'CS 570', 1],
             ['98763', 'Rowland, J', 'SFEN', 'SSW 555', 1],
             ['98763', 'Rowland, J', 'SFEN', 'SSW 810', 4]]
        self.assertEqual(a.instructor_table_db('./810.sqlite')._rows, r)


if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)
