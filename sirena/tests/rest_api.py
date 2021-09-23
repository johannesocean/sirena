# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute.
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2020-10-01 12:34

@author: a002028
"""
import requests
# import urllib


def get_periods(src, dest):
    """Get periods."""
    # src_enc = urllib.parse.quote_plus(src)
    # dest_enc = urllib.parse.quote_plus(dest)
    cookies = None
    try:
        # FIXME se wiki
        url_connect = None
        response_connect = requests.get(url_connect)
        cookies = response_connect.cookies
        # FIXME se wiki
        url_periods = None
        headers = {'Accept': 'application/json'}
        response_periods = requests.get(url_periods, cookies=cookies, headers=headers)
        if not response_periods.ok:
            raise Exception('could not get data')
        periods = response_periods.json()
        for period in periods:
            print(period['validFrom'])
            if 'validUntil' in period:
                print(period['validUntil']),
            print(period['rating']['name'])
    finally:
        if cookies is not None:
            # FIXME se wiki
            url_close = None
            requests.put(url_close, cookies=cookies)
