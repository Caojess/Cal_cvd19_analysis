import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import seaborn as sns
import matplotlib.dates as mdates

# Load the data
data = pd.read_csv('datasets/vaccination.csv', parse_dates=['administered_date'])

# Filter out "All CA Counties" and "All CA and Non-CA Counties"
data = data[~data['county'].str.lower().isin(['all ca counties', 'all ca and non-ca counties'])]

# Convert the dates to year
data['year'] = data['administered_date'].dt.year

# Group by year and county to get cumulative data
grouped_data = data.groupby(['year', 'county']).agg({
    'cumulative_total_doses': 'max',
    'total_partially_vaccinated': 'max',
    'cumulative_fully_vaccinated': 'max',
    'cumulative_at_least_one_dose': 'max',
    'cumulative_up_to_date_count': 'max'
}).reset_index()

# Load the shape file for California counties
gdf = gpd.read_file('counties.shp')

# Merge the shape data with the vaccination data
merged = gdf.merge(grouped_data, left_on='NAME', right_on='county', how='left')

# Plot heatmap for each year
fig, axes = plt.subplots(nrows=len(merged['year'].unique()), figsize=(15, len(merged['year'].unique()) * 10))

for ax, (year, group) in zip(axes, merged.groupby('year')):
    group = group.to_crs(epsg=4326)
    group.plot(column='cumulative_total_doses', cmap='YlOrRd', linewidth=0.8, ax=ax, edgecolor='0.8', legend=True)
    ax.set_title(f'Vaccination Heatmap for {year}', fontdict={'fontsize': '15', 'fontweight' : '3'})
    ax.axis('off')

plt.tight_layout()
plt.show()

# Line plot to show trends over time
plt.figure(figsize=(15, 10))
sns.lineplot(data=data, x='administered_date', y='cumulative_total_doses', hue='county')
plt.title('Trends in Cumulative Total Doses Over Time by County')
plt.xlabel('Date')
plt.ylabel('Cumulative Total Doses')
plt.xticks(rotation=45)
plt.gca().xaxis.set_major_locator(mdates.YearLocator())
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

plt.tight_layout()
plt.show()

# Bar plot of total doses by county
total_doses_by_county = data.groupby('county')['cumulative_total_doses'].max().reset_index()
plt.figure(figsize=(15, 10))
sns.barplot(data=total_doses_by_county, x='cumulative_total_doses', y='county', palette='viridis')
plt.title('Total Doses Administered by County')
plt.xlabel('Cumulative Total Doses')
plt.ylabel('County')

plt.tight_layout()
plt.show()

# Stacked area plot of cumulative doses by county over time
data_sorted = data.sort_values('administered_date')
pivot_data = data_sorted.pivot_table(index='administered_date', columns='county', values='cumulative_total_doses', fill_value=0)
plt.figure(figsize=(15, 10))
pivot_data.plot.area(figsize=(15, 10), colormap='tab20')
plt.title('Cumulative Total Doses Over Time by County')
plt.xlabel('Date')
plt.ylabel('Cumulative Total Doses')
plt.xticks(rotation=45)
plt.legend(loc='upper left', bbox_to_anchor=(1.0, 1.0))

plt.tight_layout()
plt.show()
