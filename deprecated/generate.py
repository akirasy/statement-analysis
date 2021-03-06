#!/usr/bin/env python3

from subprocess import run
from linecache import getline
from PIL import Image, ImageDraw, ImageFont

def pdf_to_text(input_pdf, output_txt):
    process = 'pdftotext' # from unix poppler package
    options = '-layout'
    run([process, options, input_pdf, output_txt])

def extract_pdf_data(filename, start, end):
    data_list = [ ]
    for i in range(start, end):
        line = getline(f'{filename}', i)
        line_split = line.split()
        item = f'{line_split[2]} {line_split[3]}'
        price = line_split[-1]
        data_list.append([item, price])
    return data_list

def categorize(raw_data, category_list):
    category = [ ]
    total = 0
    for i in raw_data:
        for j in category_list:
            if j in i[0]:
                category.append(i)
        #for j in catefory_list:
        #    if j not in i[0]:
        #        category.append(i)
    for i in category:
        total = total + float(i[1])
    # this returns 'list' and 'float'
    return [category, total]

def graph_vertical(data, output): 
    img = Image.new('RGB', [600,1024], '#ffffff')
    draw_img = ImageDraw.Draw(img)
    scale = 500/max(data)
    x = 0
    base = 800
    for i in data:
        x = x + 40 
        y = base - (i * scale) 
        draw_img.line((x,base,x,y), width=20, fill='#009933')
    img.save(f'{output}.png')

def graph_horizontal(data, output, label): 
    img = Image.new('RGB', [1024,600], '#ffffff')
    draw_img = ImageDraw.Draw(img)
    font = ImageFont.truetype('Lato-Bold.ttf', 17)
    draw_img.text((400,40), 'Credit Card Analysis', font=font, fill='#000000')
    scale = 500/max(data)
    y = 100
    base_graph = 300
    base_label = 10
    for i in data:
        y = y + 60 
        x = base_graph + (i * scale)
        draw_img.line((base_graph,y,x,y), width=40, fill='#009933')
    y = 100
    for i in label:
        y = y + 60
        draw_img.text((50,y), f'{i}', font=font, fill='#000000')
    y = 100
    for i in data:
        y = y + 60
        draw_img.text((180,y), f'RM {i}', font=font, fill='#000000')
    img.save(f'{output}.png')

def output_cli(total, label):
    for i, j in zip(label, total):
        print(f'{i} : {j}')

# list database
list_fuel = [ 'PSS', 'PETRON', ]
list_monthly = [ 'ETIQA', 'GROLIER', 'WEBE' , 'COWAY', ]
list_grocery = [ 'TF', 'GIANT', ]
list_fastfood = [ 'DOBUYO', 'MCDONALDS', 'SUSHI', 'FAMILYMART', ]
list_manjaku = [ 'MANJAKU', ]

label = ['FUEL', 'MONTHLY', 'GROCERY', 'FASTFOOD', 'MANJAKU']

# prepare dataset 
page_1 = extract_pdf_data('out.txt', 53, 68)
page_2 = extract_pdf_data('out.txt', 78, 89)
raw_data = page_1 + page_2 

fuel, fuel_total = categorize(raw_data, list_fuel)
monthly, monthly_total = categorize(raw_data, list_monthly) 
grocery, grocery_total = categorize(raw_data, list_grocery) 
fastfood, fastfood_total = categorize(raw_data, list_fastfood) 
manjaku, manjaku_total = categorize(raw_data, list_manjaku) 

# run code
data_1 = [fuel_total, monthly_total, grocery_total, fastfood_total, manjaku_total]

graph_horizontal(data_1, '20_01', label)

output_cli(data_1, label)

#pdf_to_text('file.pdf', 'new.txt')
