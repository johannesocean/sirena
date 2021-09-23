# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute.
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2020-04-07 10:28

@author: a002028
"""
import os
import numpy as np
from collections import Mapping
from datetime import datetime
import shutil
from decimal import Decimal, ROUND_HALF_UP


def check_path(path):
    """Make directory."""
    if not os.path.exists(path):
        os.makedirs(path)


def convert_string_to_datetime_obj(x, fmt):
    """Return datetime object.

    Args:
        x: can be any kind of date/time related string format
        fmt: format of output
    """
    if type(x) == str:
        return datetime.strptime(x, fmt)
    else:
        return ''


def copyfile(src, dst):
    """Copy file to destination."""
    shutil.copy2(src, dst)


def copytree(src, dst, symlinks=False, ignore=None):
    """Copy fodler tree to destination."""
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)


def create_directory_structure(dictionary, base_path):
    """Create directory based on nested dictionary.

    Args:
        dictionary: Nested dictionary
        base_path: Base folder
    """
    if len(dictionary) and not isinstance(dictionary, str):
        for direc in dictionary:
            if isinstance(direc, str):
                if '.' not in direc:
                    create_directory_structure(dictionary[direc], os.path.join(base_path, direc))
            elif isinstance(direc, dict):
                create_directory_structure(dictionary[direc], os.path.join(base_path, direc))
    else:
        os.makedirs(base_path)


def decdeg_to_decmin(pos: (str, float), string_type=True, decimals=2) -> (str, float):
    """Convert position from degrees and decimal minutes into decimal degrees."""
    pos = float(pos)
    deg = np.floor(pos)
    minute = pos % deg * 60.0
    if string_type:
        if decimals:
            output = ('%%2.%sf'.zfill(7) % decimals % (float(deg) * 100.0 + minute))
        else:
            output = (str(deg * 100.0 + minute))

        if output.index('.') == 3:
            output = '0' + output
    else:
        output = (deg * 100.0 + minute)
    return output


def decmin_to_decdeg(pos, string_type=True, decimals=4):
    """Convert position from decimal degrees into degrees and decimal minutes."""
    pos = float(pos)

    output = np.floor(pos / 100.) + (pos % 100) / 60.
    output = round_value(output, nr_decimals=decimals)
    if string_type:
        return output
    else:
        return float(output)


def find_key(key, dictionary):
    """Find key in nested dictionary.

    Generator to find an element of a specific key.
    Note that a key can occur multiple times in a nested dictionary.
    """
    if isinstance(dictionary, list):

        for d in dictionary:
            for result in find_key(key, d):
                yield result
    else:
        for k, v in dictionary.items():
            if k == key:
                yield v
            elif isinstance(v, dict):
                for result in find_key(key, v):
                    yield result
            elif isinstance(v, list):
                for d in v:
                    for result in find_key(key, d):
                        yield result


def get_file_name(file_path):
    """Return filename without extension."""
    return os.path.splitext(os.path.basename(file_path))[0]


def generate_filepaths(directory, endswith=''):
    """Generate file paths."""
    for path, _, fids in os.walk(directory):
        for f in fids:
            if f.endswith(endswith):
                yield os.path.abspath(os.path.join(path, f))


def get_subdirectories(directory):
    """Return subdirectories in the given path."""
    return [subdir for subdir in os.listdir(directory)
            if os.path.isdir(os.path.join(directory, subdir))]


def get_filepaths_from_directory(directory):
    """Generate file paths."""
    return [os.path.join(directory, fid) for fid in os.listdir(directory)
            if not os.path.isdir(directory + fid)]


def get_datetime(date_string, time_string):
    """Get datetime object for date and time."""
    if ' ' in date_string:
        date_string = date_string.split(' ')[0]
    if len(time_string) == 8:
        return datetime.strptime(date_string + ' ' + time_string, '%Y-%m-%d %H:%M:%S')
    elif len(time_string) == 5:
        return datetime.strptime(date_string + ' ' + time_string, '%Y-%m-%d %H:%M')
    else:
        return None


def get_datetime_now(fmt='%Y-%m-%d %H:%M:%S'):
    """Get datetime object according to the given format for time right NOW."""
    return datetime.now().strftime(fmt)


def get_export_folder():
    """Return path to export folder."""
    date_str = get_datetime_now(fmt='%Y%m%d')
    export_path = os.path.abspath(os.path.join('C:/sirena_exports', date_str))
    if not os.path.isdir(export_path):
        os.makedirs(export_path)
    return export_path


def get_file_list_based_on_suffix(file_list, suffix):
    """Get filenames ending with "suffix"."""
    match_list = []
    for fid in file_list:
        if '~$' in fid:
            # memory prefix when a file is open
            continue
        elif fid.endswith(suffix):
            match_list.append(fid)

    return match_list


def is_sequence(arg):
    """Check if an object is iterable (you can loop over it) and not a string."""
    return not hasattr(arg, "strip") and hasattr(arg, "__iter__")


def recursive_dict_update(d, u):
    """Recursive dictionary update.

    Copied from:
        http://stackoverflow.com/questions/3232943/update-
        value-of-a-nested-dictionary-of-varying-depth
        via satpy
    """
    if isinstance(u, dict):
        for k, v in u.items():
            if isinstance(v, Mapping):
                r = recursive_dict_update(d.get(k, {}), v)
                d[k] = r
                # d.setdefault(k, r)
            else:
                d[k] = u[k]
                # d.setdefault(k, u[k])
    return d


def round_value(value: (str, int, float), nr_decimals=3) -> str:
    """Calculate rounded value."""
    return str(Decimal(str(value)).quantize(Decimal('%%1.%sf' % nr_decimals % 1), rounding=ROUND_HALF_UP))
