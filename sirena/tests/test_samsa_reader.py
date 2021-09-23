# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute.
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2020-10-16 15:38

@author: a002028
"""
from sirena.session import Session


if __name__ == '__main__':
    s = Session(
        reader='wiski',
        station_source='samsa',
        start_time='1700-01-01',
        end_time='2019-12-31',
    )

    for sname in s.settings.stations.keys():
        if sname not in s.stations.keys():
            print(sname)
