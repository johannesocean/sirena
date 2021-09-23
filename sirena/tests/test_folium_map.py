# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute.
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2020-10-16 15:55

@author: a002028
"""
import folium
from folium.plugins import MarkerCluster


def get_html_string_format(*args):
    s = '<b>'
    for a in args:
        new_line = a + ': %s<br>'
        s += new_line
    s += '</b>'
    return s


class Map:
    """Map."""

    def __init__(self, **kwargs):
        """Initialize."""
        for key, item in kwargs.items():
            setattr(self, key, item)

        self.map = folium.Map(
            location=[61.75, 19.45],
            zoom_start=5,
            tiles='cartodbpositron',
        )
        self.marker_tag_attributes = kwargs.get('marker_tag_attributes') or {
            'stationName': 'stationName',
            'stationIdentityTypeKey': 'stationIdentityTypeKey',
            'wgs84Latitude': 'wgs84Latitude',
            'wgs84Longitude': 'wgs84Longitude'
        }
        self.html_fmt = get_html_string_format(*(self.marker_tag_attributes.get(key)
                                                 for key in self.marker_tag_attributes))

    def add_to_map(self, list_obj):
        """Add map to layer controller."""
        self.add_markers_as_cluster(list_obj)
        folium.LayerControl().add_to(self.map)

    def write(self, file_path, list_obj):
        """Write."""
        self.add_to_map(list_obj)

        self._write(file_path)

    def _write(self, file_path):
        """Save map to file."""
        self.map.save(file_path)

    def add_markers_as_cluster(self, stations_list):
        """Add group to cluster."""
        fg = self.get_group(
            name='stations',
            add_to_map=True,
            return_group=True
        )

        mc = MarkerCluster()

        for statn_dict in stations_list:
            if statn_dict.get('stationName') \
                    and statn_dict.get('wgs84Latitude') \
                    and statn_dict.get('wgs84Longitude'):
                html_obj = self.get_html_object(statn_dict)
                popup = self.get_popup(html_obj)
                marker = self.get_marker(
                    [statn_dict.get('wgs84Latitude'), statn_dict.get('wgs84Longitude')],
                    popup=popup,
                    icon=folium.Icon(
                        color='blue'
                        if statn_dict.get('stationIdentityTypeKey') == 'oceanografisktNummer'
                        else 'green'
                        if statn_dict.get('stationIdentityTypeKey') == 'klimatnummer'
                        else 'red'
                    ),
                    tooltip=statn_dict.get('stationName') or 'Click me!'
                )
                marker.add_to(mc)
        mc.add_to(fg)

    def get_group(self, **kwargs):
        """Return group."""
        fg = folium.FeatureGroup(**kwargs)

        if kwargs.get('add_to_map'):
            fg.add_to(self.map)

        if kwargs.get('return_group'):
            return fg

    def get_html_object(self, item):
        """Return html object."""
        args = []
        for tag in self.marker_tag_attributes:
            value = item.get(tag)
            args.append(value)
        html_string = self.html_fmt % tuple(args)
        return folium.Html(html_string, script=True)

    @staticmethod
    def get_marker(*args, **kwargs):
        """Return marker."""
        return folium.Marker(*args, **kwargs)

    @staticmethod
    def get_popup(html_obj):
        """Return popup object."""
        return folium.Popup(html_obj, max_width=500)


if __name__ == '__main__':
    m = Map()
    # extend...
