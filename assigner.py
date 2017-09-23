__author__ = 'andrewlaird'

import pulp
import duties
import employees
import pandas as pd

emps = employees.Employees('employee_prefs.csv')
tours = duties.Duties('tour_schedule_durations.csv')

# define a weighting function for shifts

test_shift = ('Employee 1', 'Tour 1.1a')
print(tours.get_duty_by_id(test_shift[1])['Date_Start'].dt.date.values[0])


def emp_pref(shift):

    # TODO: Fix these calls
    shift_day = tours.get_duty_by_id(shift[1])['Date_Start'].dt.strftime('%-m/%d/%y').values[0]
    shift_pref = emps.get_emp_by_id(shift[0])[shift_day].values[0]
    am_pm_pref = emps.get_emp_by_id(shift[0])[shift_day + ' time'].values[0]
    am_pm_multiplier = 1

    penalized_shifts_for_am_pref = ['Tour {}.{}'.format(day, tour)
                                    for day in range(1, 8)
                                    for tour in range(16, 19)]
    penalized_shifts_for_pm_pref = ['Tour {}.{}'.format(day, tour)
                                    for day in range(1, 8)
                                    for tour in range(1, 5)]

    if am_pm_pref == 'AM' and shift[1] in penalized_shifts_for_am_pref:
        am_pm_multiplier = .7

    if am_pm_pref == 'PM' and shift[1] in penalized_shifts_for_pm_pref:
        am_pm_multiplier = .7

    return shift_pref * am_pm_multiplier

# create variables for each employee/shift combo
possible_shifts = [(employee, shift)
                   for employee in emps.data['Name']
                   for shift in tours.data['Tours']]

x = pulp.LpVariable.dicts('shift', possible_shifts, lowBound=0, upBound=1, cat=pulp.LpInteger)

# create objective function
britannia_model = pulp.LpProblem('Britannia Scheduling Problem', pulp.LpMaximize)

britannia_model += pulp.lpSum([emp_pref(shift) * x[shift]
                               for shift in possible_shifts])

# define constraints
dates = tours.data['Date_Start'].dt.date.unique()

# No more than 4 tours per day
for date in dates:
    for employee in emps.data['Name']:
        britannia_model += pulp.lpSum([x[shift]
                                       for shift in [(employee, tour)
                                       for tour in tours.get_duties(dates=[date])['Tours']]]) <= 4

# No more than 17 tours per week
for employee in emps.data['Name']:
    britannia_model += pulp.lpSum([x[shift]
                                   for shift in [(employee, tour)
                                   for tour in tours.data['Tours']]]) <= 17

# No more than 2 employees can work the opening shift ///THIS HAS NO EFFECT
for date in dates:
    britannia_model += 1 <= pulp.lpSum([x[shift] for shift in [(employee, tour)
                                        for employee in emps.data['Name']
                                        for tour in tours.get_duties(dates=[date],
                                                                     timestamps=['8:30:00'])['Tours']]]) <= 2

# Cannot work shifts in the evening if worked at open
for date in dates:
    for employee in emps.data['Name']:
        for eve_tour_name in tours.get_duties_range(dates=[date], start_time='16:30:00', partial=True)['Tours']:

            shifts = [(employee, tour)
                      for tour in [eve_tour_name] + tours.get_duties(dates=[date],
                                                                     timestamps=['8:00:00'])['Tours'].tolist()]

            britannia_model += pulp.lpSum([x[shift]
                                           for shift in [(employee, tour)
                                           for tour in [eve_tour_name] +
                                           tours.get_duties(dates=[date],
                                                            timestamps=['8:00:00'])['Tours'].tolist()]]) <= 1

# All shifts must be filled by exactly 1 employee
for tour in tours.data['Tours']:
    britannia_model += pulp.lpSum([x[shift]
                                   for shift in [(employee, tour)
                                   for employee in emps.data['Name']]]) == 1

# Cannot work shifts that interfere with other shifts
for date in dates:
    for employee in emps.data['Name']:
        for curr_tour in tours.data['Tours']:

            curr_tour_info = tours.get_duty_by_id(curr_tour)
            curr_tour_start = curr_tour_info['Date_Start'].dt.time.values[0]
            curr_tour_stop = curr_tour_start

            britannia_model += pulp.lpSum([x[shift]
                                          for shift in [(employee, tour)
                                          for tour in tours.get_duties_range(dates=[date],
                                                                             start_time=curr_tour_start,
                                                                             stop_time=curr_tour_stop)]]) <= 1

britannia_model.solve()

print("The choosen shifts are out of a total of %s:" % len(possible_shifts))
for shift in possible_shifts:
    if x[shift].value() == 1.0:
        print(shift)


