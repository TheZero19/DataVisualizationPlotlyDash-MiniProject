import pandas as pd

df_prediction = pd.read_csv("VideoGamesSales.csv")
df_prediction.info()

# Drop rows with null values in specific columns
# columns_to_check = ['Genre', 'Platform', 'NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales', 'Global_Sales']
# df = df.dropna(subset=columns_to_check)

df_prediction = df_prediction[df_prediction["Genre"].isin(["Action", "Role-Playing"])] # this won't work: # df_prediction = df_prediction[df_prediction["Genre"] == ("Action" or "Role-Playing")]
df_prediction.info()

# Encode categorical variables
from sklearn.preprocessing import LabelEncoder
label_encoder = LabelEncoder()
df_prediction['Publisher'] = label_encoder.fit_transform(df_prediction['Publisher'])
df_prediction['Platform'] = label_encoder.fit_transform(df_prediction['Platform'])
df_prediction['Genre'] = label_encoder.fit_transform(df_prediction['Genre'])

# Split dataset into features and target variable
features = ['Publisher', 'Genre', 'NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales', 'Global_Sales']
X = df_prediction[features]
y = df_prediction['Genre']

# Split data into training and testing sets
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2) # , random_state=42

# Initialize Decision Tree Classifier
from sklearn.tree import DecisionTreeClassifier
model = DecisionTreeClassifier() # random_state=42

# Train the model
model.fit(X_train, y_train)

# Predictions
predictions = model.predict(X_test)

# Evaluation
from sklearn.metrics import classification_report
print(classification_report(y_test, predictions))
from sklearn.metrics import accuracy_score
print(accuracy_score(y_test, predictions))