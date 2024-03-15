import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib as mpl

# Path to your Excel file
file_path = 'Database Nanasala - Situation Analysis.csv'
data = pd.read_csv(file_path)

unique_values = data['Challenges and Difficulties '].unique()

# Set the visual style
# sns.set(style="whitegrid")

# Analysis 1: Operational Status of Centers
status_counts = data['Status'].value_counts()

labels = status_counts.index
sizes = status_counts.values
# Optional: Define colors for each status and whether any slice should be "exploded" (popped out)
colors = plt.cm.Pastel1(range(len(labels)))  # Use a colormap for diversity & accessibility
# Find the index for "Operating" status
operating_index = list(labels).index('Operating') if 'Operating' in labels else None

# Create explode list
explode = [0.1 if i == operating_index else 0 for i in range(len(labels))]

# Increase the font size
# mpl.rcParams['font.size'] = 0  # Adjust this value as needed

# Create pie chart
plt.figure(figsize=(8, 8))
plt.pie(sizes, explode=explode, colors=colors, autopct='%1.0f%%', shadow=True, startangle=140)
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle

plt.title('Operational Status of Nenasala Centers')
plt.show()

# Analysis 2: Distribution by District
district_counts = data['District '].value_counts().head(10).reset_index()  # Top 10 districts for simplicity
district_counts.columns = ['Number of Centers', 'District']
# Plot for Distribution by District
plt.figure(figsize=(10, 8))
sns.barplot(y='Number of Centers', x='District', data=district_counts, palette="rocket", orient='h')
plt.title('Top 10 Districts by Number of Nenasala Centers')
plt.xticks(rotation=45, ha="right")
# plt.gca().invert_xaxis()
plt.show()

# Analysis 3: Percentage of closed centers for each district
closed_centers = data[data['Status'].str.contains("Closed", case=False, na=False)]
closed_counts = closed_centers['District '].value_counts()
total_counts = data['District '].value_counts()
closed_percentage_series = (closed_counts / total_counts) * 100
closed_percentage = closed_percentage_series.reset_index()
closed_percentage.columns = ['District', 'Percentage of Closed Centers']
# Plot the percentage of closed centers for each district
plt.figure(figsize=(10, 8))
sns.barplot(x='District', y='Percentage of Closed Centers', data=closed_percentage, palette="muted")
plt.title('Percentage of Closed Nenasala Centers in Each District')
plt.xticks(rotation=45, ha="right")
plt.show()

# Analysis 4: Distribution of Centers by Type of Area
data['Type of area normalized'] = data['Type  of area '].str.strip().str.lower()
sentence_case_mapping = {v: k for k, v in data.dropna(subset=['Type  of area ']).set_index('Type  of area ')['Type of area normalized'].items()}
data['Type of area for display'] = data['Type of area normalized'].map(sentence_case_mapping)
data['Type of area for display'] = data['Type of area for display'].replace('-', 'Unknown')
type_of_area = data['Type of area for display'].value_counts().head(5).reset_index()
type_of_area.columns = ['Type of area for display', 'Count']
sns.barplot(data=type_of_area, y='Type of area for display', x='Count', hue='Count', orient='h')

# Enhancing the plot with titles and labels
plt.title('Status Distribution by Type of Area')
plt.xlabel('Type of Area')
plt.ylabel('Count')
plt.xticks(rotation=45)  # Rotating the x-axis labels for better readability
plt.legend(title='Status', bbox_to_anchor=(1.05, 1), loc='upper left')  # Moving the legend outside the plot

plt.tight_layout()  # Adjust layout to make room for the rotated x-axis labels and legend
plt.show()

# Analysis 5: Distribution of Centers by Type of Area (Percentages)
# Create the bar plot
area_counts = data['Type of area for display'].value_counts()
area_percentages = area_counts / area_counts.sum() * 100
# Labels are the unique values from 'Type of area '
labels = area_percentages.index
# Sizes are the percentages calculated previously
sizes = area_percentages.values
# Optional: Define colors for each slice
colors = plt.cm.tab20c.colors

