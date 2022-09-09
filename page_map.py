from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px


def return_fig(lgbt_index_df, selectedpoints=None):
    
    if selectedpoints == None:
        fig = px.choropleth(
            data_frame=lgbt_index_df,
            locations='ISO-3',
            color='Índice de legalidade',
            projection = 'natural earth',
            basemap_visible=True,
            color_continuous_scale='rdbu'
        )
        fig.update_layout(height=500, 
                          margin={"r":0,"t":0,"l":0,"b":0}, 
                          margin_pad=0,
                          font_family='Nunito Sans'
                        #   legend_title_text='Índice de legalidade',
                          ) 
    else:
        fig = px.choropleth(
            data_frame=lgbt_index_df,
            locations='ISO-3',
            color='Índice de legalidade',
            projection = 'natural earth',
            basemap_visible=True,
            color_continuous_scale='rdbu'
            # color_discrete_sequence='RdBu'
            )
        fig.update_layout(
            height=500,
            margin={"r":0,"t":0,"l":0,"b":0},
            # legend_title_text='Índice de legalidade',
            )
        fig.update_traces(selectedpoints=selectedpoints)
    return fig

def map_page(lgbt_index_df, books_df):
    return html.Div(
        [
            html.Br(),
            html.Br(),
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
            # dbc.Row(
            #     [   
            #         html.P("Em construição pela melhor namorada do mundo"),
            #     ], justify="center", align="center", className="h-50"
            # ),
            html.Div(id='test')
        ]
    )