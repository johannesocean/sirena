# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute.
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2020-04-09 17:26

@author: a002028
"""
from bokeh.io import output_notebook
from bokeh.models import ColumnDataSource, Slider, PreText, Circle, TapTool, HoverTool, WheelZoomTool, ResetTool, PanTool, SaveTool,  LassoSelectTool
from bokeh.layouts import grid, row, column
from bokeh.plotting import figure, show, output_file
from bokeh.tile_providers import get_provider, Vendors
import pyproj
from sirena.plotting.callbacks import station_callback, slider_callback, TextInputWidget


def convert_projection(lats, lons):
    """Transform coordinates from one spatial reference system to another.

    From WGS84 --> Google projection
    To find your EPSG check this website: http://spatialreference.org/ref/epsg/.
    """
    project_projection = pyproj.Proj({'init': 'epsg:4326', 'no_defs': True}, preserve_flags=True)  # wgs84
    google_projection = pyproj.Proj({'init': 'epsg:3857', 'no_defs': True}, preserve_flags=True)  # default google projection

    x, y = pyproj.transform(
        project_projection,
        google_projection,
        lons,
        lats
    )
    return x, y


class Plot:
    """Main class for bokeh plotting."""

    def __init__(self, stations=None, statistics=None,
                 output_filename=None, as_output_notebook=False):
        """Initialize."""
        if as_output_notebook:
            output_notebook()
        else:
            output_file(output_filename or "SMISK_VIZ.html")

        self.tile_provider = get_provider(Vendors.CARTODBPOSITRON_RETINA)

        self.statistics = statistics
        self._setup_position_source(stations)
        self._setup_text_inputs()
        self._setup_text_block()
        self._setup_data_source()
        self._setup_plot_source()
        self._setup_slider_regression()
        self._setup_map()
        self.plot_stations()
        self.plot_stats()

    def _setup_plot_source(self):
        """Set bokeh ColumnDataSource for GUI plotting."""
        self.plot_source = ColumnDataSource(
            data=dict(
                year=[],
                iv_l=[],
                iv_u=[],
                ci_l=[],
                ci_u=[],
                fitted_values=[],
                running_mean=[],
                additional_regression=[],
                data_values=[],
            )
        )

    def _setup_position_source(self, stations):
        """Set bokeh ColumnDataSource for stations."""
        position_df = {k: [] for k in ('STATN', 'LATIT', 'LONGI', 'LATIT_DD', 'LONGI_DD', 'ref_value_2000', 'absolute_landlift', 'k_value')}
        if stations:
            for _, statn_obj in stations.items():
                if statn_obj.latitude and statn_obj.longitude and statn_obj.name in self.statistics:
                    position_df['STATN'].append(statn_obj.name)
                    position_df['LATIT'].append(statn_obj.latitude)
                    position_df['LONGI'].append(statn_obj.longitude)
                    position_df['LATIT_DD'].append(str(statn_obj.latitude))
                    position_df['LONGI_DD'].append(str(statn_obj.longitude))
                    position_df['ref_value_2000'].append(statn_obj.ref_value_2000)
                    position_df['absolute_landlift'].append(statn_obj.absolute_landlift)
                    position_df['k_value'].append(statn_obj.k_value)

            xs, ys = convert_projection(position_df['LATIT'], position_df['LONGI'])
            position_df['LONGI'] = xs
            position_df['LATIT'] = ys

        self.position_source = ColumnDataSource(data=position_df)

    def _setup_data_source(self):
        """Set data source data.

        This data is used for plotting.
        """
        self.data_source = {}
        if self.statistics:
            for name, item in self.statistics.items():
                self.data_source[name] = {
                    'year': item.year,
                    'iv_l': item.iv_l,
                    'iv_u': item.iv_u,
                    'ci_l': item.ci_l,
                    'ci_u': item.ci_u,
                    'running_mean': item.running_mean,
                    'fitted_values': item.result.fittedvalues,
                    'data_values': item.data_values,
                    'text': item.summary,
                }

    def _setup_text_inputs(self):
        """Set text objects."""
        self.text_inputs = [
            TextInputWidget(label='Absolute land uplift:', button_label='Save', name='absolute_landlift'),
            TextInputWidget(label='Apparent land uplift:', button_label='Save', name='apparent_landlift'),
            TextInputWidget(label='Ref-value (RH2000):', button_label='Save', name='ref_value_2000'),
            TextInputWidget(label='k-value:', button_label='Save', name='k_value'),
            TextInputWidget(label='Equation:', button_label='Save', name='equation'),
        ]

    def _setup_map(self):
        """Set bokeh map figure."""
        pan = PanTool()
        save = SaveTool()
        tap = TapTool()
        lasso = LassoSelectTool()
        reset = ResetTool()
        wheel = WheelZoomTool()

        tooltips = HoverTool(tooltips=[("Station", "@STATN"),
                                       ("Lat", "@LATIT_DD"),
                                       ("Lon", "@LONGI_DD")])

        # range bounds supplied in web mercator coordinates
        self.map = figure(
            x_range=(0, 4000000),
            y_range=(7100000, 9850000),
            x_axis_type="mercator",
            y_axis_type="mercator",
            sizing_mode='stretch_both',
            tools=[pan, wheel, tap, lasso, tooltips, reset, save], height=300, width=500,
        )

        # self.map.yaxis.axis_label = ' '  # in order to aline y-axis with figure window below
        self.map.toolbar.active_scroll = self.map.select_one(WheelZoomTool)
        self.map.add_tile(self.tile_provider)

        tap.callback = station_callback(
            plot_source=self.plot_source,
            data_source=self.data_source,
            text_source=self.text,
            station_source=self.position_source,
            text_input_list=self.text_inputs,
        )

    def _setup_text_block(self):
        """Set bokeh text object."""
        self.text = PreText(
            text=""" """,
            style={'font-size': '10pt'},
            # width=600,
            height=450,
        )

    def _setup_slider_regression(self):
        """Set bokeh slider object."""
        self.slider = Slider(
            start=1850,
            end=2020,
            value=1850,
            step=1,
            title="Start year (regression test)",
        )
        self.slider.js_on_change('value', slider_callback(source=self.plot_source))

    def plot_stations(self):
        """plot bokeh circles on map-object."""
        renderer = self.map.circle(
            'LONGI', 'LATIT',
            source=self.position_source,
            color="#5BC798",
            line_color="aquamarine",
            size=10,
            alpha=0.7,
        )

        selected_circle = Circle(
            fill_alpha=0.5,
            fill_color="red",
            line_color="aquamarine",
        )
        nonselected_circle = Circle(
            fill_alpha=0.2,
            fill_color="blue",
            line_color="aquamarine",
        )

        renderer.selection_glyph = selected_circle
        renderer.nonselection_glyph = nonselected_circle

    def plot_stats(self):
        """Set statistics plot and add data."""
        self.plot = figure(
            tools="pan,reset,wheel_zoom,lasso_select,save",
            active_drag="lasso_select",
            title="",
            height=550,
            tooltips=[("Year", "@year"), ("Data", "@data_values")],
        )
        self.plot.title.align = 'center'
        self.plot.xaxis.axis_label = 'Year'
        self.plot.xaxis.axis_label_text_font_style = 'bold'
        self.plot.yaxis.axis_label = 'Annual Mean Sealevel'
        self.plot.yaxis.axis_label_text_font_style = 'bold'
        # p.xgrid.grid_line_color = None
        self.plot.ygrid.band_fill_alpha = 0.05
        self.plot.ygrid.band_fill_color = "black"
        # self.plot.toolbar.active_scroll = self.temp.select_one(WheelZoomTool)

        self.plot.line('year', 'data_values', color="blue", line_width=0.5, alpha=0.4, source=self.plot_source, legend_label='Data')
        self.plot.cross('year', 'data_values', color="blue", size=4, alpha=0.5, source=self.plot_source, legend_label='Data')
        self.plot.line('year', 'running_mean', color="purple", line_width=2, alpha=0.5, source=self.plot_source, legend_label='Running mean')
        self.plot.line('year', 'fitted_values', color="black", line_width=1, alpha=0.7, source=self.plot_source, legend_label='OLS')
        self.plot.line('year', 'iv_u', color="orange", line_dash='dashed', line_width=1, alpha=0.5, source=self.plot_source, legend_label='95% prediction interval')
        self.plot.line('year', 'iv_l', color="orange", line_dash='dashed', line_width=1, alpha=0.5, source=self.plot_source, legend_label='95% prediction interval')
        self.plot.line('year', 'ci_u', color="red", line_dash='dashed', line_width=1, alpha=0.7, source=self.plot_source, legend_label='95% confidence interval')
        self.plot.line('year', 'ci_l', color="red", line_dash='dashed', line_width=1, alpha=0.7, source=self.plot_source, legend_label='95% confidence interval')

        self.plot.line('year', 'additional_regression', color="green", line_width=2, alpha=0.5, source=self.plot_source, legend_label='Regression Test')

        self.plot.legend.location = "top_right"
        self.plot.legend.click_policy = "hide"

    def show_plot(self):
        """Show bokeh plot layoyt"""
        l = grid([
            row([
                column([self.map, self.plot, self.slider]),
                column([*[t.layout for t in self.text_inputs], self.text])])],
            sizing_mode='stretch_both')
        show(l)
