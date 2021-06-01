# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2021-06-01 16:12
@author: johannes
"""
from abc import ABC


class WriterBase(ABC):
    def __init__(self, *args, **kwargs):
        super(WriterBase, self).__init__()

    def write(self, *args, **kwargs):
        raise NotImplementedError
