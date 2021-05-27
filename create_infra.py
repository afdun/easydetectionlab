import os
import sys
from common_functions import add_boxes
from modify_infra import modify_infra

def create_infra():
    print("\n-----------------------------------------------------------")
    print("-------------- CREER INFRASTRUCTURE -----------------------")
    print("------------------------------------------------------------\n")
    json_file = {}
    json_file = add_boxes(json_file)
    print(json_file)
    modify_infra(json_file)

create_infra()