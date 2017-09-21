__author__ = 'andrewlaird'

import pandas

class


def get_emp_data():
    return pandas.read_csv('~/Desktop/Britannia/employee_prefs.csv')


def get_tour_data():
    return pandas.read_csv('~/Desktop/Britannia/tour_schedule_durations.csv')


def get_tours_by_day(tour_data, day):

    return tour_data[tour_data['Day'] == day]['Tours']


def get_tours(tour_data, days, timestamps, bound='Start'):

    day_vals = {'Sunday': 0, 'Monday': 1440, 'Tuesday': 2880, 'Wednesday': 4320, 'Thursday': 5760,
               'Friday': 7200, 'Saturday': 8640}

    dfs = []
    for day in days:
        for timestamp in timestamps:

            timestamp += day_vals[day]

            dfs.append(tour_data[(tour_data['Day'] == day) & (tour_data[bound] == timestamp)].copy())

    return pandas.concat(dfs)


def get_tour_range(tour_data, days, start=0, stop=1440, bound='Start'):

    day_vals = {'Sunday': 0, 'Monday': 1440, 'Tuesday': 2880, 'Wednesday': 4320, 'Thursday': 5760,
               'Friday': 7200, 'Saturday': 8640}

    dfs = []
    for day in days:

        temp_start = start + day_vals[day]
        temp_stop = stop + day_vals[day]

        dfs.append(tour_data[(tour_data[bound] >= temp_start) & (tour_data[bound] < temp_stop)])

    return pandas.concat(dfs)


# Get an individual tour based on it's unique tour id
def get_tour_by_id(tour_data, tour_id):

    return tour_data[tour_data['Tours'] == tour_id]

print(get_tour_data())





