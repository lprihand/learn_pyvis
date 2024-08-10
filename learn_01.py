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

/configure
    filter
        ip-filter 1700 name "1700" create
            default-action forward
            entry 1 create
                match protocol icmp
                exit
                log 192
                action
                    forward
                exit
            exit
            entry 10 create
                match protocol *
                exit
                log 192
                action
                    forward
                exit
            exit

/configure
        epipe 11498 name "NR_EU_Traffic_VPWS" customer 1 create
            description "NR_EU_Traffic_VPWS"
            sap lag-713:0.* create
                ingress filter ip 1700









            sap lag-713:0.* create
                shutdown
                description "NR_EU_Traffic_VPWS CRQ000003177688 18-Dec-2023"
                ingress
                    scheduler-policy "Enterprise_Scheduler"
                    scheduler-override
                        scheduler "Enterprise_Scheduler_T1" create
                        exit
                    exit
                    qos 13
                exit
                egress
                    scheduler-policy "Enterprise_Scheduler"
                    scheduler-override
                        scheduler "Enterprise_Scheduler_T1" create
                        exit
                    exit
                    qos 13
                exit
                collect-stats
            exit


sap lag-713:0.* shutdown
no sap lag-713:0.*
            sap lag-713:40.0 create
                description "NR_EU_Traffic_VPWS CRQ000003177688 18-Dec-2023"
                ingress
                    scheduler-policy "Enterprise_Scheduler"
                    scheduler-override
                        scheduler "Enterprise_Scheduler_T1" create
                        exit
                    exit
                    qos 13
                exit
                egress
                    scheduler-policy "Enterprise_Scheduler"
                    scheduler-override
                        scheduler "Enterprise_Scheduler_T1" create
                        exit
                    exit
                    qos 13
                exit
                collect-stats
                no shutdown
            exit





            sap lag-713:0.* create
                description "NR_EU_Traffic_VPWS CRQ000003177688 18-Dec-2023"
                ingress
                    scheduler-policy "Enterprise_Scheduler"
                    scheduler-override
                        scheduler "Enterprise_Scheduler_T1" create
                        exit
                    exit
                    qos 13
                exit
                egress
                    scheduler-policy "Enterprise_Scheduler"
                    scheduler-override
                        scheduler "Enterprise_Scheduler_T1" create
                        exit
                    exit
                    qos 13
                exit
                collect-stats
                no shutdown
            exit