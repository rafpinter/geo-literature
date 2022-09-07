import dash_bootstrap_components as dbc
import pandas as pd
from dash import dcc, html

def create_accordion_item(city, year, book_synopsis, author_name, author_origin, book_title):
    return dbc.AccordionItem( 
                [
                    html.P(f"{city}, {year}",
                           style={"font-family": "Arial, Helvetica, sans-serif"}),
                    html.P(
                        book_synopsis,
                        # "featured content or information.",
                        # className="lead",
                        style={"font-family": "Arial, Helvetica, sans-serif"}
            ),
            html.Hr(className="my-2"),
            html.P(
                html.B(f"{author_name}, {author_origin}",style={"font-family": "Arial, Helvetica, sans-serif"})
            ),
            # html.P(
            #     dbc.Button("Learn more", color="primary"), className="lead"
            # ),
                ],
                style={"font-family": "Nunito Sans"},
                title=f"{book_title}, {author_name}",
            )

     
def create_country_accordion_list(country, books_df):
    # lista de livros do país
    country_books_df = books_df[books_df['country_name'] == country].copy()
    
    accordion_title = html.H3(country)
    accordion_items = []
    
    for index,row in country_books_df.iterrows():
        
        accordion_item = create_accordion_item(
            city=row['city'], 
            year=row['year'], 
            book_synopsis=row['synopsis'], 
            author_name=row['author'], 
            author_origin="Country",  # colocar quando fizer o join authors e books
            book_title=row['book_title']
            )
        
        accordion_items.append(accordion_item)
    
    country_accordion = [html.Br(), accordion_title, dbc.Accordion(accordion_items, start_collapsed=True)]
    
    # print("country_accordion:", country_accordion)
    
    return country_accordion


def create_accordions(books_df, country_list=None):
    accordions = []
    
    if country_list == None:
        for country in books_df.country_name.unique():
            country_accordion = create_country_accordion_list(country, books_df)
            accordions = accordions + country_accordion
    else:        
        for country in country_list:
                country_accordion = create_country_accordion_list(country, books_df)
                accordions = accordions + country_accordion
        
    return accordions