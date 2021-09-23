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
from sirena.utils import (
    generate_filepaths,
    get_subdirectories,
    get_filepaths_from_directory
)


class InfoLog:
    """Information log."""

    missing_stations = []

    def __init__(self, station=None):
        """Initialize."""
        if station:
            self.missing_stations.append(station)

    @classmethod
    def append_missing_station(cls, station):
        """Append info."""
        return cls('\t-' + station)

    @classmethod
    def print_missing_stations(cls):
        """Print info."""
        print('Missing stations:')
        print('\n'.join(cls.missing_stations))

    @classmethod
    def reset(cls):
        """Reset list."""
        cls.missing_stations = []


class ErrorCapturing:
    """Error log."""

    errors = []

    def __init__(self, error=None):
        """Initialize."""
        if error:
            self.errors.append(error)

    @classmethod
    def append_error(cls, **error_kwargs):
        """Append error."""
        string = '\t-' + ', '.join(
            (': '.join((key, str(item))) for key, item in error_kwargs.items())
        )
        return cls(string)

    @classmethod
    def print_errors(cls):
        """Print error."""
        print('Errors:')
        print('\n'.join(cls.errors))

    @classmethod
    def reset(cls):
        """Reset list."""
        cls.errors = []


class Settings:
    """Class to hold information from etc settings files."""

    def __init__(self):
        """Initialize."""
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
        self._load_local_info()

    def __setattr__(self, name, value):
        """Define the setattr for object self.

        Special management of paths.
        """
        if name == 'dir_path':
            pass
        # elif isinstance(value, str) and 'path' in name:
        #     name = os.path.join(self.base_directory, value)
        elif isinstance(value, dict) and 'paths' in name:
            self._check_for_paths(value)
        super().__setattr__(name, value)

    def _check_for_paths(self, dictionary):
        """Look for paths in the given dictionary.

        Since default path settings are set to sirena base folder
        we need to add that base folder to all paths.
        """
        for item, value in dictionary.items():
            if isinstance(value, dict):
                self._check_for_paths(value)
            elif 'path' in item:
                dictionary[item] = os.path.join(self.base_directory, value)

    def _load_settings(self, etc_path):
        """Load settings files.

        Loading all yaml files from etc directory.
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
        """Add base dir to paths."""
        for key in self.settings['paths']:
            if key == 'server_info_path':
                continue
            self.settings['paths'][key] = Path(
                self.base_directory).joinpath(self.settings['paths'][key])

    def _load_local_info(self):
        """Load local info."""
        if not os.path.exists(self.settings['paths'].get('server_info_path')):
            raise ImportError(
                'Could not find any settings paths. You need to copy srv.json into the folder: {} '
                '(or set your own local folder of your choosing). You can get this file from JJ.'
                ''.format(self.settings['paths'].get('server_info_path'))
            )

        settings = JSONreader().load_json(
            config_files=[self.settings['paths'].get('server_info_path')],
            return_dict=True
        )
        self.set_attributes(self, **settings)

    def set_reader(self, reader):
        """Set reader.

        Includes reader kwargs as attributes to self.
        """
        self.set_attributes(self, **self.readers[reader])

    def set_writer(self, writer=None):
        """Set writer.

        Includes writer kwargs as attributes to self.
        """
        self.set_attributes(self, **self.writers.get(writer))

    def _set_sub_object(self, attr, value):
        """Update attribute."""
        setattr(self, attr, value)

    @staticmethod
    def set_attributes(obj, **kwargs):
        """Set attributes.

        With the possibility to add attributes to an object
        which is not self.
        """
        # TODO Move to utils?
        for key, value in kwargs.items():
            setattr(obj, key, value)
