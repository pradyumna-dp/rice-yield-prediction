import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

def predict_accuracy(district_name):
    # reading dataset
    df = pd.read_csv("dataset.csv")

    # Selecting District from user input
    df = df[df['DISTRICT_NAME'] == district_name]

    # label encoders to convert string value to unique numerical value [District name, Season]
    season = LabelEncoder()

    df['numeric_season'] = season.fit_transform(df['season'])

    """
    Conditions for temperature, ph, rainfall, Production 
    """

    df['T'] = 0

    df.loc[df['temperature'] < 27, 'T'] = 1

    df['pH'] = 0

    df.loc[abs(df['ph'] - 7) < 0.1, 'pH'] = 1

    df['Rain'] = 0

    df.loc[(df['rainfall'] > 70) & (df['season'] == 'Rabi'), 'Rain'] = 1
    df.loc[(df['rainfall'] > 300) & (df['season'] == 'Kharif'), 'Rain'] = 1
    df.loc[(df['rainfall'] > 100) & (df['season'] == 'Summer'), 'Rain'] = 1
    """
    end of conditions 
    """

    # Dropping modified columns
    district_data = df.drop(
        columns=['ph', 'rainfall', 'temperature', 'DISTRICT_NAME', 'season', 'Production'])

    y = district_data['Prod']
    y = y.astype('int', errors='ignore')
    X = district_data.drop(['Prod'], axis=1)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)


    # Create a decision tree classifier and fit the model on the training data
    dtc = DecisionTreeClassifier()
    dtc.fit(X_train, y_train)

    # Evaluate the performance of the decision tree model on the testing data
    y_pred = dtc.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)*100
    # print('Accuracy:', accuracy_score(y_test, y_pred)*100)
    return accuracy
