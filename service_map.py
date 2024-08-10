import os
from turtle import color
from pyvis.network import Network
import json 
import inspect
from token_manager import TokenManager
from io import StringIO
import pandas as pd
import matplotlib.pyplot as plt

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
cur_dir = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
file = f'{cur_dir}/alcuin_letters.json'

token_manager = TokenManager()
token_manager.load_token_storage(f"{currentdir}/token_storage.json")
validation = token_manager.check_token_expiry()

if validation == 2:
    token_manager.save_token_storage(f"{currentdir}/token_storage.json")

token = token_manager.get_token()

fullClassName = "service.Service"
filterExpression = ""
resultFilter = "serviceId","customerName","description","displayedName","id","numberOfSites"

apiresponse = token_manager.post_api(token, fullClassName, filterExpression, resultFilter)
json_bytes = bytes(apiresponse.text, encoding='utf-8')
data_api = StringIO(json_bytes.decode('utf-8'))
df = pd.read_json(data_api)

print(df)

# Define a function to categorize the service type based on the 'displayedName' column
def categorize_service(name):
    if "VPLS" in name:
        return "VPLS"
    elif "VPRN" in name:
        return "VPRN"
    elif "IES" in name:
        return "IES"
    elif "MIRROR" in name:
        return "MIRROR"
    elif "EPIPE" in name:
        return "EPIPE"
    else:
        return "N/A"

# Apply the function to create a new column 'serviceType'
df['serviceType'] = df['displayedName'].apply(categorize_service)

# Count the occurrences of each service type
service_counts = df['serviceType'].value_counts()

# # Plotting the pie chart
# plt.figure(figsize=(8, 8))
# plt.pie(service_counts, labels=service_counts.index, autopct='%1.1f%%', startangle=140)
# plt.title('Service Type Distribution')
# plt.show()



# # Define a function to filter out only VPRN services
# def filter_vprn_services(name):
#     return "VPRN" in name

# # Apply the function to create a new DataFrame for VPRN services only
# vprn_df = df[df['displayedName'].apply(filter_vprn_services)]

# # Ensure numberOfSites column is numeric
# vprn_df['numberOfSites'] = pd.to_numeric(vprn_df['numberOfSites'], errors='coerce')

# # Sort by numberOfSites in descending order and select top 10
# top_10_vprn_df = vprn_df.sort_values(by='numberOfSites', ascending=False).head(10)

# # Calculate the percentage of 'numberOfSites' for each VPRN service
# vprn_sites_percentage = vprn_df['numberOfSites'] / vprn_df['numberOfSites'].sum() * 100

# # Plotting the pie chart for VPRN services based on number of sites
# plt.figure(figsize=(8, 8))
# plt.pie(vprn_sites_percentage, labels=vprn_df['displayedName'], autopct='%1.1f%%', startangle=140)
# plt.title('VPRN Services Distribution by Number of Sites')
# plt.show()

df = df.drop(columns=['ies.Ies','vprn.Vprn','mirror.Mirror','vpls.Vpls','epipe.Epipe'])

# Filter out only VPRN services
vprn_df = df[df['displayedName'].str.contains("VPRN")]

# Ensure numberOfSites column is numeric
vprn_df['numberOfSites'] = pd.to_numeric(vprn_df['numberOfSites'], errors='coerce')

# Group by displayedName (VPRN ID) and sum the numberOfSites
aggregated_vprn_df = vprn_df.groupby('displayedName').sum().reset_index()

# Sort by numberOfSites in descending order and select top 10
top_10_vprn_df = aggregated_vprn_df.sort_values(by='numberOfSites', ascending=False).head(10)

# Define a function to format the labels with both percentage and number of sites
def autopct_format(values):
    def inner_autopct(pct):
        total = sum(values)
        val = int(round(pct * total / 100.0))
        return f'{pct:.1f}%\n({val} sites)'
    return inner_autopct

# Plotting the pie chart for top 10 VPRN services based on aggregated number of sites
plt.figure(figsize=(10, 8))
plt.pie(top_10_vprn_df['numberOfSites'], 
        labels=top_10_vprn_df['displayedName'], 
        autopct=autopct_format(top_10_vprn_df['numberOfSites']), 
        startangle=140)
plt.title('Top 10 VPRN Services by Aggregated Number of Sites')
plt.show()