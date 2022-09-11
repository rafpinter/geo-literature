from dash import Dash, dcc, html, Input, Output, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import json

from preprocess import litData
from functions import create_accordions, footer
from page_map import return_fig, map_page
from page_about import about_page

with open("custom.geo.json") as geojson:
    geojson = json.load(geojson)

countries_geo = []

# Looping over the custom GeoJSON file
for country in geojson['features']:
    
    # Country name detection
    country_id = country['properties']['sov_a3']
    geometry = country['geometry']
    # Adding 'id' information for further match between map and data 
    countries_geo.append({
        'type': 'Feature',
        'geometry': geometry,
        'id':country_id
        })
geojson = {'type': 'FeatureCollection', 'features': countries_geo}

ls = ['ISL', 'CAN', 'IMN', 'URY', 'NOR', 'AND', 'NLD', 'DEU', 'GBR', 'AUS', 'CHE', 'VUT', 'ARG', 'MLT', 'NZL', 'USA', 'SMR', 'SWE', 'BRA', 'ESP', 'FJI', 'LIE', 'DNK', 'LUX', 'BLZ', 'ZAF', 'FRA', 'CHL', 'FIN', 'BEL', 'MEX', 'CUB', 'ISR', 'AUT', 'PRT', 'IRL', 'CZE', 'SUR', 'CRI', 'MCO', None, 'CPV', 'WSM', 'PLW', 'SYC', 'SVN', 'NPL', 'COL', 'ECU', 'MHL', 'JPN', 'ITA', 'GNQ', 'IND', 'AGO', 'MOZ', 'MUS', 'GRC', 'LAO', 'GNB', 'TWN', 'BOL', None, 'CYP', 'TJK', 'NAM', 'NRU', 'HRV', 'NIC', 'EST', 'FSM', 'PER', 'BTN', 'VEN', 'BWA', 'BHS', 'UZB', 'SLV', 'SVK', 'PHL', 'GTM', 'TLS', 'BGR', 'HND', 'VNM', 'HUN', 'COD', 'STP', 'THA', 'LTU', 'MNE', 'LVA', 'ROU', 'POL', 'SRB', 'KOR', 'BHR', 'TON', 'PAN', 'KIR', 'BIH', 'GEO', 'ALB', 'PNG', 'LSO', 'GAB', 'PRY', 'KHM', 'LKA', 'TKM', 'CHN', 'MNG', 'UKR', 'TTO', 'KGZ', 'BFA', 'TUV', 'DOM', 'ATG', 'GRD', 'IDN', 'BLR', 'MDG', 'LCA', 'TUR', 'MDA', 'MKD', 'RUS', 'HTI', 'KAZ', 'BEN', 'SYR', 'PAK', 'BRB', 'LBN', 'RWA', 'ARM', 'COG', 'MLI', 'CIV', 'SWZ', 'DJI', 'SGP', 'JAM', 'KNA', 'SLB', 'GUY', 'NER', 'MDV', 'SLE', 'AZE', 'ZWE', 'DMA', 'MAR', 'KWT', 'CAF', 'BDI', 'KEN', 'VCT', 'LBR', 'GHA', 'BGD', 'JOR', 'ERI', 'SSD', 'MWI', 'PRK', 'ZMB', 'TGO', 'COM', 'PSE', 'CMR', 'TZA', 'GIN', 'MMR', 'TUN', 'SEN', 'DZA', 'IRQ', 'UGA', 'TCD', 'ETH', 'MYS', 'SDN', 'OMN', 'EGY', 'NGA', 'GMB', 'LBY', 'IRN', 'QAT', 'ARE', 'SOM', 'MRT', 'YEM', 'SAU', 'BRN', 'AFG']
country_dict = {}
for i, country in enumerate(ls):
    country_dict[country] = i

litData = litData()
books_df, lgbt_index_df, about_df = litData.get_data()

br_codes = books_df[['ISO-3', 'country_name']].copy().drop_duplicates()

app = Dash(__name__, external_stylesheets=[dbc.themes.LUX])
server = app.server

app.title = "Geo-Lit"
app._favicon = ("favicon.png")

app.layout = dbc.Container(
    [
        dcc.Location(id="url"),
        dbc.NavbarSimple(
            brand="Geografia Literária Francófona",
            brand_href="/",
            color="primary",
            dark=True,
            children=[
                dbc.NavItem(dbc.NavLink("Map", href="/")),
                dbc.NavItem(dbc.NavLink("About", href="/about"))
            ],
            style={"margin-left": 0, "margin-right": 0}
        ),
        html.Br(),
        html.Div(
            id='page-content',
            children=[],
            style={"margin-left": 125, "margin-right": 125}
        ),
        footer(about_df),
    ],
    fluid=True,
    style={"margin-left": 0, "margin-right": 0, "padding-left": 0, "padding-right": 0}
)

@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname'),
)
def change_page(pathname):
    if pathname == '/' or pathname == '':
        return map_page(lgbt_index_df, books_df)
    elif pathname == '/about':
        return about_page(about_df)
    else:
        return html.P('Page Not Found')

@app.callback(
    Output('accordion', 'children'),
    Input('country_dropdown', 'value')
)
def update_output(value):
    if len(value) == 0:
        return create_accordions(books_df)
    else:
        return create_accordions(books_df, value)


@app.callback(
    Output('graph', 'figure'),
    Input('country_dropdown', 'value')
)
def test(dropdown_selected_countries):
    if len(dropdown_selected_countries) == 0:
        return return_fig(lgbt_index_df)
    else:
        countries = [country_dict[br_codes.loc[br_codes['country_name']==country,'ISO-3'].item()] for country in dropdown_selected_countries if country != None]
        return return_fig(lgbt_index_df, selectedpoints=countries)


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=8050, debug=False)
    app.run_server(debug=False, host='0.0.0.0', port=8050)