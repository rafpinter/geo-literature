import dash_bootstrap_components as dbc
from dash import dcc, html
from datetime import datetime

FILE = "FUNCTIONS"


def log(FILE, message):
    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | {FILE} | {message}")


def create_accordion_item(
    publishers,
    city,
    year,
    book_synopsis,
    author_name,
    author_origin,
    book_title,
    book_link,
):
    font = "Nunito Sans"
    return dbc.AccordionItem(
        [
            dcc.Link(children=[book_title], href=book_link),
            html.P(),
            html.P(
                f"{publishers}, {city}, {year}",
                #    style={"font-family": font}
                className="text-muted",
            ),
            # html.Br(),
            html.P(
                book_synopsis,
                # style={"font-family": font}
            ),
            # html.Hr(className="my-2"),
            html.P(html.H6(f"{author_name}, {author_origin}")),
        ],
        style={"font-family": font},
        title=f"{book_title} - {author_name}",
    )


def create_country_accordion_list(country, books_df):
    # lista de livros do país
    country_books_df = books_df[books_df["country_name"] == country].copy()
    country_books_df = country_books_df.sort_values(by="author", ascending=True)
    accordion_title = html.H3(country)
    accordion_items = []

    for index, row in country_books_df.iterrows():

        accordion_item = create_accordion_item(
            publishers=row["publishers"],
            city=row["city"],
            year=row["year"],
            book_synopsis=row["synopsis"],
            author_name=row["author"],
            author_origin=row["nationality"],
            book_title=row["book_title"],
            book_link=row["link_ref"],
        )

        accordion_items.append(accordion_item)

    country_accordion = [
        html.Br(),
        accordion_title,
        dbc.Accordion(accordion_items, start_collapsed=True),
    ]

    return country_accordion


def create_accordions(books_df, country_list=None):
    accordions = []

    if country_list == None:
        for country in books_df.country_name.unique():
            log(FILE, f"Creating accordeon for {country}")
            country_accordion = create_country_accordion_list(country, books_df)
            accordions = accordions + country_accordion
    else:
        for country in country_list:
            log(FILE, f"Creating accordeon for {country}")
            country_accordion = create_country_accordion_list(country, books_df)
            accordions = accordions + country_accordion

    return accordions


def footer(about_df):
    return html.Div(
        [
            html.Footer(
                children=[
                    html.Br(),
                    dcc.Link(
                        children=["Contribuer à notre base de données"],
                        href=about_df.loc[0, "forms_link"],
                        style={"color": "#cdcece"},
                    ),
                    html.Br(),
                    html.P(
                        f"Dernière mise à jour le 04/12/2022",
                        style={"color": "#707273"},
                    ),
                ],
                style={
                    "padding-up": 150,
                    "vertical-align": "middle",
                },
            ),
        ],
        style={
            "padding-up": 150,
            "padding-left": "12.5%",
            "vertical-align": "middle",
            "padding-right": "12.5%",
            "padding-bottom": 10,
            "background-color": "#1c1c1c",
        },
    )
