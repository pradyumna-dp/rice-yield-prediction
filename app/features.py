import pandas as pd
import requests

def soil_data(district):
    df = pd.read_csv('fertilizer_list.csv')

    matching_row = df[df['DISTRICT'] == district].iloc[0]  

    row_dict = {'N': matching_row['N'], 'P': matching_row['P'], 'K': matching_row['K']}

    return row_dict

def weather(district):
    api_key = '8f48c41fdb2e9205be664e7721add142'

    api_url = f'https://api.openweathermap.org/data/2.5/weather?q={district}&appid={api_key}&units=metric'

    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        temperature = data['main']['temp']
        return temperature
    else:
        print('Error:', response.status_code)
        return 0

