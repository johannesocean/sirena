# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2020-04-28 09:35

@author: a002028

"""
import time
import pandas as pd
import numpy as np
import datetime as dt
# from numba import njit


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