from dash import Dash, dcc, html, Input, Output, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import json

from preprocess import litData
from functions import create_accordions

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
books_df, lgbt_index_df = litData.get_data()

br_codes = books_df[['ISO-3', 'country_name']].copy().drop_duplicates()

app = Dash(__name__, external_stylesheets=[dbc.themes.LUX])
server = app.server


def return_fig(selectedpoints=None):
    
    if selectedpoints == None:
        fig = px.choropleth(
            data_frame=lgbt_index_df,
            locations='ISO-3',
            color='legal',
            projection = 'natural earth',
            basemap_visible=True,
            color_continuous_scale='rdbu'
        )
        fig.update_layout(height=500, margin={"r":0,"t":0,"l":0,"b":0}, showlegend=False)
        
    else:
        fig = px.choropleth(
            data_frame=lgbt_index_df,
            locations='ISO-3',
            color='legal',
            projection = 'natural earth',
            basemap_visible=True,
            color_continuous_scale='rdbu'
            # color_discrete_sequence='RdBu'
            )
        fig.update_layout(
            height=500, 
            margin={"r":0,"t":0,"l":0,"b":0}, 
            showlegend=False)
        fig.update_traces(selectedpoints=selectedpoints)
    return fig


app.layout = dbc.Container(
    [
        dbc.NavbarSimple(
            brand="Geo Literature",
            brand_href="#",
            color="primary",
            dark=True,
            style={"margin-left": 0, "margin-right": 0}
        ),
        html.Br(),
        html.Div(
            [
                dbc.Row(
                    [
                        dcc.Graph(
                            id="graph",
                            figure=return_fig()
                        ),
                    ]    
                ),
                html.Br(),
                html.Br(),
                html.Div(
                    [
                        
                    ],
                    style={"padding-right": 25, "padding-left": 25}
                ),
                dcc.Dropdown(
                    books_df.country_name.unique(),
                    [],
                    id='country_dropdown',
                    placeholder="Selecione o país",
                    multi=True
                ),
                html.Br(),
                html.Div(id='accordion'),
                html.Br(),
                html.Br(),
                dbc.Row(
                    [   
                        html.P("Em construição pela melhor namorada do mundo"),
                    ], justify="center", align="center", className="h-50"
                ),
                html.Div(id='test')
            ],
            style={"margin-left": 125, "margin-right": 125}
        ),
    ],
    fluid=True,
    style={"margin-left": 0, "margin-right": 0, "padding-left": 0, "padding-right": 0}
)

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
        return return_fig()
    else:
        countries = [country_dict[br_codes.loc[br_codes['country_name']==country,'ISO-3'].item()] for country in dropdown_selected_countries if country != None]
        return return_fig(countries)


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=8050, debug=False)
    app.run_server(debug=False, host='0.0.0.0', port=8050)