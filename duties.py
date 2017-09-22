__author__ = 'andrewlaird'

import pandas
from pandas.tseries.offsets import Minute

TEST_DATA_PATH = 'tour_schedule_durations.csv'


class Duties():

    def __init__(self, data_file):
        self.raw_data = pandas.read_csv(data_file, parse_dates=[['Date', 'Start']])

    def get_duties(self, dates=None, timestamps=None, durations=None):

        if dates is None:
            dates = self.raw_data['Date_Start'].dt.date.unique()

        if timestamps is None:
            timestamps = self.raw_data['Date_Start'].dt.time.unique()

        if durations is None:
            durations = self.raw_data['Duration'].unique()

        dfs = []
        for date in dates:
            for timestamp in timestamps:
                datetime_to_match = pandas.to_datetime(str(date) + ' ' + str(timestamp))
                match_datetime = (self.raw_data['Date_Start'] == datetime_to_match)
                for duration in durations:

                    match_duration = (self.raw_data['Duration'] == duration)
                    dfs.append(self.raw_data[match_datetime & match_duration])

        return pandas.concat(dfs)

    def get_tour_range(self, dates=None, start_time=None, stop_time=None):

        if dates is None:
            dates = self.raw_data['Date_Start'].dt.date.unique()

        if start_time is None:
            start_time = self.raw_data['Date_Start'].dt.time.min()

        temp_stop_times = self.raw_data['Date_Start'] + pandas.Series([pandas.Timedelta(minutes=duration) for duration in self.raw_data['Duration']])

        if stop_time is None:
            stop_time = temp_stop_times.dt.time.max()

        dfs = []
        for date in dates:

            start_datetime = pandas.to_datetime(str(date) + ' ' + str(start_time))
            stop_datetime = pandas.to_datetime(str(date) + ' ' + str(stop_time))

            dfs.append(self.raw_data[(self.raw_data['Date_Start'] >= start_datetime) & (temp_stop_times < stop_datetime)])

        return pandas.concat(dfs)


def get_emp_data():
    return pandas.read_csv('~/Desktop/Britannia/employee_prefs.csv')


# Get an individual tour based on it's unique tour id
def get_tour_by_id(tour_data, tour_id):

    return tour_data[tour_data['Tours'] == tour_id]

tour_data = Duties(TEST_DATA_PATH)

print(tour_data.get_tour_range(stop_time='16:15:00'))







