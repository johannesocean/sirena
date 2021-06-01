# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2021-06-01 17:57
@author: johannes
"""
from win32com import client
from sirena.writers.writer import WriterBase


class PDFWriter(WriterBase):
    def __init__(self, *args, **kwargs):
        super(PDFWriter, self).__init__()

    def write(self):
        # TODO Fix setup in standard structure
        input_file = r'C:\Utveckling\sirena\sirena\export\mwreg_sirena.xlsx'
        output_file = input_file.replace('.xlsx', '.pdf')

        app = client.DispatchEx("Excel.Application")
        app.Interactive = False
        app.Visible = False
        Workbook = app.Workbooks.Open(input_file)
        Workbook.WorkSheets('mwreg').Select()
        try:
            Workbook.ActiveSheet.ExportAsFixedFormat(0, output_file)
        except Exception as e:
            print(
                "Failed to convert in PDF format. Please confirm environment meets all the requirements and try again")
            print(str(e))
        finally:
            Workbook.Close()
            app.Quit()
            print('Excel.Application shutdown')
