from dash import Dash, dcc, html, Input, Output, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

# from layout import layout
colors = ['#57b82e', '#73f541', '#fff550', '#face48', '#ec3832', '#a82421']

app = Dash(__name__, external_stylesheets=[dbc.themes.LITERA])

df = pd.read_csv('geo_test.csv')
df["index"] = df["index"].astype(str)

fig = px.choropleth(
    data_frame=df,
    locations='country',
    color='index',
    projection = 'natural earth',
    basemap_visible=True,
    color_discrete_sequence=colors
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
        dbc.Row(
            [   
                html.H5("Data"),
                dash_table.DataTable(id='table')
            ]
        ),
        html.Br(),
        html.Br(),
        dbc.Row(
            [   
                html.P("Em construição pela melhor namorada do mundo"),
            ], justify="center", align="center", className="h-50"
        ),
    ],
    
)

@app.callback(
    [ 
        Output('table', 'columns'),
        Output('table', 'data'),
    ],
    [
        Input('graph', 'figure'),
        Input('graph', 'hoverData')
    ]
)
def update_datatable(input,hoverData):
    print(input['data'])
    # data_sel = 
    data = df.to_dict('records')
    
    if hoverData != None:
        print("hoverdata:", hoverData["points"][0]["location"])
        try:
            print("input:", input['data'][0]['selectedpoints'])
            data = df[df["country"] == hoverData["points"][0]["location"]].to_dict('records')
        except KeyError:
            data = df.to_dict('records')
        #     hoverData['points']
        
    columns = [{"name": i, "id": i} for i in df.columns]
    return columns, data

app.run_server(debug=True)