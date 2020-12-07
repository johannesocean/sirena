# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2020-04-07 13:00

@author: a002028

"""
from abc import ABC

import time
import numpy as np
import pandas as pd
import datetime as dt


class Frame(pd.DataFrame, ABC):
    """
    Stores data from one, and only one, station.

    We intend to insert information from the WIKSI database
    """

    # datetime start date (timestamp.millisecond = 0) https://docs.python.org/3.3/library/datetime.html
    # time before this timestamp counts as negative milliseconds
    dt_start = dt.datetime(1970, 1, 1)

    @property
    def _constructor(self):
        """
        Constructor for Frame, overides method in pd.DataFrame
        :return: Frame
        """
        return Frame

    def convert_formats(self):
        """

        :return:
        """
        self['timestamp'] = self['timestamp'].apply(lambda x: self.dt_start + dt.timedelta(milliseconds=float(x)))
        self[self.data_columns] = self[self.data_columns].astype(float)

    def exclude_flagged_data(self, q_flags=None):
        """
        By default we exclude values flagged with:
        3 (160) Probably bad
        4 (220) Bad
        8 (82) Interpolated
        ..found flag 255, presumably this indicates a bad value
        """
        q_flags = q_flags or ['3', '4', '8', '82', '160', '220', '255']

        # qf_boolean = self['quality'].isin(q_flags)
        # self.drop(self[qf_boolean].index, inplace=True)

        for qf_column in self.quality_flag_columns:
            qf_boolean = self[qf_column].isin(q_flags)
            self.loc[qf_boolean, qf_column.replace('Q_', '')] = np.nan

    @property
    def data_columns(self):
        cols = []
        for c in self.columns:
            if c != 'timestamp' and not c.startswith('Q_'):
                cols.append(c)
        return cols

    @property
    def quality_flag_columns(self):
        cols = []
        for c in self.columns:
            if c.startswith('Q_'):
                cols.append(c)
        return cols


class DataFrames(dict):
    """
    Stores information for multiple stations.
    Use station name as key in this dictionary of Frame()-objects
    """
    def append_new_frame(self, **kwargs):
        """
        :param kwargs:
        :return:
        """
        name = kwargs.get('name')
        data = kwargs.get('data')
        if name:
            # print('New data added for {}'.format(name))
            self.setdefault(name, Frame(data, columns=kwargs.get('columns')))
            self[name].convert_formats()
            self[name].exclude_flagged_data()
