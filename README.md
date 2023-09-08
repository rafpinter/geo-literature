# Geo Literature

This website aims to share the data about a survey of works written by women that contemplate female characters in homoaffective relationships. The publications are contemporary and made by French-speaking writers.


## Infrastructure

The webpage was created only using the Plotly Dash framework. It is encapsulated into a Docker container that ultimately is used by a Heroku App.

If you want to run the app, install the requirements

```
pip install -r requirements.txt
```

and then:

1. Create a `.env` file at the root of the directory with the following variables:

```
SPREADSHEET_ID
BOOKS_TAB_ID
EQUALITY_SCORES_TAB_ID
ABOUT_TAB_ID
ISO_CODES_TAB_ID 
```

2. Run the dash app with:

```
python app.py
```

## How to get the data

Please contact me to get access to the data via email:

rafaelaspinter@gmail.com