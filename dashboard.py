import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set the Matplotlib style to dark background
plt.style.use('dark_background')

# Read the combined DataFrame from the CSV file
combined_df = pd.read_csv('dat/combined_data.csv')

# Add a sidebar for selecting the Wahlperiode
wahlperiode = st.sidebar.selectbox(
    'Wahlperiode auswählen',
    options=[19, 20],
    index=1
)

# Filter the DataFrame to include only votes for the selected Wahlperiode
filtered_df = combined_df[combined_df['Wahlperiode'] == wahlperiode]

# Combine the 'Name' and 'Vorname' columns to create a full name column
filtered_df['FullName'] = filtered_df['Vorname'] + ' ' + filtered_df['Name']

# Group by 'FullName' and calculate the total votes and 'nichtabgegeben' votes for each person
nicht_abgegeben = filtered_df.groupby('FullName').agg(
    total_votes=('nichtabgegeben', 'size'),
    nicht_abgegeben=('nichtabgegeben', 'sum'),
    partei=('Fraktion/Gruppe', 'first')
).reset_index()

# Sort by the sum of 'nichtabgegeben' votes
nicht_abgegeben = nicht_abgegeben.sort_values(by="nicht_abgegeben", ascending=False)

# Get the top 10 people with the most missed votes
top_10 = nicht_abgegeben.head(10)

# Display the DataFrame
st.markdown("<h1 id='analyse-der-verpassten-abstimmungen'>Analyse der verpassten Abstimmungen</h1>", unsafe_allow_html=True)

# Define the color map for parties
color_map = {
    'fraktionslos': 'grey',
    'spd': 'red',
    'afd': 'lightblue',
    'cdu/csu': 'black',
    'fdp': 'yellow',
    'die linke': 'magenta',
    'bsw': 'purple',
}

# Normalize party names to lowercase and remove trailing periods
top_10['partei'] = top_10['partei'].str.lower().str.rstrip('.')

# Plotting with seaborn
fig, ax = plt.subplots(figsize=(12, 6))
fig.patch.set_facecolor('#303030')  # Dark gray background
ax.set_facecolor('#303030')  # Dark gray background
sns.barplot(x='FullName', y='nicht_abgegeben', hue='partei', data=top_10, palette=color_map, ax=ax)
sns.despine()

# Remove the top and right spines
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Label the plot with increased font size
ax.set_title('Top 10 Personen mit den meisten verpassten Abstimmungen', color='white', fontsize=16)
ax.set_xlabel('', color='white', fontsize=14)  # Remove x-axis label
ax.set_ylabel('Anzahl der verpassten Abstimmungen', color='white', fontsize=14)

# Rotate the x-axis labels for readability and increase font size
plt.xticks(rotation=45, ha='right', color='white', fontsize=12)
plt.yticks(color='white', fontsize=12)

# Adjust layout to prevent label cut-off
plt.tight_layout()

# Display the plot in Streamlit
st.pyplot(fig)

# Add space between the plots
st.write("\n" * 3)

# New section for the second plot
st.markdown("<h1 id='diskutierte-themen-pro-monat'>Diskutierte Themen pro Monat</h1>", unsafe_allow_html=True)

# Read the votes with categories DataFrame from the CSV file
votes_with_categories_df = pd.read_csv('dat/votes_with_categories.csv')

# Convert the 'Date' column to datetime format
votes_with_categories_df['Date'] = pd.to_datetime(votes_with_categories_df['Date'], format='%d.%m.%Y')

# Extract the month and year from the 'Date' column
votes_with_categories_df['Month'] = votes_with_categories_df['Date'].dt.to_period('M')

# Group by 'Sitzungnr' and sum the categories
categories = ['Gesundheit', 'Einwanderung', 'Sicherheit', 'Energie', 'Wirtschaft', 'Rechtsreform', 'Außenpolitik', 'Regierungspolitik']
grouped_df = votes_with_categories_df.groupby(['Sitzungnr'])[categories].sum().reset_index()

# Group by 'Month' and sum the categories
monthly_df = votes_with_categories_df.groupby(['Month'])[categories].sum().reset_index()

# Calculate the percentage of each category for each month
monthly_df.set_index('Month', inplace=True)
monthly_percentage_df = monthly_df.div(monthly_df.sum(axis=1), axis=0) * 100

# Reset the index for plotting
monthly_percentage_df.reset_index(inplace=True)

# Plotting with seaborn
fig2, ax2 = plt.subplots(figsize=(12, 6))
monthly_percentage_df.set_index('Month').plot(kind='bar', stacked=True, ax=ax2, colormap='tab20')

# Remove the top and right spines
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

# Label the plot
ax2.set_title('Diskutierte Themen pro Monat')
ax2.set_xlabel('Monat')
ax2.set_ylabel('Prozentsatz')
plt.xticks(rotation=45, ha='right')

# Adjust layout to prevent label cut-off
plt.tight_layout()

# Display the plot in Streamlit
st.pyplot(fig2)