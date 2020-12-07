# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2020-04-08 15:38

@author: a002028

"""
import pandas as pd


class StationBase:
    """
    Base for Station objects.
    Intends to guide attribute settings from station register (either WISKI or SAMSA)
    """
    def __init__(self):
        super().__init__()
        self.attributes = set([])
        self._number = None
        self._start_date = None
        self._end_date = None
        self._latitude = None
        self._longitude = None

    def __setattr__(self, key, value):
        super().__setattr__(key, value)
        if key != 'attributes' and not key.startswith('_'):
            self.attributes.add(key)

    @property
    def number(self):
        return self._number

    @number.setter
    def number(self, value):
        self._number = str(value)

    @property
    def start_date(self):
        return self._start_date

    @start_date.setter
    def start_date(self, start):
        if type(start) == pd.Timestamp:
            start = start.isoformat()
        self._start_date = start

    @property
    def end_date(self):
        return self._end_date

    @end_date.setter
    def end_date(self, end):
        if type(end) == pd.Timestamp:
            end = end.isoformat()
        self._end_date = end

    @property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        self._latitude = round(float(value), 6)

    @property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        self._longitude = round(float(value), 6)


class Station(StationBase):
    """
    Stores meta information for one, and only one, station.

    We intend to insert information from SAMSA (station information database)

    Example of attributes:
    - latitude
    - longitude
    - ref_value_2000
    - absolute_landlift
    - k_value
    - ...

    """
    def __init__(self):
        super().__init__()

    def update_attributes(self, **kwargs):
        """
        :param kwargs:
        :return:
        """
        for attribute, value in kwargs.items():
            setattr(self, attribute, value)


class MultiStation(dict):
    """
    Stores meta information for multiple stations.
    Uses station name as key in this dictionary of Station()-objects
    """
    def append_new_station(self, **kwargs):
        """
        :param kwargs:
        :return:
        """
        name = kwargs.get('name')
        if name:
            name = name.upper()
            self.setdefault(name, Station())
            self[name].update_attributes(**kwargs)

    def read_from_wiski_elements(self, wiski_station_element_list):
        """
        :param wiski_station_element_list:
        :return:
        """
        for element in wiski_station_element_list:
            self.append_new_station(**{e: v for e, v in element.attributes.items()})

    def read_from_samsa_elements(self, samsa_station_element_list):
        """
        :param samsa_station_element_list:
        :return:
        """
        mapping = {
            'stationName': 'name',
            'wgs84Latitude': 'latitude',
            'wgs84Longitude': 'longitude'
        }
        for element in samsa_station_element_list:
            self.append_new_station(**{mapping.get(e, e): v for e, v in element.items()})
