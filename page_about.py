from dash import dcc, html
import dash_bootstrap_components as dbc
from functions import log

FILE = 'ABOUT'

def about_page(about_df):
    return html.Div(
        [
            html.Div(
                [
                    html.H4(about_df.loc[0,'titulo']),
                    html.Br(),
                    html.Br(),
                    dcc.Markdown(about_df.loc[0,'descricao'], style={"text-align": "justify"}),
                    html.Br(),
                    html.Br(),
                    html.P(
                        children=[
                            f"Pesquisa por ",
                            dcc.Link(children=[about_df.loc[0,'nome_lili']], href=about_df.loc[0,'contato_ligia'])
                        ]
                    ),
                    html.P(
                        children=[
                            f"Website por ",
                            dcc.Link(children=[about_df.loc[0,'nome_rafa']], href=about_df.loc[0,'contato_rafa'])
                        ]
                    ),
                ],
                style={'padding-top': 50, 'padding-bottom': 50, "margin-left": "12.5%", "margin-right": "12.5%"}
            ),
        ]
    )