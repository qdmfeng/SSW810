"""
SSW810 Homework 10
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
            for n, line in enumerate(fp):
                l = line.strip('\n').split(sep)
                if len(l) != fields:
                    raise ValueError(f'{path} has {len(l)} fields on line {n + 1} but expected {fields}')
                else:
                    if n == 0 and header:
                        continue
                    else:
                        yield tuple(l)


class Repository:
    def __init__(self, n):
        self.directory = n
        self._students = {}
        self._major = {}
        self._instructors = {}
        self._analyze_files()

    def _analyze_files(self):
        """ populate the summarized data and update students, instructors and majors"""
        for s in file_reading_gen(os.path.join(self.directory, 'majors.txt'), 3, '\t', True):
            if any(i.strip() == '' for i in s):
                raise ValueError('Invalid data in majors.txt')
            else:
                if s[0] not in self._major:
                    self._major[s[0]] = Major(s[0])
                if s[1] == 'E':
                    self._major[s[0]].e_courses.append(s[2])
                elif s[1] == 'R':
                    self._major[s[0]].r_courses.append(s[2])

        for s in file_reading_gen(os.path.join(self.directory, 'students.txt'), 3, ';', True):
            if s[0].strip() == '':
                raise ValueError('CWID cannot be None')
            elif s[2] not in self._major:
                raise ValueError('Student\'s major does not exist')
            else:
                new_student = Student(s[0], s[1], self._major[s[2]])
                self._students[s[0]] = new_student

        for s in file_reading_gen(os.path.join(self.directory, 'instructors.txt'), 3, '|', True):
            if s[0].strip() == '':
                raise ValueError('CWID cannot be None')
            else:
                new_prof = Instructor(s[0], s[1], s[2])
                self._instructors[s[0]] = new_prof

        for s in file_reading_gen(os.path.join(self.directory, 'grades.txt'), 4, '|', True):
            if s[0].strip() == '' or s[3].strip() == '':
                raise ValueError('CWID cannot be None')
            elif s[0] not in self._students:
                raise ValueError('Student does not exist')
            elif s[3] not in self._instructors:
                raise ValueError('Instructor does not exist')
            else:
                self._students[s[0]].classes_taken[s[1]] = s[2]
                self._instructors[s[3]].classes_taught[s[1]] += 1

        for st in self._students.values():
            st.update_status()

    def pretty_print(self):
        """ print out the pretty table of student summary, instructor summary and major summary"""
        pts = PrettyTable(
            field_names=['CWID', 'Name', 'Major', 'Completed Courses', 'Remaining Required', 'Remaining Electives'])
        for key, d in self._students.items():
            pts.add_row([key, d.name, d.major.name, sorted(list(d.classes_taken.keys())), sorted(d.classes_remain['R']),
                         sorted(d.classes_remain['E'])])
        print(pts.get_string(title="Student Summary"))

        pti = PrettyTable(field_names=['CWID', 'Name', 'Dept', 'Courses', 'Students'])
        for key, d in self._instructors.items():
            for k, n in d.classes_taught.items():
                pti.add_row([key, d.name, d.dept, k, n])
        print(pti.get_string(title="Instructor Summary"))

        ptm = PrettyTable(field_names=['Dept', 'Required', 'Electives'])
        for key, d in self._major.items():
            ptm.add_row([key, d.r_courses, d.e_courses])
        print(ptm.get_string(title="Major Summary"))


class Student:
    def __init__(self, id, n, m):
        self.cwid = id
        self.name = n
        self.major = m
        self.classes_taken = defaultdict(str)
        self.classes_remain = defaultdict(list)

    def update_status(self):
        """update students classes_remain based on classes_taken"""
        valid_grade = ['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C']
        for c in self.major.r_courses:
            if c not in self.classes_taken or self.classes_taken[c] not in valid_grade:
                self.classes_remain['R'].append(c)
        for c in self.major.e_courses:
            if c not in self.classes_taken or self.classes_taken[c] not in valid_grade:
                self.classes_remain['E'].append(c)


class Major:
    def __init__(self, n):
        self.name = n
        self.r_courses = []
        self.e_courses = []


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
