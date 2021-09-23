# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2020-04-08 15:38

@author: a002028

"""
import pandas as pd


class StationBase:
    """Base for Station objects.

    Intends to guide attribute settings from station register (either WISKI or SAMSA)
    """

    def __init__(self):
        """Initialize."""
        super().__init__()
        self.added_attributes = set([])
        self._number = None
        self._start_date = None
        self._end_date = None
        self._latitude = None
        self._longitude = None

    def __setattr__(self, key, value):
        """Set attribute."""
        super().__setattr__(key, value)
        if key != 'added_attributes' and not key.startswith('_'):
            self.added_attributes.add(key)

    @property
    def number(self):
        """Return number."""
        return self._number

    @number.setter
    def number(self, value):
        """Set number."""
        self._number = str(value)

    @property
    def start_date(self):
        """Return start_date."""
        return self._start_date

    @start_date.setter
    def start_date(self, start):
        """Set start_date."""
        if type(start) == pd.Timestamp:
            start = start.isoformat()
        self._start_date = start

    @property
    def end_date(self):
        """Return end_date."""
        return self._end_date

    @end_date.setter
    def end_date(self, end):
        """Set end_date."""
        if type(end) == pd.Timestamp:
            end = end.isoformat()
        self._end_date = end

    @property
    def latitude(self):
        """Return latitude."""
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        """Set latitude."""
        self._latitude = round(float(value), 6)

    @property
    def longitude(self):
        """Return longitude."""
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        """Set longitude."""
        self._longitude = round(float(value), 6)


class Station(StationBase):
    """Stores meta information for one, and only one, station.

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
        """Initialize."""
        super().__init__()

    def update_attributes(self, **kwargs):
        """Update attributes."""
        for attribute, value in kwargs.items():
            setattr(self, attribute, value)


class MultiStation(dict):
    """Stores meta information for multiple stations.

    Uses station name as key in this dictionary of Station()-objects
    """

    def append_new_station(self, **kwargs):
        """Append new station."""
        name = kwargs.get('name')
        if name:
            name = name.upper()
            self.setdefault(name, Station())
            self[name].update_attributes(**kwargs)

    def read_from_wiski_elements(self, wiski_station_element_list):
        """Read element from wiski."""
        for element in wiski_station_element_list:
            self.append_new_station(**{e: v for e, v in element.attributes.items()})

    def read_from_samsa_elements(self, samsa_station_element_list):
        """Read element from samsa."""
        mapping = {
            'stationName': 'name',
            'stationIdentity': 'number',
            'wgs84Latitude': 'latitude',
            'wgs84Longitude': 'longitude',
        }
        samsa_attributes = {
            'referensvarde': 'ref_value_2000'
        }
        for element in samsa_station_element_list:
            d = {}
            for e, v in element.items():
                d[mapping.get(e, e)] = v
                if e == 'attributes':
                    if isinstance(v, list):
                        for attr_dict in v:
                            if attr_dict.get('attributeKey') in samsa_attributes:
                                mapped_key = samsa_attributes.get(attr_dict.get('attributeKey'))
                                d[mapped_key] = float(attr_dict.get('attributeValue'))

            self.append_new_station(**d)
