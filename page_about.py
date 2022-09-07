from dash import dcc, html
import dash_bootstrap_components as dbc

def about_page(about_df):
    return html.Div(
        [
            html.H4(about_df.loc[0,'titulo']),
            html.Br(),
            html.Br(),
            html.P(about_df.loc[0,'descricao']),
            html.Br(),
            html.Br(),
            html.P(f"Pesquisa por {about_df.loc[0,'nome_lili']}"),
            html.P(f"Website por {about_df.loc[0,'nome_rafa']}"),
        ],
        style={'padding-top': 50, 'padding-bottom': 50}
    )