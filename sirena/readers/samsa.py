# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute.
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2020-10-19 13:53

@author: a002028
"""
import requests


class SAMSABase:
    """Base class for SAMSA reader."""

    def __init__(self):
        """Initialize."""
        super(SAMSABase, self).__init__()
        self.server = None
        self._time_limit = None
        self._filters = None
        self._fields = None

    def update_attributes(self, **kwargs):
        """Update attributes."""
        for attribute, value in kwargs.items():
            setattr(self, attribute, value)

    def get_data(self, *args, **kwargs):
        """Return data."""
        raise NotImplementedError

    @property
    def url(self):
        """Return url."""
        return ''.join((self.server, self.filter_combo))

    @property
    def filter_combo(self):
        """Return filter_combo."""
        return '&'.join((self.time_limit, self.filters, self.fields))

    @property
    def time_limit(self):
        """Return time_limit."""
        return self._time_limit

    @time_limit.setter
    def time_limit(self, value):
        """Set time_limit."""
        self._time_limit = 'timeLimit=' + str(value)

    @property
    def filters(self):
        """Return filters."""
        return self._filters

    @filters.setter
    def filters(self, filter_list):
        """Set filters."""
        self._filters = 'filters=' + ','.join(filter_list)

    @property
    def fields(self):
        """Return fields."""
        return self._fields

    @fields.setter
    def fields(self, field_list):
        """Set fields."""
        self._fields = 'fields=' + ','.join(field_list)


class SAMSAData(SAMSABase):
    """SAMSA reader."""

    def __init__(self):
        """Initialize."""
        super(SAMSAData, self).__init__()

    def get_data(self):
        """Return data."""
        data = None
        try:
            data = requests.get(self.url).json()
            data = data.get('data')
        except requests.exceptions.RequestException as e:
            print('Could not load data.')
            # logging.warning('Could not load data.')
        return data
