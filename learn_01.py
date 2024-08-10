from logging import shutdown
from turtle import forward
from pyvis.network import Network
import json 
from pprint import pprint
import os 

cur_dir = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
file = f'{cur_dir}/160051_response.json'

def get_data():
    with open(file, "r") as json_file:
        data = json.load(json_file)
        return data

epp_data = get_data()

pprint (epp_data)
