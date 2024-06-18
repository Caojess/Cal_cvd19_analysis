import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
import contextily as ctx
from matplotlib.colors import Normalize

# Load the data
file_path = 'datasets/covid_cases.csv'
covid_data = pd.read_csv(file_path)

# Convert the data to a long format
covid_data_melted = covid_data.melt(id_vars=["County", "State", "Country_Region"], 
                                    var_name="Date", 
                                    value_name="Cases")

# Convert the Date column to datetime format
covid_data_melted['Date'] = pd.to_datetime(covid_data_melted['Date'], format='%m/%d/%y')

# Filter data for California
california_data = covid_data_melted[covid_data_melted['State'] == 'California']

# Calculate the overall minimum and maximum cases for normalization
overall_min = california_data['Cases'].min()
overall_max = california_data['Cases'].max()

# Function to plot heatmap for a specific year
def plot_heatmap(year, ax, norm):
    yearly_data = california_data[california_data['Date'].dt.year == year]
    yearly_cases = yearly_data.groupby('County')['Cases'].sum().reset_index()

    # Load the California counties shapefile
    counties = gpd.read_file('counties.shp')

    # Filter for California counties
    california_counties = counties[counties['STATEFP'] == '06']  # California FIPS code is 06

    # Merge COVID data with the counties shapefile
    california_counties = california_counties.merge(yearly_cases, left_on='NAME', right_on='County', how='left')
    california_counties['Cases'] = california_counties['Cases'].fillna(0)  # Replace NaN with 0

    # Plotting with consistent color spectrum
    california_counties.plot(column='Cases', cmap='OrRd', linewidth=0.8, ax=ax, edgecolor='0.8', legend=False, norm=norm)
    
    ax.set_title(f'COVID-19 Cases in California - {year}')
    ax.axis('off')
    ctx.add_basemap(ax, crs=california_counties.crs.to_string(), source=ctx.providers.OpenStreetMap.Mapnik)

# Create normalization based on overall min and max values
norm = Normalize(vmin=overall_min, vmax=overall_max)

# Create heatmaps for each year from 2020 to 2024
fig, axes = plt.subplots(1, 5, figsize=(25, 10), sharex=True, sharey=True)
years = [2020, 2021, 2022, 2023]

for i, year in enumerate(years):
    plot_heatmap(year, axes[i], norm)

# Adjust colorbars
for ax in axes:
    cax = fig.add_axes([ax.get_position().x1 + 0.01, ax.get_position().y0, 0.02, ax.get_position().height])
    sm = plt.cm.ScalarMappable(cmap='OrRd', norm=norm)
    sm._A = []  # Create an empty array for the ScalarMappable
    fig.colorbar(sm, cax=cax)

plt.tight_layout()
plt.show()

# Additional Visualization 1: Trend Line of COVID-19 Cases Over Time for California
plt.figure(figsize=(14, 7))
california_data.groupby('Date')['Cases'].sum().cumsum().plot()
plt.title('Cumulative COVID-19 Cases Over Time in California')
plt.xlabel('Date')
plt.ylabel('Cumulative Cases')
plt.grid(True)
plt.show()

# Additional Visualization 2: Bar Plot of Total Cases by County
plt.figure(figsize=(14, 7))
total_cases_by_county = california_data.groupby('County')['Cases'].sum().sort_values(ascending=False)
total_cases_by_county.plot(kind='bar')
plt.title('Total COVID-19 Cases by County in California')
plt.xlabel('County')
plt.ylabel('Total Cases')
plt.show()

# Additional Visualization 3: Heatmap of Monthly Cases
california_data['YearMonth'] = california_data['Date'].dt.to_period('M')
monthly_cases = california_data.groupby(['YearMonth', 'County'])['Cases'].sum().unstack().fillna(0)

plt.figure(figsize=(14, 10))
sns.heatmap(monthly_cases.T, cmap='OrRd', cbar=True)
plt.title('Monthly COVID-19 Cases by County in California')
plt.xlabel('Month')
plt.ylabel('County')
plt.show()
