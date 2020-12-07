# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2020-04-07 10:54

@author: a002028

"""
import os
import yaml
from sirena import utils


class YAMLreader(dict):
    """
    """
    def load_yaml(self, config_files, file_names_as_key=False, return_dict=False):
        """

        :param config_files: list of file paths
        :param file_names_as_key: False | True
        :param return_dict: False | True
        :return: Dictionary with loaded files specifications
        """
        for config_file in config_files:
            with open(config_file, encoding='utf8') as fd:
                file = yaml.load(fd, Loader=yaml.FullLoader)
                if file_names_as_key:
                    file_name = self.get_file_name(config_file)
                    self[file_name] = file
                else:
                    self = utils.recursive_dict_update(self, file)

        if return_dict:
            return self

    @staticmethod
    def get_file_name(file_path):
        """
        :param file_path: str, complete path to file
        :return: filename without extension
        """
        return os.path.splitext(os.path.basename(file_path))[0]
