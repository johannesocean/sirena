# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute.
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2021-03-29 14:57

@author: johannes
"""
import statsmodels.api as sm


if __name__ == '__main__':
    duncan_prestige = sm.datasets.get_rdataset("Duncan", "carData")
    Y = duncan_prestige.data['income']
    X = duncan_prestige.data['education']
    X = sm.add_constant(X)
    model = sm.OLS(Y, X)
    results = model.fit()
    # results.params
