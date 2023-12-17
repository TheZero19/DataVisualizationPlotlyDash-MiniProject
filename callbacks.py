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
    # print(genre_selected)
    # print(type(genre_selected))
    #
    # print(platform_selected)
    # print(type(platform_selected))

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
    Output(component_id='GraphForBarChartOfTotalSalesBasedOnGenre', component_property='figure'),
    [Input(component_id='YearForBarChartOfTotalSalesOnUniqueGenre', component_property='value')]
)
def updateBarChartOfTotalSalesBasedOnGenreOverTheYears(selected_year):
    dff = pd.read_csv("VideoGamesSales.csv")
    dff = dff[dff["Year"] == selected_year]
    genre_sales = dff.groupby('Genre')['Global_Sales'].sum().reset_index()
    fig = px.bar(genre_sales, x='Genre', y='Global_Sales', labels={'Global_Sales': 'Total Sales'},
                 title=f'Total Sales by Genre in {selected_year}')
    return fig

@app.callback(
    Output(component_id='SelectedCategoricalValuesToPredict', component_property='options'),
    [Input(component_id='selectCategoricalAttributeToPredict', component_property='value')]
)
def update_dropdown_selectCategoricalAttributeToPredict_options(selected_option):
    if selected_option == 'Genre':
        return unique_genres
    elif selected_option == 'Platform':
        return unique_platforms

@app.callback(
    Output(component_id='container2', component_property='children'),
    [Input(component_id='selectCategoricalAttributeToPredict', component_property='value'),
     Input(component_id='SelectedCategoricalValuesToPredict', component_property='value')]
)
def updatePredictionOfDecisionTreeClassifier(selected_category, selected_categorical_values):
    df_prediction = pd.read_csv("VideoGamesSales.csv")

    if selected_category == 'Platform':
        df_prediction = df_prediction[df_prediction["Platform"].isin(selected_categorical_values)]
        # df_prediction.info()
        print("Platform Selected")

        # Drop rows with null values in specific columns
        columns_to_check = ['Genre', 'Platform', 'NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales', 'Global_Sales']
        df_prediction = df_prediction.dropna(subset=columns_to_check)

        # Encode categorical variables
        from sklearn.preprocessing import LabelEncoder
        label_encoder = LabelEncoder()
        df_prediction['Publisher'] = label_encoder.fit_transform(df_prediction['Publisher'])
        df_prediction['Platform'] = label_encoder.fit_transform(df_prediction['Platform'])
        df_prediction['Genre'] = label_encoder.fit_transform(df_prediction['Genre'])

        # Split dataset into features and target variable
        features = ['Publisher', 'Genre', 'NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales', 'Global_Sales']
        X = df_prediction[features]
        y = df_prediction['Platform']

    else:
        # if selected_category == 'Genre':
        df_prediction = df_prediction[df_prediction["Genre"].isin(selected_categorical_values)]

        print("Genre Selected")

        # Drop rows with null values in specific columns
        columns_to_check = ['Genre', 'Platform', 'NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales', 'Global_Sales']
        df_prediction = df_prediction.dropna(subset=columns_to_check)

        # Encode categorical variables
        from sklearn.preprocessing import LabelEncoder
        label_encoder = LabelEncoder()
        df_prediction['Publisher'] = label_encoder.fit_transform(df_prediction['Publisher'])
        df_prediction['Platform'] = label_encoder.fit_transform(df_prediction['Platform'])
        df_prediction['Genre'] = label_encoder.fit_transform(df_prediction['Genre'])

        # Split dataset into features and target variable
        features = ['Publisher', 'NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales', 'Global_Sales']
        X = df_prediction[features]
        y = df_prediction['Genre']


    print(f"Number of samples in X: {len(X)}, Number of samples in y: {len(y)}")

    # Split data into training and testing sets
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)  # , random_state=42

    # Initialize Decision Tree Classifier
    from sklearn.tree import DecisionTreeClassifier
    model = DecisionTreeClassifier()  # random_state=42

    # Initialize Another Classifiers:
    from sklearn.ensemble import RandomForestClassifier
    model2 = RandomForestClassifier()

    # Train the model
    model.fit(X_train, y_train)
    model2.fit(X_train, y_train)

    # Predictions
    predictions = model.predict(X_test)
    predictions2 = model2.predict(X_test)

    # Evaluation
    from sklearn.metrics import classification_report
    print(classification_report(y_test, predictions))
    print(classification_report(y_test, predictions2))
    from sklearn.metrics import accuracy_score
    print(accuracy_score(y_test, predictions))
    print(accuracy_score(y_test, predictions2))

    return "Decision Tree Classifier Accuracy: {}, Random Forest Classifier Accuracy: {}".format(accuracy_score(y_test, predictions), accuracy_score(y_test, predictions2))