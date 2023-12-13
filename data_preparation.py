import pandas as pd

# Reading data
df = pd.read_csv("VideoGamesSales.csv")

# -----------------------------------------------------------------------------------------------------
# Cleaning
# Drop rows with null values in the attributes/columns specified:
df = df.dropna(subset=['Genre'])
df = df.dropna(subset=['Platform'])
df = df.dropna(subset=['Year'])

# Find and get unique values of different attributes
unique_genres = df['Genre'].unique()
unique_platforms = df['Platform'].unique()
unique_years = df['Year'].unique()

# Create options for the dropdown as the dcc.Dropdown expects a list of dictionaries
dropdown_options_genres = [{'label': genre, 'value' : genre} for genre in unique_genres]
dropdown_options_platform = [{'label' : publisher, 'value' : publisher} for publisher in unique_platforms]
dropdown_options_years = [{'label': year, 'value': year} for year in unique_years]

# -----------------------------------------------------------------------------------------------------
# checking values
print(df.head())
print(unique_genres)
print(unique_platforms)

