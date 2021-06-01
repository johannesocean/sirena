# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2021-05-28 11:04
@author: johannes
"""
import os
import time
from sirena.session import Session
from sirena.plotting.widgets import Plot


session_obj = Session(
    reader='wiski',
    station_source='samsa',
    start_time='1700-01-01',
    end_time='2020-12-31',
)

selected_dataset = 'annual_RH2000'
print('Read data..')
start_time = time.time()
dfs = session_obj.read(
    all_stations=True,
    datasets=[selected_dataset],
)
print("Data extracted--%.3f sec" % (time.time() - start_time))

stats = session_obj.get_statistics(
    dfs[selected_dataset],
    stats_for_year=None,
    parameter='RH2000_Year.Mean'
)

session_obj.store_statistics(stats)


session_obj.write('xlsx_template')
