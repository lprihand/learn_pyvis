import os
from pyvis.network import Network
import json 

cur_dir = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
file = f'{cur_dir}/alcuin_letters.json'

def get_data():
    with open(file, "r") as json_file:
        data = json.load(json_file)
        return (data["alcuin_letters"])
    
def map_data(letter_data):
    g = Network(height="1500px", width="100%", bgcolor="#222222", font_color="white")
    for letter in letter_data:
        ep = (letter["ep_num"])[0]
        mss = (letter["mss"])
        g.add_node(ep)
        for ms in mss:
            g.add_node(ms)
            g.add_edge(ep, ms)
    g.barnes_hut()
    g.show("letters.html", notebook=False)
    
epp_data = get_data()
map_data(epp_data)

#018786
