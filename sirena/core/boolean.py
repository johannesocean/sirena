# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2020-04-07 10:35

@author: a002028

"""


class BooleanBase:
    """

    """
    def __init__(self):
        super().__init__()
        self.data = None
        self._boolean = True

    def boolean_not_nan(self, param):
        """
        :param param:
        :return: triggers @boolean.setter
        """
        return self.data[param].notna()

    def add_boolean_from_list(self, parameter, value_list):
        """
        :param parameter:
        :param value_list:
        :return: triggers @boolean.setter
        """
        self.boolean = self.data[parameter].isin(value_list)

    def add_boolean_month(self, month):
        """
        :param month: int
        :return: triggers @boolean.setter
        """
        self.boolean = self.data['timestamp'].dt.month == month

    def add_boolean_equal(self, param, value):
        """
        :param param:
        :param value:
        :return: triggers @boolean.setter
        """
        self.boolean = self.data[param] == value

    def add_boolean_less_or_equal(self, param, value):
        """
        :param param: pd.DataFrame column key
        :param value: float/int
        :return: triggers @boolean.setter
        """
        self.boolean = self.data[param] <= value

    def reset_boolean(self):
        """"""
        self._boolean = True

    @property
    def boolean(self):
        """"""
        return self._boolean

    @boolean.setter
    def boolean(self, add_bool):
        """"""
        self._boolean = self._boolean & add_bool
