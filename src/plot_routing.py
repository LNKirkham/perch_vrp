
#!/usr/bin/env python
"""
PROJECT:
    Perch_VRP

CODE:
    plot_routing.py

SUMMARY:
    Plots the routing solution

DOCS:
    None yet

DEPENDENCIES:
    Configuration parameters specified in config.py

LAST EDITED:
    2021-04-13  Created - Louise

CONTACT:
    Louise Kirkham <louisek@gmail.com.com>

REPO:
    https://github.com/LNKirkham/perch_vrp

"""


import pandas as pd
import numpy as np
from filepaths import FILEPATHS
from collection_point import canababes
import plotly.graph_objects as go


def plot_routing_solution(delivery_points_df, collection_point_df, selected_locations_df):

    my_mapbox_access_token = 'pk.eyJ1IjoibG91aXNla2lya2hhbSIsImEiOiJjazYxMGJrZDcwOTdzM3RxaXQ4NG1jZHVlIn0.NeE7I8fu5zglEoeFc_eirQ'

    fig = go.Figure()

    # Map layout
    fig.update_layout(
        autosize=True,
        hovermode='closest',
        mapbox=dict(
            accesstoken=my_mapbox_access_token,
            style='light',
            center={'lon': np.mean(delivery_points_df['longitude']),
                    'lat': np.mean(delivery_points_df['latitude'])},
            zoom=11
        ),
    )

    for route_num, route_df in selected_locations_df.groupby('route_num'):
        # Add collection point to group df
        route_df = pd.concat([collection_point_df, route_df]).reset_index(drop=True)

        # Add route to map
        fig.add_trace(go.Scattermapbox(
            lat=route_df['latitude'],
            lon=route_df['longitude'],
            mode='lines+markers',
            marker=go.scattermapbox.Marker(
                size=13,
            ),
            hoverinfo='text',
            text='Stop ' + route_df.index.astype(str) + ' - ' + route_df['address'],

            name='Route ' + str(route_num)
        ))

    fig.show()

    fig.write_html(FILEPATHS['solution_plot'])


if __name__ == '__main__':

    delivery_points_df = pd.read_csv(FILEPATHS['delivery_points'], index_col=False)
    collection_point_df = pd.DataFrame.from_records([s.to_dict() for s in [canababes]])
    selected_locations_df = pd.read_csv(FILEPATHS['selected_locations_solution'], index_col=False)

    plot_routing_solution(delivery_points_df, collection_point_df, selected_locations_df)