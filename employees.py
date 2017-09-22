__author__ = 'abelromer'

import pandas

class Employees:

    def __init__(self, data_file):
        self.raw_data = pandas.read_csv(data_file)

    def emp_pref(shift):

        shift_day = tour_data[tour_data['Tours'] == shift[1]]['Day'].values[0]
        shift_pref = employee_data[employee_data['Name'] == shift[0]][shift_day].values[0]
        am_pm_pref = employee_data[employee_data['Name'] == shift[0]][shift_day + ' time'].values[0]
        am_pm_multiplier = 1

        penalized_shifts_for_am_pref = ['Tour {}.{}'.format(day, tour) for day in range(1, 8) for tour in range(16, 19)]
        penalized_shifts_for_pm_pref = ['Tour {}.{}'.format(day, tour) for day in range(1, 8) for tour in range(1, 5)]

        if am_pm_pref == 'AM' and shift[1] in penalized_shifts_for_am_pref:
            am_pm_multiplier = .7

        if am_pm_pref == 'PM' and shift[1] in penalized_shifts_for_pm_pref:
            am_pm_multiplier = .7

        return shift_pref * am_pm_multiplier

employee_data = Employees('employee_prefs.csv')
print(employee_data.raw_data)
