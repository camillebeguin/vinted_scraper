import os
import time
from textwrap import dedent

import dash
from dash import html, dcc
#import dash_core_components as dcc
#import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

import numpy as np
import pandas as pd

from src.config.app_template import *

# Utils
def blank_fig(height):
    """
    Build blank figure with the requested height
    """
    return {
        "data": [],
        "layout": {
            "height": height,
            "template": template,
            "xaxis": {"visible": False},
            "yaxis": {"visible": False},
        },
    }

# Read data and extract the list of brands
DATA_PATH = '../data/preprocessed/pages_data.parquet.gz'
df = pd.read_parquet(DATA_PATH)
brand_list = df['brand'].unique()

# Overlay for a plot pannel
def build_modal_info_overlay(id, side, content):
    """
    Build div representing the info overlay for a plot panel
    """
    div = html.Div(
        [  # modal div
            html.Div(
                [  # content div
                    html.Div(
                        [
                            html.H4(
                                [
                                    "Info",
                                    html.Img(
                                        id=f"close-{id}-modal",
                                        src="assets/times-circle-solid.svg",
                                        n_clicks=0,
                                        className="info-icon",
                                        style={"margin": 0},
                                    ),
                                ],
                                className="container_title",
                                style={"color": "white"},
                            ),
                            dcc.Markdown(content),
                        ]
                    )
                ],
                className=f"modal-content {side}",
            ),
            html.Div(className="modal"),
        ],
        id=f"{id}-modal",
        style={"display": "none"},
    )

    return div

# Build Dash layout
app = dash.Dash(__name__)

