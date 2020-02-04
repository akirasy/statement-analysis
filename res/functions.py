#!/usr/bin/env python3

from subprocess import run
from linecache import getline
from PIL import Image, ImageDraw, ImageFont

def convert_pdf_to_text(input_pdf, output_txt):
    process = 'pdftotext' # from unix poppler package
    options = '-layout'
    run([process, options, input_pdf, output_txt])

def get_txt_lines(filename, start, end):
    data_list = [ ]
    for i in range(start, end):
        line = getline(f'{filename}', i)
        line_split = line.split()
        item = f'{line_split[2]} {line_split[3]}'
        price = line_split[-1]
        data_list.append([item, price])
    return data_list

def extract_txt(filename):
    # get file date
    date_raw = getline(f'{filename}', 12)
    date_split = date_raw.split()
    date = f'{date_split[0]} {date_split[1]} {date_split[2]}'
    
    # get total statement balance
    total_raw = getline(f'{filename}', 21)
    total_split = total_raw.split()
    total = float(total_split[4].replace(',',''))

    # get item-price list
    item_price = [ ]
    for i in range(53, 68):
        line = getline(f'{filename}', i)
        line_split = line.split()
        item = f'{line_split[2]} {line_split[3]}'
        price = line_split[-1]
        item_price.append([item, price])
    for i in range(78, 93):
        line = getline(f'{filename}', i)
        line_split = line.split()
        if len(line_split) == 0:
            break
        item = f'{line_split[2]} {line_split[3]}'
        price = line_split[-1]            
        item_price.append([item, price])
    
    # return [list, string, float]
    return [item_price, date, total]
    #return item_price

def total_price(raw_data):
    total = 0
    for i in raw_data:
        if 'CR' not in i[1]:
            total = total + float(i[1].replace(',',''))
    return total

def categorize_data(raw_data, category_list):
    category = [ ]
    total = 0
    for i in raw_data:
        for j in category_list:
            if j in i[0]:
                category.append(i)
    for i in category:
        total = total + float(i[1])
    # this returns 'list' and 'float'
    #return [category, total]
    return total

def process_data(raw_data, all_list):
    processed_data = [ ]
    for i in all_list:
        data = categorize_data(raw_data, i)
        processed_data.append(data)
    other = total_price(raw_data) - sum(processed_data)
    processed_data.append(other)
    return processed_data

def produce_graph_vertical(data, output): 
    img = Image.new('RGB', [600,1024], '#ffffff')
    draw_img = ImageDraw.Draw(img)
    scale = 500/max(data)
    x = 0
    base = 800
    for i in data:
        x = x + 40 
        y = base - i * scale 
        draw_img.line((x,base,x,y), width=20, fill='#009933')
    img.save(f'{output}.png')

def draw_rectangle(obj_img, x, y, text_1, text_2, title_gap_x, font):
    width = 200
    height = 60
    obj_img.rectangle([x,y,x+width,y+height], outline='#000000')
    obj_img.text([x+title_gap_x,y+5], f'{text_1}', font=font, fill='#000000')
    obj_img.text([x+title_gap_x,y+20], f'{text_2}', font=font, fill='#000000')

def produce_graph_horizontal(data, output, label, date, total): 
    img = Image.new('RGB', [1024,600], '#ffffff')
    draw_img = ImageDraw.Draw(img)
    font = ImageFont.truetype('res/fonts/Lato-Bold.ttf', 19)
    draw_img.text((400,40), 'CREDIT CARD ANALYSIS', font=font, fill='#000000')

    draw_img.rectangle([100,100,100+200,100+60], outline='#000000')
    draw_img.text([100+40,100+5], 'Total Balance', font=font, fill='#000000')
    draw_img.text([100+60,100+30], f'RM{total}', font=font, fill='#000000')

    draw_img.rectangle([400,100,400+200,100+60], outline='#000000')
    draw_img.text([400+35,100+5], 'Statement Date', font=font, fill='#000000')
    draw_img.text([400+60,100+30], f'{date}', font=font, fill='#000000')

#    draw_rectangle(draw_img, 100, 100, 'Total Balance', 'RM 400', 40, font)
#    draw_rectangle(draw_img, 400, 100, 'Statement Date', 'RM 255', 36, font)

    scale = 600/max(data)
    y = 200
    base_graph = 300
    for i, j in zip(data, label):
        y = y + 40 
        x = base_graph + (i * scale)
        draw_img.line((base_graph,y,x,y), width=30, fill='#009933')
        draw_img.text((50,y-10), f'{j}', font=font, fill='#000000')
        draw_img.text((180,y-10), f'RM {round(i,2)}', font=font, fill='#000000')
    img.save(f'{output}.png')

def produce_cli_output(total, label):
    for i, j in zip(label, total):
        print(f'{i} : {round(j,2)}')
