# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2020-04-07 10:28

@author: a002028

"""
import os
from pathlib import Path
from sirena.readers.yaml_reader import YAMLreader
from sirena.readers.json_reader import JSONreader
from sirena.utils import generate_filepaths, get_subdirectories, get_filepaths_from_directory


class InfoLog:
    """
    We don't intend to initialize this class into an object, hence classmethods
    """
    missing_stations = []

    def __init__(self, station=None):
        if station:
            self.missing_stations.append(station)

    @classmethod
    def append_missing_station(cls, station):
        return cls('\t-' + station)

    @classmethod
    def print_missing_stations(cls):
        print('Missing stations:')
        print('\n'.join(cls.missing_stations))

    @classmethod
    def reset(cls):
        cls.missing_stations = []


class ErrorCapturing:
    """
    We don't intend to initialize this class into an object, hence classmethods
    """
    errors = []

    def __init__(self, error=None):
        if error:
            self.errors.append(error)

    @classmethod
    def append_error(cls, **error_kwargs):
        string = '\t-' + ', '.join((': '.join((key, str(item))) for key, item in error_kwargs.items()))
        return cls(string)

    @classmethod
    def print_errors(cls):
        print('Errors:')
        print('\n'.join(cls.errors))

    @classmethod
    def reset(cls):
        cls.errors = []


class Settings:
    """
    """
    def __init__(self):
        self.server_samsa = None
        self.server_wiski = None
        self.readers = None
        self.writers = None
        self.stations = None
        self.base_directory = os.path.dirname(os.path.realpath(__file__))
        self.export_path = os.path.join(self.base_directory, 'export')
        etc_path = os.path.join(self.base_directory, 'etc')
        self._load_settings(etc_path)
        self._add_base_dir_to_paths()
        self._load_server_info()

    def __setattr__(self, name, value):
        """
        Defines the setattr for object self
        :param name: str
        :param value: any kind
        :return:
        """
        if name == 'dir_path':
            pass
        # elif isinstance(value, str) and 'path' in name:
        #     name = os.path.join(self.base_directory, value)
        elif isinstance(value, dict) and 'paths' in name:
            self._check_for_paths(value)
        super().__setattr__(name, value)

    def _check_for_paths(self, dictionary):
        """
        Since default path settings are set to sirena base folder
        we need to add that base folder to all paths
        :param dictionary: Dictionary with paths as values and keys as items..
        :return: Updates dictionary with local path (self.dir_path)
        """
        for item, value in dictionary.items():
            if isinstance(value, dict):
                self._check_for_paths(value)
            elif 'path' in item:
                dictionary[item] = os.path.join(self.base_directory, value)

    def _load_settings(self, etc_path):
        """
        :param etc_path: str, local path to settings
        :return: Updates attributes of self
        """
        paths = generate_filepaths(etc_path, endswith='.yaml')
        settings = YAMLreader().load_yaml(
            paths,
            file_names_as_key=True,
            return_dict=True
        )
        self.set_attributes(self, **settings)
        subdirectories = get_subdirectories(etc_path)

        for subdir in subdirectories:
            if subdir in ['templates', 'icons']:
                continue
            subdir_path = os.path.join(etc_path, subdir)
            paths = get_filepaths_from_directory(subdir_path)
            sub_settings = YAMLreader().load_yaml(
                paths,
                file_names_as_key=True,
                return_dict=True
            )
            self._check_for_paths(sub_settings)
            self._set_sub_object(subdir, sub_settings)

    def _add_base_dir_to_paths(self):
        for key in self.settings['paths']:
            if key == 'server_info_path':
                continue
            self.settings['paths'][key] = Path(self.base_directory).joinpath(self.settings['paths'][key])

    def _load_server_info(self):
        """
        :return:
        """
        if not os.path.exists(self.settings['paths'].get('server_info_path')):
            raise ImportError(
                'Could not find any settings paths. You need to copy srv.json into the folder: {} '
                '(or set your own local folder of your choosing). You can get this file from JJ.'.format(
                    self.settings['paths'].get('server_info_path')))

        settings = JSONreader().load_json(
            config_files=[self.settings['paths'].get('server_info_path')],
            return_dict=True
        )
        self.set_attributes(self, **settings)

    def set_reader(self, reader):
        """
        :param reader: str
        :return: Includes reader kwargs as attributes to self
        """
        self.set_attributes(self, **self.readers[reader])

    def set_writer(self, writer=None):
        """
        :param writer: str
        :return: Includes writer kwargs as attributes to self
        """
        self.set_attributes(self, **self.writers.get(writer))

    def _set_sub_object(self, attr, value):
        """
        :param attr: str, attribute
        :param value: any kind
        :return: Updates attributes of self
        """
        setattr(self, attr, value)

    @staticmethod
    def set_attributes(obj, **kwargs):
        """
        #TODO Move to utils?
        With the possibility to add attributes to an object which is not 'self'
        :param obj: object
        :param kwargs: Dictionary
        :return: sets attributes to object
        """
        for key, value in kwargs.items():
            setattr(obj, key, value)


if __name__ == '__main__':

    s = Settings()
    inf_log = InfoLog.append_missing_station('dsg')
    inf_log = InfoLog.append_missing_station('3')
    inf_log = InfoLog.append_missing_station('4')
    new = InfoLog()
    print(new.missing_stations)

    InfoLog.print_missing_stations()
