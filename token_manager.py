import json
from datetime import datetime, timedelta
import urllib3
import requests
import os 
from dotenv import load_dotenv

# Get the current file path
cur_Path = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
# Get the parent directory path
par_Dir = os.path.abspath(os.path.join(cur_Path, os.pardir))
# Load environment variables from .env file located in the parent directory
env_path = os.path.join(cur_Path, '.env')
load_dotenv(dotenv_path=env_path)

# Get the file pattern from environment variables
token64 = os.getenv('TOKEN64')

class TokenManager:

    nfmp_MLQ2 = os.getenv('nfmp_mlq2')
    nfmp_ADAM = os.getenv('nfmp_adam')
    nsp_MLQ2 = os.getenv('nsp_mlq2')
    nsp_ADAM = os.getenv('nsp_adam')

    def __init__(self, token_storage=None):
        self.token_storage = token_storage or {}

    @classmethod
    def get_node(self, node_name):
        nodes = {
            'nfmp_MLQ2': self.nfmp_MLQ2,
            'nfmp_ADAM': self.nfmp_ADAM,
            'nsp_MLQ2': self.nsp_MLQ2,
            'nsp_ADAM': self.nsp_ADAM
        }
        return nodes.get(node_name, 'Node not found')
    

    def save_token_storage(self, file_path):
        with open(file_path, 'w') as file:
            json.dump(self.token_storage, file)

    def load_token_storage(self, file_path):
        with open(file_path, 'r') as file:
            self.token_storage = json.load(file)


    def generate_new_token(self):

        # ***get token***
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        payload = json.dumps({
        "grant_type": "client_credentials"
        })

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Basic {token64}'
        }

        try:
            url = f"https://{self.nsp_ADAM}/rest-gateway/rest/api/v1/auth/token"
            response = requests.request(
                "POST", url, headers=headers, data=payload, verify=False)
            response.raise_for_status()
            json_data = json.loads(response.text)
            new_token = json_data['access_token']

        except:
            url = f"https://{self.nsp_MLQ2}/rest-gateway/rest/api/v1/auth/token"
            response = requests.request(
                "POST", url, headers=headers, data=payload, verify=False)
            response.raise_for_status()
            json_data = json.loads(response.text)
            new_token = json_data['access_token']

        new_token = f"{new_token}"
        expiration_time = datetime.now() + timedelta(minutes=60)  # Assuming a 60-minute expiry for the token
        #print (expiration_time)

        # Save token and expiration time
        self.token_storage['token'] = new_token
        self.token_storage['expiration_time'] = expiration_time.isoformat()

        return new_token

    def get_token(self):
        # Check if token exists and is not expired
        if 'token' in self.token_storage and 'expiration_time' in self.token_storage:
        #if 'token' in self.token_storage:
            expiration_time = datetime.fromisoformat(self.token_storage['expiration_time'])
            #return expiration_time
            if expiration_time > datetime.now():
                return self.token_storage['token']
        else:
            # If token is expired or doesn't exist, generate a new one
            return self.generate_new_token()

    def check_token_expiry(self):
        # Check if the token is expired
        if 'expiration_time' in self.token_storage:
            expiration_time = datetime.fromisoformat(self.token_storage['expiration_time'])
            if expiration_time <= datetime.now():
                print("Token has expired. Generating a new token.")
                cir = 2
                self.generate_new_token()
                return cir
            
    def post_api(self,token,fullClassName, filterExpression, resultFilter):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        
        url = f'https://{self.nfmp_MLQ2}:8443/nfm-p/rest/api/v1/managedobjects/searchWithFilter'
        payload = json.dumps({"fullClassName":f"{fullClassName}",
                              "filterExpression":f"{filterExpression}",
                              "resultFilter": resultFilter
                              }) 
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}' 
        }
        
        apiresponse = requests.request("POST", url, headers=headers, data=payload, verify=False)
        # print (apiresponse.content)
        # apiresponse = apiresponse.text
        
        if (apiresponse.status_code == 500):
            url = f'https://{self.nfmp_ADAM}:8443/nfm-p/rest/api/v1/managedobjects/searchWithFilter'
            apiresponse = requests.request("POST", url, headers=headers, data=payload, verify=False)
            # apiresponse = apiresponse.text
        
        return apiresponse

    def executeMultiCli(self,token,cliCommand, nodeIP):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        
        url = f'https://{self.nfmp_MLQ2}:8443/nfm-p/rest/api/v2/netw/NetworkElement/executeMultiCli/network:{nodeIP}'
        payload = json.dumps(cliCommand) 
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}' 
        }
        
        apiresponse = requests.request("PUT", url, headers=headers, data=payload, verify=False)
        # print (apiresponse.content)
        # apiresponse = apiresponse.text

        if (apiresponse.status_code == 500):
            url = f'https://{self.nfmp_ADAM}:8443/nfm-p/rest/api/v1/managedobjects/searchWithFilter'
            apiresponse = requests.request("POST", url, headers=headers, data=payload, verify=False)
            # apiresponse = apiresponse.text
            
        return apiresponse
