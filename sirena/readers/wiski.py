# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2020-04-07 12:59

@author: a002028

"""
import pandas as pd

import urllib
import xml.dom.minidom as minidom


class WiskiBase:
    def __init__(self):
        super(WiskiBase, self).__init__()
        self.server = None
        self._station = None
        self._time_window = None
        self.parameter = None
        self.channel = None

    def update_attributes(self, **kwargs):
        """
        :param kwargs:
        :return:
        """
        for attribute, value in kwargs.items():
            setattr(self, attribute, value)

    def get_data(self, *args, **kwargs):
        raise NotImplementedError

    @staticmethod
    def url_combo_join(join_list, join_chr='/'):
        return join_chr.join(join_list)

    @property
    def url(self):
        """
        Example:
        'server/200/' + station + '/' + parameter + '/' + tname + '/?from=' + start + '&to=' + end
        :return:
        """
        return '/'.join([self.server, self.station, self.parameter, self.channel, self.time_window])

    @property
    def station(self):
        return self._station

    @station.setter
    def station(self, value):
        self._station = str(value)

    @property
    def time_window(self):
        return self._time_window

    @time_window.setter
    def time_window(self, start_stop):
        start = start_stop[0]
        end = start_stop[-1]
        if type(start) == pd.Timestamp:
            start = start.isoformat()
        if type(end) == pd.Timestamp:
            end = end.isoformat()
        self._time_window = ''.join(('?from=', start, '&to=', end))

    @property
    def parameter_name(self):
        return '_'.join((self.parameter, self.channel))

    @property
    def qf_name(self):
        return '_'.join(('Q', self.parameter_name))


class Wiski(WiskiBase):
    """

    """
    def __init__(self):
        super(Wiski, self).__init__()

    def get_wiski_record(self):
        result = urllib.request.urlopen(urllib.request.Request(self.url))
        doc = minidom.parse(result)
        return doc.getElementsByTagName("timeseriesValueList")[0].getElementsByTagName("timeseriesvalue")

    def get_data(self, as_dataframe=False):
        data_records = self.get_wiski_record()
        data_out = []
        for element in data_records:
            row_data = [
                element.attributes["timestamp"].value,
                element.childNodes[0].data,
                element.attributes["quality"].value
            ]
            data_out.append(row_data)

        if as_dataframe:
            return pd.DataFrame(data_out, columns=['timestamp', self.parameter_name, self.qf_name])
        else:
            return data_out, ['timestamp', self.parameter_name, self.qf_name]


class WiskiData(Wiski):
    """

    """
    def __init__(self):
        super(Wiski, self).__init__()


class WiskiGeo(Wiski):
    """
    Aimed to store latitude and longitude data.
    Relevant for e.g. FerryBox data.
    If used, we might want to process this data in another fashion than ordinary timeseries..
    """
    def __init__(self):
        super(Wiski, self).__init__()


class WiskiStationRegister:
    """
    """
    def __init__(self, url=None):
        self.url = url

    def get_data(self):
        """
        :return:
        """
        data = None
        try:
            result = urllib.request.urlopen(urllib.request.Request(self.url))
            doc = minidom.parse(result)
            data = doc.getElementsByTagName("station")
        except ValueError as e:
            print('\nWARNING! Could not load data in {} due to exception: {}\n'.format(self.__class__.__name__, e))
        return data


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    # date_list = pd.date_range(start='2019-07-01', end='2019-07-31', freq='1min')
    # date_list = pd.date_range(start='2019-10-01', end='2019-10-28', freq='1min')
    start_date = pd.Timestamp('2019-10-29')
    end_date = pd.Timestamp('2019-10-30')

    wh = Wiski()
    wh.update_attributes(**{'site': 'server',
                            'station': 38055,
                            'parameter': 'PHYC',
                            'channel': 'Cmd',
                            # 'station': 39005,
                            # "parameter": 'RH2000',
                            # 'channel': 'Year.Mean',
                            'time_window': (start_date, end_date)})

    # df[['value', 'latitude', 'longitude']] = df[['value', 'latitude', 'longitude']].astype(np.float)
    # # df = df.reindex(df.time)
    # df = df.set_index('time')
    # df_resampled = df.resample('5min').mean()
