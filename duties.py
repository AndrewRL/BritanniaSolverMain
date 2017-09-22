__author__ = 'andrewlaird'

import pandas

TEST_DATA_PATH = 'tour_schedule_durations.csv'


class Duties():

    def __init__(self, data_file):
        self.data = pandas.read_csv(data_file, parse_dates=[['Date', 'Start']])

    def get_duties(self, dates=None, timestamps=None, durations=None):

        if dates is None:
            dates = self.data['Date_Start'].dt.date.unique()

        if timestamps is None:
            timestamps = self.data['Date_Start'].dt.time.unique()

        if durations is None:
            durations = self.data['Duration'].unique()

        dfs = []
        for date in dates:
            for timestamp in timestamps:
                datetime_to_match = pandas.to_datetime(str(date) + ' ' + str(timestamp))
                match_datetime = (self.data['Date_Start'] == datetime_to_match)
                for duration in durations:

                    match_duration = (self.data['Duration'] == duration)
                    dfs.append(self.data[match_datetime & match_duration])

        return pandas.concat(dfs)

    def get_duties_range(self, dates=None, start_time=None, stop_time=None, partial=False):

        if dates is None:
            dates = self.data['Date_Start'].dt.date.unique()

        if start_time is None:
            start_time = self.data['Date_Start'].dt.time.min()

        temp_stop_times = self.data['Date_Start'] + pandas.Series([pandas.Timedelta(minutes=duration)
                                                                       for duration in self.data['Duration']])

        if stop_time is None:
            stop_time = temp_stop_times.dt.time.max()

        dfs = []

        for date in dates:

            start_datetime = pandas.to_datetime(str(date) + ' ' + str(start_time))
            stop_datetime = pandas.to_datetime(str(date) + ' ' + str(stop_time))

            if partial is True:

                dfs.append(self.data[(temp_stop_times >= start_datetime) & (temp_stop_times < stop_datetime)])
                dfs.append(self.data[(self.data['Date_Start'] >= start_datetime) & (self.data['Date_Start'] < stop_datetime)])

            match_start_time = (self.data['Date_Start'] >= start_datetime)
            match_stop_time = (temp_stop_times < stop_datetime)

            dfs.append(self.data[match_start_time & match_stop_time])

        return pandas.concat(dfs).drop_duplicates()

    def get_duty_by_id(self, tour_id):

        return self.data[self.data['Tours'] == tour_id]


tour_data = Duties(TEST_DATA_PATH)

print(tour_data.get_duty_by_id('Tour 1.4'))







