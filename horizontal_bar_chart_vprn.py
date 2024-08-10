import pandas as pd
import matplotlib.pyplot as plt
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



# Define a function to filter out only VPRN services
def filter_vprn_services(name):
    return "VPRN" in name

# Apply the function to create a new DataFrame for VPRN services only
vprn_df = df[df['displayedName'].apply(filter_vprn_services)]

# Ensure numberOfSites column is numeric
vprn_df['numberOfSites'] = pd.to_numeric(vprn_df['numberOfSites'], errors='coerce')

# Sort the DataFrame by numberOfSites for better visualization
vprn_df = vprn_df.sort_values(by='numberOfSites', ascending=False)

# Plotting the horizontal bar chart for VPRN services based on number of sites
plt.figure(figsize=(10, 8))
plt.barh(vprn_df['displayedName'], vprn_df['numberOfSites'], color='skyblue')
plt.xlabel('Number of Sites')
plt.ylabel('VPRN Services')
plt.title('VPRN Services Distribution by Number of Sites')
plt.gca().invert_yaxis()  # Invert y-axis to show the largest on top
plt.show()
