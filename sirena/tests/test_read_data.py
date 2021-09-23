# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute.
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2020-10-22 14:48

@author: a002028
"""
from sirena.session import Session


if __name__ == '__main__':
    session_obj = Session(
        reader='wiski',
        station_source='samsa',
        start_time='1700-01-01',
        end_time='2019-12-31',
    )
    example_statn = 'RATAN'
    print('Station attributes: {}'.format(session_obj.stations[example_statn].added_attributes))

    selected_dataset = 'annual_RH2000'
    print('\nRead data.. (~5 seconds)')
    dfs = session_obj.read(
        all_stations=True,
        datasets=[selected_dataset],
    )

    print('\nData loaded for the following stations: {}'.format(list(dfs[selected_dataset])))
    print('\nData example for station: {}\n{}'.format(
        example_statn,
        dfs[selected_dataset][example_statn])
    )
