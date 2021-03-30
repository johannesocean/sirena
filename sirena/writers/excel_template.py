# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2021-03-29 13:20
@author: johannes
"""
import os
import pandas as pd
import shutil
import openpyxl
from datetime import datetime
from openpyxl import load_workbook


class ExcelTemplateWriter:
    """
    """
    def __init__(self, tmp_path=None, export_path=None):
        self.workbook_template_path = tmp_path
        self.export_path = export_path
        self.template_sheetname = 'mwreg'
        self.workbook = None
        self.file_name = None

        self.sheet_mapping = {
            'date': 'C4',
            'area': 'C9',
            'parameter': 'C10',
            'mean': ['D'+n for n in map(str, range(14, 26))],
            'std': ['E'+n for n in map(str, range(14, 26))],
            'min': ['F'+n for n in map(str, range(14, 26))],
            'max': ['G'+n for n in map(str, range(14, 26))],
        }

    def copy_new_woorkbook(self, file_name):
        file_name = file_name + '.xlsx' if not file_name.endswith('.xlsx') else file_name
        self.file_name = os.path.join(
            self.export_path,
            file_name
        )
        shutil.copyfile(self.workbook_template_path, self.file_name)
        self.workbook = load_workbook(self.file_name)

    def get_new_sheet(self, new_sheet_name):
        ws = self.workbook.copy_worksheet(self.workbook[self.template_sheetname])
        ws.title = new_sheet_name
        return ws

    def insert_data_to_template(self, ws, annual_stats, parameter, area_long_name):
        for sheet_spec, item in self.sheet_mapping.items():
            if sheet_spec == 'parameter':
                ws[item] = '{} ({})'.format(self.parameter_long_names.get(parameter, ''),
                                            self.parameter_units.get(parameter, ''))
            elif sheet_spec == 'area':
                ws[item] = area_long_name
            elif sheet_spec == 'date':
                ws[item] = datetime.now().strftime('%Y-%m-%d')
            else:
                for cell, value in zip(item, annual_stats[parameter+':'+sheet_spec]):
                    ws[cell] = value

    def loop_data_file(self):

        for area_tag, item in self.stats.items():
            annual_stats = item.get('annual')
            area_long_name = self.shape_provider.get_area_long_name(area_tag)
            self.copy_new_woorkbook(area_tag)

            for parameter in self.parameters:
                ws = self.get_new_sheet(parameter)
                self.insert_data_to_template(ws, annual_stats, parameter, area_long_name)
                img = openpyxl.drawing.image.Image('etc/sharkweb_img.png')
                img.anchor = 'D1'
                ws.add_image(img)

            self.workbook.template = False
            self.workbook.save(self.file_name)


if __name__ == '__main__':
    wd = os.path.dirname(os.path.realpath(__file__))
    tmp_path = os.path.join(wd, 'etc', 'templates', 'mwreg.xlsx')
    # export_path = os.path.join(wd, 'export')

    handler = ExcelTemplate(
        tmp_path=tmp_path,
        # export_path=export_path,
    )

