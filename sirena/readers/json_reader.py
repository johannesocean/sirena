# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute.
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2020-04-07 15:41

@author: a002028
"""
import json
import numpy as np
from sirena import utils


class JSONreader(dict):
    """Read json files.

    - Import json
    - Export to json
    - Find dictionary within json file based on a specific key
    - Add elements to dictionary
    - Fill up json/dictionary structure with relevant/desired information
    """

    def load_json(self, config_files=None, return_dict=False):
        """Load json file.

        Array will be either a list of dictionaries or one single dictionary
        depending on what the json file includes.
        """
        if not isinstance(config_files, (list, np.ndarray)):
            config_files = [config_files]

        for config_file in config_files:
            with open(config_file, 'r') as fd:
                self = utils.recursive_dict_update(self, json.load(fd))

        if return_dict:
            return self
