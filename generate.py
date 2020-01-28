#!/usr/bin/env python3

from res.functions import *

# list database
list_fuel = [ 'PSS', 'PETRON', ]
list_monthly = [ 'ETIQA', 'GROLIER', 'WEBE' , 'COWAY', ]
list_grocery = [ 'TF', 'GIANT', ]
list_fastfood = [ 'DOBUYO', 'MCDONALDS', 'SUSHI', 'FAMILYMART', ]
list_manjaku = [ 'MANJAKU', ]

label = ['FUEL', 'MONTHLY', 'GROCERY', 'FASTFOOD', 'MANJAKU']

# prepare dataset 
page_1 = get_txt_lines('out.txt', 53, 68)
page_2 = get_txt_lines('out.txt', 78, 89)
raw_data = page_1 + page_2 

fuel, fuel_total = categorize_data(raw_data, list_fuel)
monthly, monthly_total = categorize_data(raw_data, list_monthly) 
grocery, grocery_total = categorize_data(raw_data, list_grocery) 
fastfood, fastfood_total = categorize_data(raw_data, list_fastfood) 
manjaku, manjaku_total = categorize_data(raw_data, list_manjaku) 

# run code
data_1 = [fuel_total, monthly_total, grocery_total, fastfood_total, manjaku_total]

produce_graph_horizontal(data_1, '20_01', label)

produce_cli_output(data_1, label)
