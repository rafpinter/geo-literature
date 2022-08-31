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

litData = litData()
books_df, lgbt_index_df = litData.get_data()

app = Dash(__name__, external_stylesheets=[dbc.themes.LITERA])
server = app.server

fig = px.choropleth(
    data_frame=lgbt_index_df,
    locations='ISO-3',
    color='legal',
    projection = 'natural earth',
    basemap_visible=True,
    # color_discrete_sequence='RdBu'
)
fig.update_layout(height=500, margin={"r":0,"t":0,"l":0,"b":0}, showlegend=False)



app.layout = dbc.Container(
    [
        dbc.NavbarSimple(
            brand="Geo Literature",
            brand_href="#",
            color="primary",
            dark=True,
        ),
        html.Br(),
        dbc.Row(
            [
                dcc.Graph(
                    id="graph",
                    figure=fig
                ),
            ]    
        ),
        html.Br(),
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
        # dbc.Row(
        #     [   
        #         html.H5("Data"),
        #         dash_table.DataTable(id='table')
        #     ]
        # ),
        html.Br(),
        dbc.Row(
            [   
                html.P("Em construição pela melhor namorada do mundo"),
            ], justify="center", align="center", className="h-50"
        ),
        html.Div(id='test')
    ],
    
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
    [ 
        Output('test', 'children'),
    ],
    [
        Input('graph', 'selectedData'),
    ]
)
def test(a):
    print(a)
    return a
# def update_datatable(input,hoverData):
#     # print(input['data'])
#     # data_sel = 
#     data = books_df.to_dict('records')
    
#     if hoverData != None:
#         # print("hoverdata:", hoverData["points"][0]["location"])
#         try:
#             # print("input:", input['data'][0]['selectedpoints'])
#             data = books_df[books_df["country"] == hoverData["points"][0]["location"]].to_dict('records')
#         except KeyError:
#             data = books_df.to_dict('records')
#         #     hoverData['points']
        
#     columns = [{"name": i, "id": i} for i in books_df.columns]
#     return columns, data
 

if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=8050, debug=False)
    app.run_server(debug=False, host='0.0.0.0', port=8050)