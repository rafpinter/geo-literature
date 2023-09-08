from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import json

from configs.vars import APP_TITLE, APP_FAVICON, PAGE_HEADER, APP_HOST, APP_PORT
from configs.vars import (
    SPREADSHEET_ID,
    BOOKS_TAB_ID,
    EQUALITY_SCORES_TAB_ID,
    ABOUT_TAB_ID,
    ISO_CODES_TAB_ID,
)
from src.country_names import country_dict
from src.functions import create_accordions, footer, log
from src.preprocess import litData
from pages.page_map import return_fig, map_page
from pages.page_about import about_page

FILE = "APP"

log(FILE, "Opening geojson")
with open("data/custom.geo.json") as geojson:
    geojson = json.load(geojson)

countries_geo = []

log(FILE, "Formating geojson")
# Looping over the custom GeoJSON file
for country in geojson["features"]:
    # Country name detection
    country_id = country["properties"]["sov_a3"]
    geometry = country["geometry"]
    # Adding 'id' information for further match between map and data
    countries_geo.append({"type": "Feature", "geometry": geometry, "id": country_id})
geojson = {"type": "FeatureCollection", "features": countries_geo}

log(FILE, "Getting data")

# Creating object
litData = litData(
    SPREADSHEET_ID=SPREADSHEET_ID,
    BOOKS_TAB_ID=BOOKS_TAB_ID,
    EQUALITY_SCORES_TAB_ID=EQUALITY_SCORES_TAB_ID,
    ABOUT_TAB_ID=ABOUT_TAB_ID,
    ISO_CODES_TAB_ID=ISO_CODES_TAB_ID,
)
books_df, lgbt_index_df, about_df = litData.get_data()

br_codes = books_df[["ISO-3", "country_name"]].copy().drop_duplicates()

log(FILE, "Creating dash object")
app = Dash(__name__, external_stylesheets=[dbc.themes.LUX])
server = app.server

app.title = APP_TITLE
app._favicon = APP_FAVICON

log(FILE, "Creating main app front-end")
app.layout = dbc.Container(
    [
        dcc.Location(id="url"),
        dbc.NavbarSimple(
            brand=PAGE_HEADER,
            brand_href="/",
            color="primary",
            dark=True,
            children=[
                dbc.NavItem(dbc.NavLink("Carte", href="/")),
                dbc.NavItem(dbc.NavLink("À PROPOS", href="/about")),
            ],
            style={"margin-left": 0, "margin-right": 0},
        ),
        html.Br(),
        html.Div(
            id="page-content",
            children=[],
            style={"margin-left": 125, "margin-right": 125},
        ),
        footer(about_df),
    ],
    fluid=True,
    style={"margin-left": 0, "margin-right": 0, "padding-left": 0, "padding-right": 0},
)


@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname"),
)
def change_page(pathname):
    log(FILE, f"Redirecting to {pathname}")
    if pathname == "/" or pathname == "":
        return map_page(lgbt_index_df, books_df)
    elif pathname == "/about":
        return about_page(about_df)
    else:
        return html.P("Page Not Found")


@app.callback(Output("accordion", "children"), Input("country_dropdown", "value"))
def update_output(value):
    if len(value) == 0:
        log(FILE, "Creating accordions to all data")
        return create_accordions(books_df)
    else:
        log(FILE, f"Creating accordions to {value}")
        return create_accordions(books_df, value)


@app.callback(Output("graph", "figure"), Input("country_dropdown", "value"))
def test(dropdown_selected_countries):
    if len(dropdown_selected_countries) == 0:
        log(FILE, f"Creating graph to all data")
        return return_fig(lgbt_index_df)
    else:
        countries = [
            country_dict[
                br_codes.loc[br_codes["country_name"] == country, "ISO-3"].item()
            ]
            for country in dropdown_selected_countries
            if country != None
        ]
        log(FILE, f"Creating graph to {countries}")
        return return_fig(lgbt_index_df, selectedpoints=countries)


if __name__ == "__main__":
    # app.run(host='0.0.0.0', port=8050, debug=False)
    app.run_server(debug=False, host=APP_HOST, port=APP_PORT)
