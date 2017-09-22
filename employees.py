__author__ = 'abelromer'

import pandas


class Employees:

    def __init__(self, data_file):
        self.data = pandas.read_csv(data_file)

    def get_emp_by_id(self, emp_id):
        return self.data[self.data['Name'] == emp_id]