# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute.
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2020-04-17 09:50

@author: a002028
"""
from bokeh.models import Button, FileInput, CustomJS, TextInput
from bokeh.layouts import row, column, Spacer
from bokeh.events import ButtonClick
from functools import partial


# FIXME We need to clean this shit up! No parameter hardcoding! Tidy up!!!

def get_download_widget():
    """Return Button widget."""
    button = Button(label="Download selected data", button_type="success", width=40)
    return button


def get_file_widget():
    """Return FileInput widget."""
    # button_input = FileInput(accept=".csv,.txt")
    button_input = FileInput()

    return button_input


class TextInputWidget(dict):
    """Widget to handle text layout."""

    def __init__(self, **kwargs):
        """Initialize."""
        super(TextInputWidget, self).__init__()
        self['name'] = kwargs.get('name')

        self['text_obj'] = TextInput(value="None", title=kwargs.get('label') or "Label:", width=300)
        self['text_obj'].js_on_change("value", CustomJS(code="""
            console.log('text_input: value=' + this.value, this.toString())
        """))
        self['button'] = Button(label=kwargs.get('button_label') or 'Save',
                                width=50, button_type='success')
        self['button'].on_event(ButtonClick, partial(self.callback, text=self['text_obj']))

        self.layout = row([self['text_obj'], column([Spacer(height=18), self['button']])])

    @staticmethod
    def callback(text=None):
        """Print text."""
        print('text.value', text.value)


def station_callback(plot_source=None, data_source=None, station_source=None,
                     text_source=None, text_input_list=None):
    """JS callback for stations in GUI."""
    code = """
    // Get data from python dictionary
    var selected_data = {
        year: [], 
        iv_l: [], 
        iv_u: [], 
        ci_l: [], 
        ci_u: [], 
        running_mean: [], 
        fitted_values: [], 
        additional_regression: [], 
        data_values: []
    };
    var data = source;
    var text_input_list = text_input_list;

    // Get indices array of all selected items (in this case stations on the map)
    var selected_index = station_source.selected.indices[0];
    var station = station_source.data.STATN[selected_index];
    var text_values = {
        ref_value_2000: station_source.data.ref_value_2000[selected_index].toString(), 
        absolute_landlift: station_source.data.absolute_landlift[selected_index].toString(), 
        k_value: station_source.data.k_value[selected_index].toString()
    };

    // console.log('selected station', station)
    var txt_name;
    for (var i = 0; i < text_input_list.length; i++) {
        txt_name = text_input_list[i].name;
        if (txt_name in text_values) {
            text_input_list[i]['text_obj'].value = text_values[txt_name];
        }
    }

    var year_val, iv_l_val, iv_u_val, ci_l_val, ci_u_val, runmean_val, fitted_val, data_val;
    for (var i = 0; i < data[station].year.length; i++) {
        year_val = data[station].year[i];
        iv_l_val = data[station].iv_l[i];
        iv_u_val = data[station].iv_u[i];
        ci_l_val = data[station].ci_l[i];
        ci_u_val = data[station].ci_u[i];
        runmean_val = data[station].running_mean[i];
        fitted_val = data[station].fitted_values[i];
        data_val = data[station].data_values[i];

        selected_data.year.push(year_val);
        selected_data.iv_l.push(iv_l_val);
        selected_data.iv_u.push(iv_u_val);
        selected_data.ci_l.push(ci_l_val);
        selected_data.ci_u.push(ci_u_val);
        selected_data.running_mean.push(runmean_val);
        selected_data.fitted_values.push(fitted_val);
        selected_data.additional_regression.push(fitted_val);
        selected_data.data_values.push(data_val);
    }
    //console.log('data[station].text', data[station].text)

    plot_source.data = selected_data;
    text_source.text = data[station].text;
    """
    # Create a CustomJS callback with the code and the data
    return CustomJS(args={'source': data_source,
                          'plot_source': plot_source,
                          'station_source': station_source,
                          'text_source': text_source,
                          'text_input_list': text_input_list,
                          },
                    code=code)


def slider_callback(source=None):
    """JS callback for sliders in GUI."""
    code = """
    var data = source.data;
    var selected_year = cb_obj.value;
    var x_values = data['year'];
    var y_values = data['data_values'];

    //console.log('y_values', y_values)

    var sum_x = 0;
    var sum_y = 0;
    var sum_xy = 0;
    var sum_xx = 0;
    var count = 0;

    var x_reg = 0;
    var y_reg = 0;
    var values_length = x_values.length;

    for (var i = 0; i < values_length; i++) {
        x_reg = x_values[i];
        if (x_reg >= selected_year) {
            y_reg = y_values[i];
            sum_x += x_reg;
            sum_y += y_reg;
            sum_xx += x_reg*x_reg;
            sum_xy += x_reg*y_reg;
            count++;
        }
    }

    /* Calculate m and b for the formular:
     * y = x * m + b
     */
    var m = (count*sum_xy - sum_x*sum_y) / (count*sum_xx - sum_x*sum_x);
    var b = (sum_y/count) - (m*sum_x)/count;
    //console.log('m', m)
    //console.log('b', b)
    var result_values_y = [];
    var x = 0;
    var y = 0;
    for (var i = 0; i < values_length; i++) {
        x = x_values[i];
        //console.log('x', x)
        y = x * m + b;
        result_values_y.push(y);
    }

    //console.log('result_values_y', result_values_y)

    data['additional_regression'] = result_values_y;
    source.change.emit();
    """
    return CustomJS(args=dict(source=source), code=code)
