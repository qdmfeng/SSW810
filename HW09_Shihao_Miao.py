"""
SSW810 Homework 9
Created on 11/5/2019
by Shihao Miao
"""
from prettytable import PrettyTable
import os
from collections import Counter, defaultdict


def file_reading_gen(path, fields, sep=',', header=False):
    """read field-separated text files and yield a tuple with all of the values from a single line in the file """
    try:
        fp = open(path, 'r')
    except FileNotFoundError:
        raise FileNotFoundError(f'Cannot open {path}')
    else:
        with fp:
            for n,line in enumerate(fp):
                l = line.strip('\n').split(sep)
                if len(l) != fields:
                    raise ValueError(f'{path} has {len(l)} fields on line {n+1} but expected {fields}')
                else:
                    if n == 0 and header:
                        continue
                    else:
                        yield tuple(l)


class Repository:
    def __init__(self, n):
        self.directory = n
        self._students = {}
        self._instructors = {}
        self._analyze_files()

    def _analyze_files(self):
        """ populate the summarized data and update students and instructors"""
        for s in file_reading_gen(os.path.join(self.directory, 'students.txt'), 3, '\t'):
            if s[0].strip()=='':
                raise ValueError('CWID cannot be None')
            else:
                new_student = Student(s[0], s[1], s[2])
                self._students[s[0]] = new_student

        for s in file_reading_gen(os.path.join(self.directory, 'instructors.txt'), 3, '\t'):
            if s[0].strip()=='':
                raise ValueError('CWID cannot be None')
            else:
                new_prof = Instructor(s[0], s[1], s[2])
                self._instructors[s[0]] = new_prof

        for s in file_reading_gen(os.path.join(self.directory, 'grades.txt'), 4, '\t'):
            if s[0].strip()=='' or s[3].strip()=='':
                raise ValueError('CWID cannot be None')
            elif s[0] not in self._students:
                raise ValueError('Student does not exist')
            elif s[3] not in self._instructors:
                raise ValueError('Instructor does not exist')
            else:
                self._students[s[0]].classes_taken[s[1]] = s[2]
                self._instructors[s[3]].classes_taught[s[1]] += 1

    def pretty_print(self):
        """ print out the pretty table of student summary and instructor summary"""
        pts = PrettyTable(field_names=['CWID', 'Name', 'Completed Courses'])
        for key, d in self._students.items():
            pts.add_row([key, d.name, sorted(list(d.classes_taken.keys()))])
        print(pts.get_string(title="Student Summary"))

        pti = PrettyTable(field_names=['CWID', 'Name', 'Dept', 'Courses', 'Students'])
        for key, d in self._instructors.items():
            for k, n in d.classes_taught.items():
                pti.add_row([key, d.name, d.dept, k, n])
        print(pti.get_string(title="Instructor Summary"))


class Student:
    def __init__(self, id, n, m):
        self.cwid = id
        self.name = n
        self.major = m
        self.classes_taken = defaultdict(str)


class Instructor:
    def __init__(self, id, n, d):
        self.cwid = id
        self.name = n
        self.dept = d
        self.classes_taught = defaultdict(int)


def main(d):
    """print a prettytable with a sample directory."""
    r = Repository(d)
    r.pretty_print()
