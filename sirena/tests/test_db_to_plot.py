# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2020-04-27 12:29

@author: a002028

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

# session_obj.update_station_info()

pp = Plot(
    stations=session_obj.stations,
    statistics=stats,
    output_filename=os.path.join(session_obj.settings.base_directory, "export", "SMISK_VIZ_tst.html")
)

pp.show_plot()
