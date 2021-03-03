# -*- coding: utf-8 -*-
"""
Created on 2020-04-07 10:28

@author: a002028

"""
import pandas as pd

from sirena.config import Settings, InfoLog, ErrorCapturing
from sirena.core.station import MultiStation
from sirena.core.data_handler import DataFrames
from sirena.core.calculator import Statistics


class Session:
    """
    # TODO:
        1. Beräkning:
        2. csv export av stationer med valid tidsserie

    """
    def __init__(self, reader=None, station_source=None, start_time=None, end_time=None):
        self.settings = Settings()
        self.stations = MultiStation()

        self.readers = self.create_reader_instances(reader=reader)

        self.create_station_source_connection(station_source)

        self.start_time = pd.Timestamp(start_time)
        self.end_time = pd.Timestamp(end_time)

    def create_station_source_connection(self, source):
        """
        :return:
        """
        if source == 'wiski':
            assert 'stations' in self.readers
            reader = self.readers['stations'].get('reader')
            reader.url = self.settings.server_wiski
            self.stations.read_from_wiski_elements(reader.get_data())
        elif source == 'samsa':
            reader_spec = self.settings.readers.get('samsa')
            reader = reader_spec.get('reader')()
            reader.update_attributes(
                server=self.settings.server_samsa,
                **reader_spec.get('attributes')
            )
            self.stations.read_from_samsa_elements(reader.get_data())
        else:
            raise AssertionError('Station source not recognized ({})'.format(source))

        self.update_station_info()

    def update_station_info(self):
        """
        :return:
        """
        for key, item in self.settings.stations.items():
            if key in self.stations:
                self.stations[key].update_attributes(**item)

    def create_reader_instances(self, reader=None):
        """
        Find readers and return their instances
        :param data_sets: iterator of strings
        :param reader: string
        :return: Dictionary, reader instances
        """
        reader_instances = {}
        for dataset, dictionary in self.settings.readers[reader]['datasets'].items():
            data_type = self.settings.readers[reader]['data_types'][dictionary['data_type']]
            reader_instances[dataset] = {'reader': self.load_reader(data_type)}
            for key, item in dictionary.items():
                reader_instances[dataset].setdefault(key, item)

        return reader_instances

    @staticmethod
    def load_reader(data_type):
        """
        :param data_type: Dictionary
        :return: Reader instance
        """
        reader_instance = data_type.get('reader')
        return reader_instance()

    def read(self, **kwargs):
        """"""
        selected_datasets = kwargs.get('datasets') or ['annual_RH2000']
        data_dictionary = {}
        for dataset_setting in selected_datasets:
            reader_container = self.readers[dataset_setting]

            if kwargs.get('all_stations'):
                station_list = self.settings.stations.get('station_list')
            elif kwargs.get('stations'):
                station_list = kwargs.get('stations')
            else:
                raise AssertionError('NO DESIGNATED STATION LIST! {} ?'.format(kwargs.get('stations')))

            datasets = self._read_datasets(
                reader_container,
                station_list
            )
            data_dictionary[dataset_setting] = datasets

        return data_dictionary

    def _read_datasets(self, reader_container, station_list):
        """
        start_date = pd.Timestamp('1700-01-01')
        end_date = pd.Timestamp('2020-12-31')

        reader = s.readers['sealevel']['reader']
        reader.update_attributes(**{'server': server,
                                    'station': int,
                                    'parameter': '',
                                    'channel': '',
                                    'time_window': (start_date, end_date)})
        df = reader.get_data()

        """
        reader = reader_container.get('reader')
        reader.update_attributes(
            server=self.settings.server_wiski,
            parameter=reader_container.get('parameter'),
            time_window=self.time_window
        )

        dfs = DataFrames()
        for station in station_list:
            if not self.stations.get(station):
                InfoLog.append_missing_station(station)
                continue

            reader.update_attributes(station=self.stations[station].number)

            df = pd.DataFrame()
            for channel in reader_container.get('channels'):
                reader.update_attributes(channel=channel)
                try:
                    #TODO set timestamp as index?
                    df_channel = reader.get_data(as_dataframe=True)
                    if df.empty:
                        df = df_channel
                    else:
                        df = pd.merge(df, df_channel, how='inner', on='timestamp')
                except BaseException as excep:
                    ErrorCapturing.append_error(
                        Error=excep,
                        Station=station,
                        Parameter=reader.parameter,
                        Channel=reader.channel
                    )
            if not df.empty:
                dfs.append_new_frame(
                    name=station,
                    data=df,
                    columns=df.columns
                )

        return dfs

    def get_statistics(self, dataframes, parameter=None, stats_for_year=None):
        """

        :param dataframes:
        :param stats_for_year:
        :return:
        """
        stat_obj = Statistics(calculation_year=stats_for_year)

        for key, df in dataframes.items():
            stat_obj.append_new_station(
                name=key,
                station_attr=self.settings.stations.get(key),
                data=df,
                parameter=parameter
            )
        return stat_obj

    @property
    def time_window(self):
        """
        :return: tuple of start- and end-time
        """
        return self.start_time, self.end_time
