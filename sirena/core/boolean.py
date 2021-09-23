# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute.
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2020-04-07 10:35

@author: a002028
"""


class BooleanBase:
    """Base class for boolean handling."""

    # TODO This class is not used yet.

    def __init__(self):
        """Initialize."""
        super().__init__()
        self.data = None
        self._boolean = True

    def boolean_not_nan(self, param):
        """Add boolean not NaN.

        Triggers @boolean.setter
        """
        return self.data[param].notna()

    def add_boolean_from_list(self, parameter, value_list):
        """Add boolean from list.

        Triggers @boolean.setter
        """
        self.boolean = self.data[parameter].isin(value_list)

    def add_boolean_month(self, month):
        """Add boolean for date = month.

        Triggers @boolean.setter
        """
        self.boolean = self.data['timestamp'].dt.month == month

    def add_boolean_equal(self, param, value):
        """Add boolean for pd.Series == value.

        Triggers @boolean.setter
        """
        self.boolean = self.data[param] == value

    def add_boolean_less_or_equal(self, param, value):
        """Add boolean for pd.Series <= value.

        Triggers @boolean.setter
        """
        self.boolean = self.data[param] <= value

    def reset_boolean(self):
        """Reset boolean."""
        self._boolean = True

    @property
    def boolean(self):
        """Return boolean."""
        return self._boolean

    @boolean.setter
    def boolean(self, add_bool):
        """Set boolean."""
        self._boolean = self._boolean & add_bool
