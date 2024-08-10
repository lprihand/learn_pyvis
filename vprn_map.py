import os
from turtle import color
from pyvis.network import Network
import json 
import inspect
from token_manager import TokenManager
from io import StringIO
import pandas as pd


currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
cur_dir = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
file = f'{cur_dir}/alcuin_letters.json'

token_manager = TokenManager()
token_manager.load_token_storage(f"{currentdir}/token_storage.json")
validation = token_manager.check_token_expiry()

if validation == 2:
    token_manager.save_token_storage(f"{currentdir}/token_storage.json")

token = token_manager.get_token()

vrf_id = '6036'

fullClassName = "vprn.Site"
filterExpression = f"serviceId = {vrf_id}"
resultFilter = "serviceId", "siteId"#,"description","administrativeState","operationalState","displayedName","numberOfAccessInterfaces"

apiresponse = token_manager.post_api(token, fullClassName, filterExpression, resultFilter)
json_bytes = bytes(apiresponse.text, encoding='utf-8')
data_api = StringIO(json_bytes.decode('utf-8'))
df = pd.read_json(data_api)

# Load the JSON file
with open(f'{currentdir}/device.json', 'r') as file:
    device_data = json.load(file)

# Create a mapping dictionary
site_mapping = {item['siteId']: item['siteName'] for item in device_data}
site_mapping2 = {item['siteId']: item['reachability'] for item in device_data}

# Map the siteName to the DataFrame
df['siteName'] = df['siteId'].map(site_mapping)
df['reachability'] = df['siteId'].map(site_mapping2)

print(df)


fullClassName = "service.L3AccessInterface"
filterExpression = f"serviceId = {vrf_id}"
resultFilter = "displayedName","primaryIPv4Address", "serviceId", "nodeName","nodeId","operationalState","l3InterfaceDescription"

apiresponse = token_manager.post_api(token, fullClassName, filterExpression, resultFilter)
json_bytes = bytes(apiresponse.text, encoding='utf-8')
data_api = StringIO(json_bytes.decode('utf-8'))
df2 = pd.read_json(data_api)

def map_data(data_df, data_df2):
    g = Network(height="1500px", width="100%", bgcolor="#222222", font_color="white", select_menu=True, filter_menu=True)
    
    # letters = string.ascii_uppercase
    # # Generate all two-letter combinations
    # two_letter_combinations = [''.join(pair) for pair in itertools.product(letters, repeat=2)]

    vrf_node = str(df["serviceId"][0])
    print (vrf_node)
    # Add the result_id node with a label and larger size
    g.add_node(vrf_node, 
               label=vrf_node, 
               size=50, 
               color= 'purple', # Adjust size as needed
               font=dict(size=100, color='white'),  # Adjust font size and color
            #    shape='ellipse',  # Ensures the node is circular
               title=vrf_node
               )  # Optional: Display as tooltip

    for name, reach in zip(df.siteName, df.reachability):
        edge_color = '#f07878' if reach == 'up' else 'red'
        g.add_node(name, 
                    color=edge_color, 
                    size=30
                    # label="Router", 
                    # shape='icon', 
                    # icon={
                    #         "face": 'FontAwesome',
                    #         "code": '\uf796',  # Unicode for the router icon
                    #         "size": 30,        # Size of the icon
                    #         "color": edge_color   # Color of the icon
                    #     }
                    )
        g.add_edge(vrf_node, name)

    for interface, name, address, state, desc in zip(df2.displayedName, df2.nodeName, df2.primaryIPv4Address, df2.operationalState, df2.l3InterfaceDescription):
        int_add = interface+':'+address
        edge_color = 'green' if state == 'serviceUp' else 'red'
        g.add_node(int_add, title=str(desc), size=15)
        g.add_edge(name, int_add, color=edge_color)

    g.barnes_hut
    g.show("service_mapping.html", notebook=False)

map_data(df, df2)