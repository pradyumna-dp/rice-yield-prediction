import pandas as pd
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split

def predict_production(district_name, year):
    # Load data from a CSV file
    data = pd.read_csv('dataset.csv')
    data = data[data['DISTRICT_NAME'] == district_name]

    if year in data['Crop_Year'].values:
        # Display the production data for the year
        production = data.loc[data['Crop_Year'] == year, 'Production'].iloc[0]
        print('Actual production for year {}: {}'.format(year, production))
        return production
    else:
        avg_area = data['Area'].mean()
        # Split the data into training and testing sets
        X = data[['Crop_Year','Area']]
        y = data['Production']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Create a decision tree regressor object
        model = DecisionTreeRegressor(max_depth=3)

        # Fit the model to the training data
        model.fit(X_train, y_train)

        # Predict the production for the year
        new_data = [[year,avg_area]]
        production = model.predict(new_data)[0]
        print('Predicted production for year {}: {}'.format(year, production))
        return production