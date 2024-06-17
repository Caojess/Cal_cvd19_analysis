import pandas as pd

# Load the dataset
input_file = 'time_series_covid19_confirmed_US.csv'
output_file = 'cleaned_covid_data.txt'

# Read the CSV file
df = pd.read_csv(input_file)

# Drop the specified columns
columns_to_drop = ['UID', 'iso2', 'iso3', 'code3', 'FIPS', 'Lat', 'Long_', 'Combined_Key']
df_cleaned = df.drop(columns=columns_to_drop)

# Save the cleaned data to a text file
df_cleaned.to_csv(output_file, sep='\t', index=False)

print(f"Cleaned data has been written to {output_file}")

