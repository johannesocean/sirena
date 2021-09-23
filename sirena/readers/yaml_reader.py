# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute.
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2020-04-07 10:54

@author: a002028
"""
import yaml
from sirena import utils


class YAMLreader(dict):
    """Read yaml files."""

    def load_yaml(self, config_files, file_names_as_key=False, return_dict=False):
        """Load yaml file(s).

        Args:
            config_files (list): list of file paths
            file_names_as_key (bool): False | True
            return_dict (bool): False | True
        """
        for config_file in config_files:
            with open(config_file, encoding='utf8') as fd:
                file = yaml.load(fd, Loader=yaml.FullLoader)
                if file_names_as_key:
                    file_name = utils.get_file_name(config_file)
                    self[file_name] = file
                else:
                    self = utils.recursive_dict_update(self, file)

        if return_dict:
            return self
