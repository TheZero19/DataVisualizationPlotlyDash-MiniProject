from dash.dependencies import Input, Output
from data_preparation import *
import plotly.express as px
from app import app

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


@app.callback(
    Output(component_id='SelectedCategoricalValuesToPredict', component_property='options'),
    [Input(component_id='selectCategoricalAttributeToPredict', component_property='value')]
)
def update_dropdown_selectCategoricalAttributeToPredict_options(selected_option):
    if selected_option == 'Genre':
        return unique_genres
    elif selected_option == 'Platform':
        return unique_platforms