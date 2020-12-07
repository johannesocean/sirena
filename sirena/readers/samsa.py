# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2020-10-19 13:53

@author: a002028

"""
import requests


class SAMSABase:
    """
    """
    def __init__(self):
        super(SAMSABase, self).__init__()
        self.server = None
        self._time_limit = None
        self._filters = None
        self._fields = None

    def update_attributes(self, **kwargs):
        """
        :param kwargs:
        :return:
        """
        for attribute, value in kwargs.items():
            setattr(self, attribute, value)

    def get_data(self, *args, **kwargs):
        raise NotImplementedError

    @property
    def url(self):
        return ''.join((self.server, self.filter_combo))

    @property
    def filter_combo(self):
        return '&'.join((self.time_limit, self.filters, self.fields))

    @property
    def time_limit(self):
        return self._time_limit

    @time_limit.setter
    def time_limit(self, value):
        self._time_limit = 'timeLimit=' + str(value)

    @property
    def filters(self):
        return self._filters

    @filters.setter
    def filters(self, filter_list):
        self._filters = 'filters=' + ','.join(filter_list)

    @property
    def fields(self):
        return self._fields

    @fields.setter
    def fields(self, field_list):
        self._fields = 'fields=' + ','.join(field_list)


class SAMSAData(SAMSABase):
    """
    """
    def __init__(self):
        super(SAMSAData, self).__init__()

    def get_data(self):
        data = None
        try:
            data = requests.get(self.url).json()
            data = data.get('data')
        except requests.exceptions.RequestException as e:
            print('Could not load data.')
            # logging.warning('Could not load data.')
        return data
