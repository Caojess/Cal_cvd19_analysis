import pandas as pd
from datetime import timedelta
import requests

# Function to download and read the dataset with SSL verification turned off
def fetch_covid_data(url):
    response = requests.get(url, verify=False)
    with open('time_series_covid19_confirmed_US.csv', 'wb') as file:
        file.write(response.content)
    df = pd.read_csv('time_series_covid19_confirmed_US.csv')
    return df

# Function to process the data
def process_data(df):
    # Melt the dataframe to have date, state, and cases columns
    df = df.melt(id_vars=['Province_State'], var_name='date', value_name='cases')
    df['date'] = pd.to_datetime(df['date'])

    # Calculate weekly cases
    df = df.groupby(['Province_State', pd.Grouper(key='date', freq='W-MON')])['cases'].sum().reset_index().sort_values('date')
    df.columns = ['State', 'week_start', 'cases']
    df['week_end'] = df['week_start'] + timedelta(days=6)

    return df

# Function to write the processed data to a text file
def write_to_text(df, filename):
    output = ""
    for _, row in df.iterrows():
        output += f"{row['week_start'].date()} to {row['week_end'].date()}, {row['state']}, {row['cases']}\n"

    with open(filename, 'w') as file:
        file.write(output)

    print(f"Data has been written to {filename}")

# Main function to run the program
def main():
    url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv'
    df = fetch_covid_data(url)
    processed_df = process_data(df)
    write_to_text(processed_df, 'covid_weekly_cases.txt')

# Run the program
if __name__ == "__main__":
    main()
