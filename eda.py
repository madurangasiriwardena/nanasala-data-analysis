import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.impute import SimpleImputer

# Load the dataset
df = pd.read_csv('Database Nanasala - Situation Analysis.csv')

# Basic data cleaning and preprocessing
# Assuming 'operational_status' and 'revenue_status' are your target variables
# Convert categorical variables to numerical
df['location'] = df['Type  of area '].apply(lambda x: 1 if x == 'rural' else 0)
encoder = LabelEncoder()
df['6.2 Revenue Sufficient'] = df['6.2 Revenue Sufficient'].str.strip().str.replace('-', 'Unknown')
df['operational_status'] = df['Status']

df['Computers - Functional -ICTA'] = pd.to_numeric(df['Computers - Functional -ICTA'].str.strip().replace('-', 0), errors='coerce')
df['Computer - Functional - Non ICTA'] = pd.to_numeric(df['Computer - Functional - Non ICTA'].str.strip().replace('-', 0), errors='coerce')
df['Total Functional Computers'] = df['Computers - Functional -ICTA'] + df['Computer - Functional - Non ICTA']
df['Total Functional Computers'] = df['Total Functional Computers'].fillna(0)

# Relationship between number of computers and operational status
sns.boxplot(x='operational_status', y='Total Functional Computers', data=df)
plt.show()

sns.scatterplot(x='6.2 Revenue Sufficient', y='Total Functional Computers', data=df)
plt.title('Number of Computers vs Revenue')
plt.xlabel('Revenue')
plt.ylabel('Number of Computers')
plt.show()
