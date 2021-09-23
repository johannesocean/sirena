# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute.
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2020-04-28 09:35

@author: a002028
"""
from sirena.session import Session
# import time
# import pandas as pd
# import numpy as np
# import datetime as dt
# from numba import njit
# import yaml


if __name__ == '__main__':
    s = Session(
        reader='wiski',
        station_source='samsa',
        start_time='1700-01-01',
        end_time='2020-12-31',
    )

    # df = pd.read_excel(
    #     r'C:\Utveckling\sirena\sirena\etc\templates\mwreg.xlsx',
    #     sheet_name='stat_uppg',
    #     header=7,
    #     dtype=str,
    #     keep_default_na=True,
    # )
    #
    # data = s.settings.stations
    #
    # for row in df.itertuples():
    #     for statn in data.keys():
    #         if type(row.STATION) != str:
    #             break
    #         if row.STATION.upper().startswith(statn):
    #             data[statn].setdefault('template_name', row.STATION)
    #             data[statn].setdefault('template_number', row.NR)
    #             data[statn].setdefault('template_latitude', row.LATITUD)
    #             data[statn].setdefault('template_longitude', row.LONGITUD)
    #
    # delta = pd.Timedelta('15 minutes')
    #
    #
    # @njit
    # def njit_vectorize(array):
    #     res = np.empty(array.shape)
    #     for i in range(len(array)):
    #         res[i] = array[i] + delta
    #     return res
    #
    #
    # def vectorize(x):
    #     return x + delta
    #
    # df = pd.DataFrame({'time': pd.date_range(start='1700-01-01', end='2020-01-01', freq='D')})
    #
    # start_time = time.time()
    #
    # # df['time'] = df['time'].apply(lambda x: x + delta)
    # df['time'] = np.vectorize(vectorize)(df['time'])
    # # df['time'] = njit_vectorize(df['time'].values)
    #
    # print("Timeit--%.3f sec" % (time.time() - start_time))
