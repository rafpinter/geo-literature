from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
from functions import log

FILE = 'PAGE_MAP'

def return_fig(lgbt_index_df, selectedpoints=None):
    log(FILE, "Creating choropleth figure")
    fig = px.choropleth(
        data_frame=lgbt_index_df,
        locations='ISO-3',
        color='Índice de legalidade',
        projection = 'natural earth',
        basemap_visible=True,
        color_continuous_scale='rdbu',
        hover_data=['ISO-3', 'country', 'books_per_country']
    )
    fig.update_layout(
        height=500, 
        margin={"r":0,"t":0,"l":0,"b":0}, 
        margin_pad=0,
        font_family='Nunito Sans',
    # #   legend_title_text='Índice de legalidade',
        )
    fig.update_coloraxes(showscale=False)
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
                    html.H4("Direitos reservados à comunidade LGBTQIAP+ no mundo", 
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
                    html.H4("Representatividade da homoafetividade entre mulheres na literatura de expressão francesa contemporânea",
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