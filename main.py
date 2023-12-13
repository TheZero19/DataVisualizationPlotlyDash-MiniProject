import dash
from dash import dcc, html
import pandas as pd
from dash.dependencies import Input, Output
import plotly.express as px

# Starting the app and reading data
app = dash.Dash(__name__)
df = pd.read_csv("VideoGamesSales.csv")

# -----------------------------------------------------------------------------------------------------
# Cleaning
# Drop rows with null values in the attributes/columns specified:
df = df.dropna(subset=['Genre'])
df = df.dropna(subset=['Platform'])
df = df.dropna(subset=['Year'])

# Find and get unique values of different attributes
unique_genres = df['Genre'].unique()
unique_platform = df['Platform'].unique()
unique_years = df['Year'].unique()

# Create options for the dropdown as the dcc.Dropdown expects a list of dictionaries
dropdown_options_genres = [{'label': genre, 'value' : genre} for genre in unique_genres]
dropdown_options_platform = [{'label' : publisher, 'value' : publisher} for publisher in unique_platform]
dropdown_options_years = [{'label': year, 'value': year} for year in unique_years]

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
            style = {'width':'40%'},
            figure = {}
    ),

    # dcc.Dropdown(
    #             id = 'selectGenreForGlobalSalesInDifferentYears',
    #             options = dropdown_options_genres,
    #             value = "PC",
    #             multi = False,
    #             style = {'width' : '40%'}
    # ),

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
    )
])

# -----------------------------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components.
@app.callback(
    [Output(component_id='testGraph', component_property='figure'),
    Output(component_id='container', component_property='children'),
    Output(component_id='PieChartOfGenreDistInDifferentYears', component_property='figure')],

    [Input(component_id = 'selectGenre', component_property='value'),
     Input(component_id= 'selectPlatform', component_property='value'),
     Input(component_id= 'ForPieChartOfGenreDistInDifferentYears', component_property= 'value')]
)

def updateGraph(genre_selected, platform_selected, yearForGenreDist): # #of args = #of inputs in the callback & arg always refers to the component_property
    print(genre_selected)
    print(type(genre_selected))

    print(platform_selected)
    print(type(platform_selected))

    container = "The genre chosen by the user was {} for {}".format(genre_selected, platform_selected)

    # Making a copy of df so that any changes we make here in the function won't be affected to the original df
    dff = df.copy()
    dff2 = df.copy()

    # Graph 1
    dff = dff[dff["Genre"] == genre_selected]
    dff = dff[dff["Platform"] == platform_selected]

    # Graph 2 --pie chart in genre distributions in different years
    dff2 = dff2[dff2["Year"] == yearForGenreDist]
    genre_counts = dff2['Genre'].value_counts().reset_index() # Calculate the number of games per genre for the selected year
    genre_counts.columns = ['Genre', 'Count']

    #Checking
    print(dff.head())

    # Plotly Express
    fig = px.scatter(
        data_frame=dff,
        x = "Year",
        y = "Global_Sales"
    )

    fig2 = px.pie(genre_counts, values='Count', names='Genre', title=f"Games by Genre in {yearForGenreDist}")

    # order of returned values is wrt to the order of [Output]s in the callback
    return fig, container, fig2

if __name__ == '__main__':
    app.run(debug=True)