app.layout = html.Div(
    children=[
        html.Div(
            [
                html.H1(
                    children=[
                        "Vinted Dashboard",
                        html.A(
                            html.Img(
                                src="assets/Vinted_logo.png",
                                style={"float": "right", "height": "50px"},
                            ),
                            href="https://dash.plot.ly/",
                        ),
                    ],
                    style={"text-align": "left"},
                ),
            ]
        ),
        html.Div(
            children=[
                build_modal_info_overlay(
                    "user-selectors",
                    "bottom",
                    dedent(
                        """
            The _**Filters** panel displays user filters such as the brand or catalog.
            """
                    )
                ),
                build_modal_info_overlay(
                    "scraping-indicator",
                    "bottom",
                    dedent(
                        """
            The _**Scraped Ads**_ panel displays the number of ads that were scraped
            in that category.
            """
                    ),
                ),
                build_modal_info_overlay(
                    "trend-indicator",
                    "bottom",
                    dedent(
                        """
            The _**Ads Trends**_ panel displays the number of ads posted in that
            category in the past 60 days (vs previous period).
        """
                    ),
                ),
                build_modal_info_overlay(
                    "price-hist",
                    "bottom",
                    dedent(
                        """
            The _**Selling Price Distribution**_ panel displays the distribution of prices in
            posted ads. 
        """
                    ),
                ),
                build_modal_info_overlay(
                    "post-fav-scatter",
                    "top",
                    dedent(
                        """
            The _**Favourite conversion over time**_ panel displays a scatterplot of the time since 
            the ad was posted plotted against the number of favourite. 
        """
                    ),
                ),
                build_modal_info_overlay(
                    "post-view-scatter",
                    "top",
                    dedent(
                        """
            The _**View conversion over time**_ panel displays a scatterplot of the time since 
            the ad was posted plotted against the number of favourite. 
        """
                    ),
                ),
                html.Div(
                    children=[
                        html.H4(
                            [
                                "Parameters",
                            ],
                            className="container_title",
                        ),
                        html.Br(),
                        dcc.Markdown('Select a brand: '),
                        dcc.Dropdown(brand_list, brand_list[0], id='brand-selector'),
                        html.Div(id='dd-output-container'),
                    ],
                    className="twelve columns pretty_container",
                    style={
                        "width": "98%",
                        "margin-right": "0",
                    },
                    id="selector-div",
                ),
                html.Div(
                    children=[
                        html.Div(
                            children=[
                                html.H4(
                                    [
                                        "Available Scraped Ads",
                                    ],
                                    className="container_title",
                                ),
                                dcc.Loading(
                                    dcc.Graph(
                                        id="scraped-ads-indicator",
                                        figure=blank_fig(row_heights[0]),
                                        config={"displayModeBar": False},
                                    ),
                                    className="svg-container",
                                    style={"height": 50},
                                ),
                            ],
                            className="six columns pretty_container",
                            id="scraped-div",
                        ),
                        html.Div(
                            children=[
                                html.H4(
                                    [
                                        "Trends Last 30 Days",
                                    ],
                                    className="container_title",
                                ),
                                dcc.Graph(
                                    id="ads-trend-indicator",
                                    figure=blank_fig(row_heights[0]),
                                    config={"displayModeBar": False},
                                ),
                            ],
                            className="six columns pretty_container",
                            id="trend-div",
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.H4(
                            [
                                "Price Distribution",
                            ],
                            className="container_title",
                        ),
                        dcc.Graph(
                            id="price-distrib-graph",
                            figure=blank_fig(row_heights[1]),
                            config={"displayModeBar": False},
                        ),
                    ],
                    className="twelve columns pretty_container",
                    style={
                        "width": "98%",
                        "margin-right": "0",
                    },
                    id="map-div",
                ),
                # html.Div(
                #     children=[
                        # html.Div(
                        #     children=[
                        #         html.H4(
                        #             [
                        #                 "Signal Range",
                        #                 html.Img(
                        #                     id="show-range-modal",
                        #                     src="assets/question-circle-solid.svg",
                        #                     className="info-icon",
                        #                 ),
                        #             ],
                        #             className="container_title",
                        #         ),
                        #         dcc.Graph(
                        #             id="range-histogram",
                        #             figure=blank_fig(row_heights[2]),
                        #             config={"displayModeBar": False},
                        #         ),
                        #         html.Button(
                        #             "Clear Selection",
                        #             id="clear-range",
                        #             className="reset-button",
                        #         ),
                        #     ],
                        #     className="six columns pretty_container",
                        #     id="range-div",
                        # ),
                        # html.Div(
                        #     children=[
                        #         html.H4(
                        #             [
                        #                 "Construction Date",
                        #                 html.Img(
                        #                     id="show-created-modal",
                        #                     src="assets/question-circle-solid.svg",
                        #                     className="info-icon",
                        #                 ),
                        #             ],
                        #             className="container_title",
                        #         ),
                        #         dcc.Graph(
                        #             id="created-histogram",
                        #             config={"displayModeBar": False},
                        #             figure=blank_fig(row_heights[2]),
                        #         ),
                        #         html.Button(
                        #             "Clear Selection",
                        #             id="clear-created",
                        #             className="reset-button",
                        #         ),
                        #     ],
                        #     className="six columns pretty_container",
                        #     id="created-div",
                        # ),
                #     ]
                # ),
            ]
        ),
        html.Div(
            [
                html.H4("Acknowledgements", style={"margin-top": "0"}),
                dcc.Markdown(
                    """\
The Vinted Pricing Dashboard was created in the context of a personal project for the MSc Data Science for Business X-HEC.
"""
                ),
            ],
            style={
                "width": "98%",
                "margin-right": "0",
                "padding": "10px",
            },
            className="twelve columns pretty_container",
        ),
    ]
)

# PANEL 1/2: INDICATORS
@app.callback(
    Output('scraped-ads-indicator', 'figure'),
    Input('brand-selector', 'value')
)
def build_scraped_indicator_figure(brand):
    filtered_df = df[df['brand']==brand]
    n_scraped = filtered_df.shape[0]

    # indicator
    scraped_indicator = {
        "data": [
        {
            "type": "indicator",
            "value": n_scraped,
            "number": {"font": {"color": "#263238", "size": 50}},
            "mode": "number",
            "title": "Total ads count"
        }
    ],
        "layout": {
            # "template": {
            #     'data' : {
            #         'indicator': [{
            #             'delta' : {'reference': 90}}]}},
            "height": row_heights[0],
            "margin": {"l": 10, "r": 10, "t": 10, "b": 10},
            },
    }
    return scraped_indicator

@app.callback(
    Output('ads-trend-indicator', 'figure'),
    Input('brand-selector', 'value')
)
def build_ads_trend_indicator(brand):
    max_date = df['photo_timestamp'].max()
    duration = 30
    filtered_df = df[df['brand']==brand]

    # Period 1: last 30 days
    min_date_p1 = max_date - pd.DateOffset(days=duration)
    n_p1 = (filtered_df['photo_timestamp'].between(min_date_p1, max_date)).sum()

    # Period 1: last 120 to 60 days
    min_date_p2 = max_date - pd.DateOffset(days=duration*2)
    n_p2 = (filtered_df['photo_timestamp'].between(min_date_p2, min_date_p1)).sum()

    # Indicator
    trend_indicator = {
        "data": [
        {
            "type": "indicator",
            "value": n_p1,
            "number": {"font": {"color": "#263238", "size": 50}},
            "mode": "number+delta",
            "title": f"Ads posted in the last {duration} days"
        }
    ],
        "layout": {
            "template": {
                'data' : {
                    'indicator': [{
                        'delta' : {'reference': n_p2}}]}},
            "height": row_heights[0],
            "margin": {"l": 10, "r": 10, "t": 10, "b": 10},
            },
    }
    return trend_indicator

# PANEL 3: PRICE DISTRIBUTION
@app.callback(
    Output('price-distrib-graph', 'figure'),
    Input('brand-selector', 'value')
)
def build_price_distribution_histogram(brand):
    filtered_df = df[df['brand']==brand]
    fig = px.histogram(filtered_df['price'], color_discrete_sequence=["#008080"])
    fig.update_layout(
        xaxis_title='Selling price (€)',
        yaxis_title='Ads',
        template=template,
        showlegend=False
    )
    return fig

if __name__ == "__main__":
    app.run_server(debug=True)
