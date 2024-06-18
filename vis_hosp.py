import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
import contextily as ctx
from matplotlib.colors import Normalize

# Load the data
file_path = 'datasets/covid_hosp.csv'
covid_data = pd.read_csv(file_path)

# Convert the Date column to datetime format
covid_data['todays_date'] = pd.to_datetime(covid_data['todays_date'])

# Filter data for California counties
# Note: Assuming all data is from California as the 'State' column is not present

# Calculate the overall minimum and maximum cases for normalization
overall_min = covid_data['hospitalized_covid_confirmed_patients'].min()
overall_max = covid_data['hospitalized_covid_confirmed_patients'].max()

def plot_heatmap(year, ax, norm):
    yearly_data = covid_data[covid_data['todays_date'].dt.year == year]
    yearly_cases = yearly_data.groupby('county')['hospitalized_covid_confirmed_patients'].sum().reset_index()

    # Load the California counties shapefile
    counties = gpd.read_file('counties.shp')

    # Filter for California counties
    california_counties = counties[counties['STATEFP'] == '06']  # California FIPS code is 06

    # Merge COVID data with the counties shapefile
    california_counties = california_counties.merge(yearly_cases, left_on='NAME', right_on='county', how='left')
    california_counties['hospitalized_covid_confirmed_patients'] = california_counties['hospitalized_covid_confirmed_patients'].fillna(0)  # Replace NaN with 0

    # Plotting with consistent color spectrum
    california_counties.plot(column='hospitalized_covid_confirmed_patients', cmap='OrRd', linewidth=0.8, ax=ax, edgecolor='0.8', legend=False, norm=norm)
    
    ax.set_title(f'{year}', fontsize=12)
    ax.axis('off')
    ctx.add_basemap(ax, crs=california_counties.crs.to_string(), source=ctx.providers.OpenStreetMap.Mapnik)

# Create normalization based on overall min and max values
norm = Normalize(vmin=overall_min, vmax=overall_max)

# Create heatmaps for each year from 2020 to 2024
fig, axes = plt.subplots(1, 5, figsize=(25, 10), sharex=True, sharey=True)
years = [2020, 2021, 2022, 2023, 2024]

for i, year in enumerate(years):
    plot_heatmap(year, axes[i], norm)

# Add a single colorbar at the bottom
cax = fig.add_axes([0.2, 0.1, 0.6, 0.02])
sm = plt.cm.ScalarMappable(cmap='OrRd', norm=norm)
sm._A = []  # Create an empty array for the ScalarMappable
fig.colorbar(sm, cax=cax, orientation='horizontal')

# Add a main title
plt.suptitle('Hospitalized COVID-19 Patients in California', fontsize=16, y=1.05)
plt.tight_layout(rect=[0, 0.2, 1, 0.95])
plt.show()

# Additional Visualization 1: ICU Hospitalizations vs ICU Available Beds
plt.figure(figsize=(14, 7))
icu_data = covid_data.groupby('todays_date').sum()
plt.plot(icu_data.index, icu_data['icu_covid_confirmed_patients'], label='ICU COVID Confirmed Patients')
plt.plot(icu_data.index, icu_data['icu_available_beds'], label='ICU Available Beds')
plt.title('ICU COVID-19 Confirmed Patients vs ICU Available Beds Over Time')
plt.xlabel('Date')
plt.ylabel('Number of Patients/Beds')
plt.legend()
plt.grid(True)
plt.show()

# Additional Visualization 2: Hospital COVID Confirmed vs Suspected Patients
plt.figure(figsize=(14, 7))
hospital_data = covid_data.groupby('todays_date').sum()
plt.plot(hospital_data.index, hospital_data['hospitalized_covid_confirmed_patients'], label='Hospitalized COVID Confirmed Patients')
plt.plot(hospital_data.index, hospital_data['hospitalized_suspected_covid_patients'], label='Hospitalized Suspected COVID Patients')
plt.title('Hospitalized COVID-19 Confirmed Patients vs Suspected Patients Over Time')
plt.xlabel('Date')
plt.ylabel('Number of Patients')
plt.legend()
plt.grid(True)
plt.show()
