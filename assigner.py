__author__ = 'andrewlaird'

import pulp, duties, employees

employee_data = employees.Employees('employee-prefs.csv')
tour_data = duties.Duties('tour_schedule_durations.csv')

# define a weighting function for shifts


def emp_pref(shift):

    shift_day = tour_data.raw_data[tour_data.raw_data['Tours'] == shift[1]]['Day'].values[0]
    shift_pref = employee_data.raw_data[employee_data.raw_data['Name'] == shift[0]][shift_day].values[0]
    am_pm_pref = employee_data.raw_data[employee_data.raw_data['Name'] == shift[0]][shift_day + ' time'].values[0]
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
                   for employee in employee_data.raw_data['Name']
                   for shift in tour_data.raw_data['Tours']]

x = pulp.LpVariable.dicts('shift', possible_shifts, lowBound=0, upBound=1, cat=pulp.LpInteger)

#create objective function
britannia_model = pulp.LpProblem('Britannia Scheduling Problem', pulp.LpMaximize)

britannia_model += pulp.lpSum([emp_pref(shift) * x[shift]
                               for shift in possible_shifts])

#define constraints
days = tour_data.raw_data['Date_Start'].dt.date.unique()

# No more than 4 tours per day
for day in days:
    for employee in employee_data.raw_data['Name']:
        britannia_model += pulp.lpSum([x[shift]
                                       for shift in [(employee, tour)
                                       for tour in tour_data.get_duties(dates=[day])['Tours']]]) <= 4

# No more than 17 tours per week
for employee in employee_data.raw_data['Name']:
    britannia_model += pulp.lpSum([x[shift]
                                   for shift in [(employee, tour)
                                   for tour in tour_data.raw_data['Tours']]]) <= 17

# No more than 2 employees can work the opening shift ///THIS HAS NO EFFECT
for day in days:
    britannia_model += 1 <= pulp.lpSum([x[shift] for shift in [(employee, tour)
                                        for employee in employee_data.raw_data['Name']
                                        for tour in tour_data.get_duties(dates=[day],
                                                                         timestamps=['8:30:00'])['Tours']]]) <= 2

# Cannot work shifts in the evening if worked at open
for day in days:
    for employee in employee_data.raw_data['Name']:
        for eve_tour_name in tour_data.get_duties_range(dates=[day], [1050, 1080, 1110], bound='Stop')['Tours']:
            britannia_model += pulp.lpSum([x[shift]
                                           for shift in [(employee, tour)
                                           for tour in [eve_tour_name] + tour_data.get_duties(dates=[day],
                                                                                              timestamps=['8:00:00'])['Tours'].tolist()]]) <= 1

# All shifts must be filled by exactly 1 employee
for tour in tour_data.raw_data['Tours']:
    britannia_model += pulp.lpSum([x[shift]
                                   for shift in [(employee, tour)
                                   for employee in employee_data.raw_data['Name']]]) == 1

# Cannot work shifts that interfere with other shifts
for day in days:
    for employee in employee_data.raw_data['Name']:
        for curr_tour in tour_data.raw_data['Tours']:

            curr_tour_info = tour_data.get_duty_by_id(curr_tour)
            curr_tour_start = curr_tour_info['Start']
            curr_tour_stop = curr_tour_info['Stop']

            britannia_model += pulp.lpSum([x[shift]
                                          for shift in [(employee, tour)
                                          for tour in tour_data.get_duties_range(dates=[day],
                                                                                 start_time=curr_tour_start,
                                                                                 stop_time=curr_tour_stop)]]) <= 1

britannia_model.solve()

print("The choosen shifts are out of a total of %s:" % len(possible_shifts))
for shift in possible_shifts:
    if x[shift].value() == 1.0:
        print(shift)


