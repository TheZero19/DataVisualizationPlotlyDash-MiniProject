import dash
from dash import dcc, html # Starting the app and reading data
from data_preparation import *

app = dash.Dash(__name__)

# App Layout
app.layout = html.Div([

    html.H1("Sales of Video Games"),
    dcc.Dropdown(
                id = 'selectGenre',
                options = dropdown_options_genres,
                value = 'Action',
                style={'width' : '40%'},
                multi = False
    ),

    dcc.Dropdown(
                id = 'selectPlatform',
                options = dropdown_options_platform,
                value = "PC",
                multi = False,
                style = {'width' : '40%'}
    ),

    html.Br(),

    html.Div(
        id = 'container',
        children = []
    ),

    dcc.Graph(
            id = 'testGraph',
            style = {'width':'40%'},
            figure = {}
    ),

    html.H2("Select the year for viewing genre distributions in different years"),
    dcc.Dropdown(
                id = 'ForPieChartOfGenreDistInDifferentYears',
                options=dropdown_options_years,
                value=2013,
                style={'width':'40%'}
    ),

    dcc.Graph(
            id = 'PieChartOfGenreDistInDifferentYears',
            style = {'width':'40%'},
            figure = {}
    ),

    html.Br(),

    html.H3("Select the categorical data to be predicted to compare the algorithm for classifiers"),

    dcc.Dropdown(
                id = 'selectCategoricalAttributeToPredict',
                options = [
                    {'label' : 'Genre', 'value' : 'Genre',},
                    {'label' : 'Platform', 'value' : 'Platform'},
                ],
                value = 'Genre',
                multi=False,
                style={'width':'40%'}
    ),

    dcc.Dropdown(
                id = 'SelectedCategoricalValuesToPredict',
                options = unique_genres,
                value = ['Action', 'Role-Playing'], # THANK YOU FOR WASTING 2.5 HOURS
                multi=True,
    ),

    html.Div(
        id = 'container2',
        children=[]
    ),

])

# Callbacks Section:
from callbacks import *

if __name__ == '__main__':
    app.run(debug=True)