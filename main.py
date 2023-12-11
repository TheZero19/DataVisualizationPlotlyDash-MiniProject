import dash
from dash import dcc, html
import pandas as pd
from dash.dependencies import Input, Output
import plotly.express as px

# Starting the app
app = dash.Dash(__name__)

# -----------------------------------------------------------------------------------------------------
df = pd.read_csv("VideoGamesSales.csv")
# Find and get unique values of different attributes
unique_genres = df['Genre'].unique()
unique_platform = df['Platform'].unique()

# Create options for the dropdown as the dcc.Dropdown expects a list of dictionaries
dropdown_options_genres = [{'label': genre, 'value' : genre} for genre in unique_genres]
dropdown_options_platform = [{'label' : publisher, 'value' : publisher} for publisher in unique_platform]

# -----------------------------------------------------------------------------------------------------
# checking values
print(df.head())
print(unique_genres)
print(unique_platform)

# -----------------------------------------------------------------------------------------------------
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
            style = {'width':'50%'},
            figure = {}
    )
])

# -----------------------------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components.
@app.callback(
    [Output(component_id='testGraph', component_property='figure'),
    Output(component_id='container', component_property='children')],
    [Input(component_id = 'selectGenre', component_property='value'),
     Input(component_id= 'selectPlatform', component_property='value')]
)

def updateGraph(genre_selected, platform_selected): # #of args = #of inputs in the callback & arg always refers to the component_property
    print(genre_selected)
    print(type(genre_selected))

    print(platform_selected)
    print(type(platform_selected))

    container = "The genre chosen by the user was {} for {}".format(genre_selected, platform_selected)

    # Making a copy of df so that any changes we make here in the function won't be affected to the original df
    dff = df.copy()
    dff = dff[dff["Genre"] == genre_selected]
    dff = dff[dff["Platform"] == platform_selected]

    #Checking
    print(dff.head())

    # Plotly Express
    fig = px.scatter(
        data_frame=dff,
        x = "Year",
        y = "Global_Sales"
    )

    # order of returned values is wrt to the order of [Output]s in the callback
    return fig, container

if __name__ == '__main__':
    app.run(debug=True)