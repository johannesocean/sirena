# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2020-04-07 13:01

@author: a002028

"""
import numpy as np
import pandas as pd
from datetime import datetime
import statsmodels.api as sm
from statsmodels.sandbox.regression.predstd import wls_prediction_std
from statsmodels.stats.outliers_influence import summary_table
from sklearn.preprocessing import PolynomialFeatures

from sirena.utils import round_value


class AnnualMeanEquation:
    """
    """
    def __init__(self, *args, **kwargs):
        self.ref_value = kwargs.get('ref_value_2000') or np.nan
        self.k = kwargs.get('k_value') * -1 or np.nan
        self.year = kwargs.get('year') or np.nan

    def __call__(self):
        """
        Reference year for RH2000 is 2000

        calculated_mean__yyyy = ref_value_2000 - k * (yyyy-2000)
        :return:
        """
        self.calculated = self.ref_value - self.k * (self.year - 2000)
        return self.calculated

    @property
    def single_line(self):
        return '-' * 65

    @property
    def dubble_line(self):
        return '='*65

    def get_summary_string(self, summary):
        """
        """
        start_idx = summary.find('* The condition') - 1
        return '\n'.join((
            summary[:start_idx],
            self.calculation_string,
            self.single_line,
            self.equation_string,
            self.dubble_line,
            summary[start_idx+1:]
        ))

    @property
    def equation_string(self):
        """
        """
        return '{} = {} - {} * ({}-2000)'.format(
            round(self.calculated, 3),
            self.ref_value,
            round(self.k, 3),
            self.year
        )

    @property
    def calculation_string(self):
        """
        """
        return 'SMHI calculation:    M_(yyyy) = ref_value_2000 - k * (yyyy-2000)'


class OLSEquation:
    """
    """
    def __init__(self, *args, **kwargs):
        """
        :param args:
        :param kwargs:
        """
        self.df = kwargs.get('data')
        self.parameter = kwargs.get('parameter')
        qf_boolean = self.df[self.parameter].isna()
        if qf_boolean.any():
            self.df.drop(self.df[qf_boolean].index, inplace=True)

    def __call__(self):
        """
        :return:
        """
        res = sm.OLS(
            self.df[self.parameter],
            self.df.loc[:, ['year', 'intercept']],
            hasconst=True
        ).fit()
        return res


class OLSPolynomialRegression:
    """
    Source:
    https://ostwalprasad.github.io/machine-learning/Polynomial-Regression-using-statsmodel.html

    """
    def __init__(self, *args, **kwargs):
        """
        :param args:
        :param kwargs:
        """
        self.df = kwargs.get('data')
        self.parameter = kwargs.get('parameter')
        self.polynomial_degree = kwargs.get('polynomial_degree') or 2
        qf_boolean = self.df[self.parameter].isna()
        if qf_boolean.any():
            self.df.drop(self.df[qf_boolean].index, inplace=True)

    def __call__(self):
        """
        :return:
        """
        x = self.df['year'].values
        y = self.df[self.parameter].values

        x = x[:, np.newaxis]
        y = y[:, np.newaxis]

        polynomial_features = PolynomialFeatures(degree=self.polynomial_degree)
        xp = polynomial_features.fit_transform(x)

        res = sm.OLS(y, xp).fit()

        return res


class CalculatorBase:
    """

    """
    def __init__(self):
        super().__init__()
        self.attributes = set([])

    def __setattr__(self, key, value):
        super().__setattr__(key, value)
        if key != 'attributes' and not key.startswith('_'):
            self.attributes.add(key)

    def update_attributes(self, **kwargs):
        """
        :param kwargs:
        :return:
        """
        for attribute, value in kwargs.items():
            setattr(self, attribute, value)


class Calculator(CalculatorBase):
    """

    """
    def __init__(self, calculation_year=None):
        super().__init__()
        self.calc_year = calculation_year

    @staticmethod
    def calculate_wls_prediction_std(result):
        """
        :return:
            predstd : array_like, standard error of prediction same length as rows of exog
            iv_l : array_like, lower confidence bound
            iv_u : array_like, upper confidence bound
        """
        # predstd, iv_l, iv_u = wls_prediction_std(result)
        return wls_prediction_std(result)

    @staticmethod
    def get_regression_summary(result, conf_int=0.95, columns=None, as_dataframe=False):
        """
        :param result:
        :param conf_int:
        :param as_dataframe:
        :return:
        """
        column_mapper = {
            'Obs': 'obs',
            'Dep Var\nPopulation': 'dep_var_population',
            'Predicted\nValue': 'predicted_value',
            'Std Error\nMean Predict': 'std_error_mean_predict',
            'Mean ci\n95% low': 'mean_ci_lo',
            'Mean ci\n95% upp': 'mean_ci_up',
            'Predict ci\n95% low': 'pred_ci_lo',
            'Predict ci\n95% upp': 'pred_ci_up',
            'Residual': 'residual',
            'Std Error\nResidual': 'std_error_residual',
            'Student\nResidual': 'student_residual',
            "Cook's\nD": 'cooks'
        }
        # columns = columns or ['Mean ci\n95% low', 'Mean ci\n95% upp']
        simple_table, data_table, table_columns = summary_table(result, alpha=conf_int)
        table_columns = [column_mapper.get(c) for c in table_columns]
        if as_dataframe:
            return pd.DataFrame(data_table, columns=table_columns)

    def calculate_running_mean(self, data, parameter):
        """

        :return:
        """
        running_mean = data[parameter].rolling(
            31,
            center=True,
            # min_periods=3,
        ).mean()

        self.update_attributes(running_mean=running_mean)

    def calculate_annual_mean_water_level(self, station_attr):
        """
        :param station_attr:
        :return:
        """
        if station_attr:
            station_attr.setdefault('ref_value_2000', np.nan)
            station_attr.setdefault('k_value', round_value(self.result.params[0]) or None)
            station_attr.setdefault('year', self.calc_year or None)

            am = AnnualMeanEquation(**station_attr)
            res = am()

            self.update_attributes(
                annual_mean=res,
                summary=am.get_summary_string(self.result.summary2().as_text()),
            )

    def calculate_stats(self, data, parameter):
        """
        :param data:
        :return:
        """
        data = data.assign(intercept=1., year=lambda x: x.timestamp.dt.year)

        ols = OLSPolynomialRegression(
            data=data,
            parameter=parameter,
            polynomial_degree=2
        )
        res = ols()

        reg_sum = self.get_regression_summary(
            res,
            conf_int=0.05,
            as_dataframe=True
        )

        self.update_attributes(
            result=res,
            data_values=data[parameter],
            year=data['year'],
            predstd=reg_sum['predicted_value'],
            ci_l=reg_sum['mean_ci_lo'],
            ci_u=reg_sum['mean_ci_up'],
            iv_l=reg_sum['pred_ci_lo'],
            iv_u=reg_sum['pred_ci_up']
        )


class Statistics(dict):
    """
    Dictionary of stations with applied calculations
    """
    def __init__(self, calculation_year=None):
        self.calc_year = calculation_year or datetime.now().year
        print('Calculate annual mean water level for year {}'.format(self.calc_year))

    def append_new_station(self, **kwargs):
        """
        :param kwargs:
        :return:
        """
        name = kwargs.get('name')
        if name:
            print('New station added: {}'.format(name))

            self.setdefault(name, Calculator(calculation_year=self.calc_year))

            self[name].calculate_stats(kwargs.get('data'), kwargs.get('parameter'))

            self[name].calculate_annual_mean_water_level(kwargs.get('station_attr'))

            self[name].calculate_running_mean(kwargs.get('data'), kwargs.get('parameter'))
