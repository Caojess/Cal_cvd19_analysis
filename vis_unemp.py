import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
file_path = 'datasets/unemployment.csv'
df = pd.read_csv(file_path)

# Convert the 'Date' column to datetime format
df['Date'] = pd.to_datetime(df['Date'])

# Set the 'Date' column as the index
df.set_index('Date', inplace=True)

# Plotting the trend of seasonally adjusted and not seasonally adjusted unemployment rates over time
plt.figure(figsize=(12, 6))
plt.plot(df.index, df['Seasonally Adjusted'], label='Seasonally Adjusted', color='blue')
plt.plot(df.index, df['Not Seasonally Adjusted'], label='Not Seasonally Adjusted', color='orange')
plt.xlabel('Date')
plt.ylabel('Unemployment Rate')
plt.title('Unemployment Rate Trends in California')
plt.legend()
plt.grid(True)
plt.show()

# Plotting the average unemployment rates by month to observe seasonal patterns
df['Month'] = df.index.month
monthly_avg = df.groupby('Month')[['Seasonally Adjusted', 'Not Seasonally Adjusted']].mean()

plt.figure(figsize=(12, 6))
monthly_avg.plot(kind='bar', ax=plt.gca())
plt.xlabel('Month')
plt.ylabel('Average Unemployment Rate')
plt.title('Average Monthly Unemployment Rates in California')
plt.xticks(rotation=0)
plt.legend(title='Rate Type')
plt.grid(True)
plt.show()
