import dash
from dash import dcc, html # Starting the app and reading data
from data_preparation import *

external_stylesheets = [
    "https://codepen.io/chriddyp/pen/bWLwgP.css"
]

app = dash.Dash(__name__,
                external_stylesheets = external_stylesheets
                )

# App Layout
app.layout = html.Div([
    html.Div([
        html.Img(src="/assets/1.png"),
        html.H1("Sales of Video Games"),

    ], className="banner"),

    html.Div([
        html.Div([
            html.H4("Select the genre and the platform to view scatterplot over the years"),

            html.Div([
                html.Div([
                    html.Div([
                        dcc.Dropdown(
                            id='selectGenre',
                            options=dropdown_options_genres,
                            value='Action',
                            multi=False
                        ),
                    ], className="six columns"),
                    html.Div([
                        dcc.Dropdown(
                            id='selectPlatform',
                            options=dropdown_options_platform,
                            value="PC",
                            multi=False,
                        ),
                    ], className="six columns"),
                ]),

                html.Div(
                    id='container',
                    children=[]
                ),
                dcc.Graph(
                    id='testGraph',
                    figure={}
                ),
            ], className="eleven columns"),
        ], className="six columns"),

        html.Div([
            html.H4("Select the year for viewing the sales distribution over different genres"),

            html.Div([
                dcc.Dropdown(
                    id='YearForBarChartOfTotalSalesOnUniqueGenre',
                    options=dropdown_options_years,
                    value=2013,
                ),
                dcc.Graph(
                    id='GraphForBarChartOfTotalSalesBasedOnGenre',
                    figure={},
                ),
            ], className="eleven columns"),

        ], className="six columns"),
    ], className="eleven columns"),

    html.Div([
        html.Div([
            html.H4("Select the year for viewing distribution of number of games based on genre in different years"),

            html.Div([
                dcc.Dropdown(
                    id='ForPieChartOfGenreDistInDifferentYears',
                    options=dropdown_options_years,
                    value=2013,
                    style={'width': '40%'}
                ),

                dcc.Graph(
                    id='PieChartOfGenreDistInDifferentYears',
                    figure={}
                ),
            ], className="eleven columns"),
            ], className="six columns"),

        html.Div([
            html.H4("Select the categorical data to be predicted to compare the algorithm for classifiers"),

            html.Div([
                html.Label("Select one category"),
                dcc.Dropdown(
                    id='selectCategoricalAttributeToPredict',
                    options=[
                        {'label': 'Genre', 'value': 'Genre', },
                        {'label': 'Platform', 'value': 'Platform'},
                    ],
                    value='Genre',
                    multi=False,
                    style={'width': '40%'}
                ),
                html.Br(),
                html.Label("Select one or more classes"),
                dcc.Dropdown(
                    id='SelectedCategoricalValuesToPredict',
                    options=unique_genres,
                    value=['Action', 'Role-Playing'],  # THANK YOU FOR WASTING 2.5 HOURS
                    multi=True,

                ),
                html.Br(),
                html.Label("Result:"),
                html.Div(
                    id='container2',
                    children=[]
                ),
            ], className="eleven columns"),
            ], className="six columns"),
        ], className="eleven columns"),

])

# Callbacks Section:
from callbacks import *

if __name__ == '__main__':
    app.run(debug=True)