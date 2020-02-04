#!/usr/bin/env python3

from res.functions import *

# set database
list_fuel = [
        'PSS', 'PETRON',
        ]
list_monthly = [
        'ETIQA', 'GROLIER',
        'WEBE' , 'COWAY',
        ]
list_grocery = [
        'TF', 'GIANT',
        ]
list_fastfood = [
        'DOBUYO', 'MCDONALDS',
        'SUSHI', 'FAMILYMART',
        ]
list_manjaku = [
        'MANJAKU',
        ]
list_interest = [
        'MGMT',
        ]
label = [
        'FUEL', 
        'MONTHLY', 
        'GROCERY', 
        'FASTFOOD', 
        'MANJAKU', 
        'INTEREST',
        'OTHERS',
        ]

all_list = [
        list_fuel,
        list_monthly,
        list_grocery,
        list_fastfood,
        list_manjaku,
        list_interest,
        ]

# prepare dataset 
raw_data, date, total = extract_txt('out.txt')

# run code
processed_data = process_data(raw_data, all_list)
produce_graph_horizontal(processed_data, '20_01', label, date, total)
produce_cli_output(processed_data, label)

# try code functions and run
def try_code():
    for i, j in zip(label, processed_data):
        print(f'{i} : RM{j}')
#try_code()
