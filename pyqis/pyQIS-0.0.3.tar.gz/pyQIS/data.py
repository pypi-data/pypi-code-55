"""
    pyQIS - QIS Server Client implementation in Python 3
    Copyright (C) 2020  Sefa Eyeoglu <contact@scrumplex.net> (https://scrumplex.net)

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""


class Grade:

    def __init__(self, exam_id: str, description: str, grade: float):
        self.exam_id = exam_id
        self.description = description
        self.grade = grade

    def __str__(self):
        return "{} ({}), Grade: {}".format(self.description, self.exam_id, self.grade)

    def __repr__(self):
        return self.__str__()


class Semester:

    def __init__(self, season: str, year: int, grade_average_exam_identifier: str):
        self.season = season
        self.year = year
        self.grades = []
        self.grade_average_exam_identifier = grade_average_exam_identifier

    def __str__(self):
        return "Semester: {}{}".format(self.season, self.year)

    def __repr__(self):
        return self.__str__()

    def grade_average(self) -> (bool, float):
        grade_sum = 0.0
        count = 0
        for grade in self.grades:
            if self.grade_average_exam_identifier in grade.exam_id:
                return False, grade.grade
            if grade.grade is not None:
                grade_sum += grade.grade
                count += 1
        if count == 0:
            return False, 0.0
        return True, round(grade_sum / count, 1)