# Create pie chart
plt.figure(figsize=(8, 8))
wedges, texts, autotexts = plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140, pctdistance=0.85)

# Draw a circle at the center of pie to make it look like a donut
centre_circle = plt.Circle((0,0),0.70,fc='white')
fig = plt.gcf()
fig.gca().add_artist(centre_circle)

# Equal aspect ratio ensures that pie is drawn as a circle
plt.axis('equal')

# Customize the font size
plt.setp(texts, size=8)
plt.setp(autotexts, size=8, weight="bold")

plt.title('Distribution of Centers by Type of Area (Percentages)', pad=20)
plt.show()

# Analysis 6: Average Number of Functional Computers by Center Status
# Step 0: Replace "-" with 0 in the relevant columns
data['Computers - Functional -ICTA'] = pd.to_numeric(data['Computers - Functional -ICTA'].replace('-', 0), errors='coerce')
data['Computer - Functional - Non ICTA'] = pd.to_numeric(data['Computer - Functional - Non ICTA'].replace('-', 0), errors='coerce')

data['Total Functional Computers'] = data['Computers - Functional -ICTA'] + data['Computer - Functional - Non ICTA']

# Calculate the average total functional computers by status
average_computers_by_status = data.groupby('Status')['Total Functional Computers'].mean().reset_index()

# Now let's plot this using seaborn's barplot
# sns.set(style="whitegrid")
plt.figure(figsize=(10, 6))
sns.barplot(x='Status', y='Total Functional Computers', data=average_computers_by_status)

plt.title('Average Number of Functional Computers by Center Status')
plt.xlabel('Center Status')
plt.ylabel('Average Number of Functional Computers')

plt.show()

# Analysis 7: Revenue Sufficiency by Type of Area (Percentage)
data['6.2 Revenue Sufficient'] = data['6.2 Revenue Sufficient'].str.strip().str.replace('-', 'Unknown')
# Step 1: Calculate the counts
counts = data.groupby(['Type of area for display', '6.2 Revenue Sufficient']).size().reset_index(name='counts')

# Step 2: Calculate total counts for each 'Type of area '
total_counts = data.groupby('Type of area for display').size().reset_index(name='total_counts')

# Merge the total counts back to the original counts DataFrame
counts = pd.merge(counts, total_counts, on='Type of area for display')

# Step 3: Calculate the percentages
counts['percentage'] = (counts['counts'] / counts['total_counts']) * 100

# Step 4: Plot these percentages using a bar plot
plt.figure(figsize=(10, 6))
sns.barplot(data=counts, x='Type of area for display', y='percentage', hue='6.2 Revenue Sufficient')

# Customizing the plot
plt.title('Revenue Sufficiency by Type of Area (Percentage)')
plt.xlabel('Type of Area')
plt.ylabel('Percentage')
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()

# Assuming 'data' is your DataFrame
revenue_sufficient_counts = data['6.2 Revenue Sufficient'].value_counts()
revenue_sufficient_percentages = (revenue_sufficient_counts / revenue_sufficient_counts.sum()) * 100
labels = revenue_sufficient_percentages.index
sizes = revenue_sufficient_percentages.values
colors = plt.cm.tab20c.colors  # Use a colormap for diverse colors

# Create pie chart
plt.figure(figsize=(8, 8))
wedges, texts, autotexts = plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)

# Draw a circle at the center to make it a donut chart (optional)
centre_circle = plt.Circle((0,0),0.70,fc='white')
fig = plt.gcf()
fig.gca().add_artist(centre_circle)

# Equal aspect ratio ensures that pie is drawn as a circle
plt.axis('equal')

plt.title('Revenue Sufficiency Percentages', pad=20)
plt.setp(texts, size=8)
plt.setp(autotexts, size=8, weight="bold")
plt.show()