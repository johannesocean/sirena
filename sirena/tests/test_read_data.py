# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2020-10-22 14:48

@author: a002028

"""
import os
import time
from sirena.session import Session
from sirena.plotting.widgets import Plot


session_obj = Session(
    reader='wiski',
    station_source='wiski',
    start_time='1700-01-01',
    end_time='2019-12-31',
)

selected_dataset = 'annual_RH2000'
print('Read data..')
start_time = time.time()
dfs = session_obj.read(
    all_stations=True,
    datasets=[selected_dataset],
)

# session_obj.stations['RATAN']
