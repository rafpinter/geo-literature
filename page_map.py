from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
from functions import log
import pandas as pd

FILE = 'PAGE_MAP'

def return_fig(lgbt_index_df, selectedpoints=None):
    log(FILE, "Creating choropleth figure")
    
    lgbt_index_df = lgbt_index_df.rename(
        columns={
            'books_per_country': 'Livres par pays',
            'country': 'Pays',
            'Índice de legalidade': 'Taux de legalité',
            'ISO-3': 'Acronyme du pays',
            }
    )
    
    fig = px.choropleth(
        data_frame=lgbt_index_df,
        locations='Acronyme du pays',
        color='Taux de legalité',
        projection = 'natural earth',
        basemap_visible=True,
        color_continuous_scale='rdbu',
        hover_data=['Pays', 'Livres par pays']
    )
    fig.update_layout(
        height=500, 
        margin={"r":0,"t":0,"l":0,"b":0}, 
        margin_pad=0,
        font_family='Nunito Sans',
    # #   legend_title_text='Índice de legalidade',
        )
    fig.update_coloraxes(showscale=False)
    # fig.update_traces(
    #     hovertemplate='<br>'.join([
    #         "Pays: %{customdata[0]}",
    #         "Taux de legalité: %{'Taux de legalité'}",
    #         "Livre par pays: %{customdata[1]}"
    #     ])
    # )
    if selectedpoints != None:
        log(FILE, f"Updating choropleth figure for selected points: {selectedpoints}")
        fig.update_traces(selectedpoints=selectedpoints)
    return fig

def map_page(lgbt_index_df, books_df):
    log(FILE, "Creating map page front-end")
    return html.Div(
        [
            html.Div(
                [
                    # html.Br(),
                    html.H4("DROITS RÉSERVÉS À LA COMMUNAUTÉ LGBTQIAP+ DANS LE MONDE", 
                            style={
                                # "margin-left": "12.5%", "margin-right": "12.5%",
                                "margin": "auto", 
                                "text-align": "center",
                                "padding-bottom": 10}),
                    dbc.Row(
                        [
                            dcc.Graph(
                                id="graph",
                                figure=return_fig(lgbt_index_df),
                                config={
                                    'displayModeBar': False
                                }
                            ),
                        ]
                    ),
                    # dcc.Markdown(
                    #     "Explicação do mapa e [fonte](www.google.com)",
                    #     style={
                    #         # "margin-left": "12.5%", "margin-right": "12.5%",
                    #         "margin": "auto", 
                    #         "text-align": "center",
                    #         "padding-bottom": 10}
                        # )
                ]
            ),
            html.Div(
                [
                    html.Br(),
                    html.Br(),
                    html.Div(
                        [
                            
                        ],
                        style={"padding-right": "6.5%", "padding-left": "6.5%"}
                    ),
                    # html.Br(),
                    html.H4("REPRÉSENTATION DE L'HOMOSEXUALITÉ FÉMININE DANS LA LITTÉRATURE FRANCOPHONE CONTEMPORAINE",
                            style={
                                # "margin-left": "12.5%", "margin-right": "12.5%",
                                "margin": "auto", 
                                "text-align": "center",
                                "padding-bottom": 10}),
                    html.Br(),
                    dcc.Dropdown(
                        books_df.country_name.unique(),
                        books_df.country_name.unique(),
                        id='country_dropdown',
                        placeholder="Selecione o país",
                        multi=True
                    ),
                    html.Br(),
                    html.Div(id='accordion'),
                    html.Br(),
                    html.Br(),
                    # dbc.Row(
                    #     [   
                    #         html.P("Em construição pela melhor namorada do mundo"),
                    #     ], justify="center", align="center", className="h-50"
                    # ),
                    html.Div(id='test')
                ],
                style={"margin-left": "12.5%", "margin-right": "12.5%"}
            )
        ]
    )