import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Read the CSV file
df = pd.read_csv('dat/votes_with_categories.csv')

# Convert the 'Date' column to datetime format
df['Date'] = pd.to_datetime(df['Date'], format='%d.%m.%Y')

# Extract the month and year from the 'Date' column
df['Month'] = df['Date'].dt.to_period('M')

# Group by 'Sitzungnr' and sum the categories
categories = ['Gesundheit', 'Einwanderung', 'Sicherheit', 'Energie', 'Wirtschaft', 'Rechtsreform', 'Außenpolitik', 'Regierungspolitik']
grouped_df = df.groupby(['Sitzungnr'])[categories].sum().reset_index()

# Group by 'Month' and sum the categories
monthly_df = df.groupby(['Month'])[categories].sum().reset_index()

# Calculate the percentage of each category for each month
monthly_df.set_index('Month', inplace=True)
monthly_percentage_df = monthly_df.div(monthly_df.sum(axis=1), axis=0) * 100

# Reset the index for plotting
monthly_percentage_df.reset_index(inplace=True)

# Plotting with seaborn
fig, ax = plt.subplots(figsize=(12, 6))
monthly_percentage_df.set_index('Month').plot(kind='bar', stacked=True, ax=ax, colormap='tab20')

# Label the plot
ax.set_title('Topics Discussed Each Month')
ax.set_xlabel('Month')
ax.set_ylabel('Percentage')
plt.xticks(rotation=45, ha='right')

# Adjust layout to prevent label cut-off
plt.tight_layout()

# Display the plot in Streamlit
st.pyplot(fig)