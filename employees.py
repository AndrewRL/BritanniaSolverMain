__author__ = 'abelromer'

import pandas


class Employees:

    def __init__(self, data_file):
        self.data = pandas.read_csv(data_file)



employee_data = Employees('employee_prefs.csv')
print(employee_data.data)
