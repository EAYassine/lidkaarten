from dotenv import load_dotenv
import os
from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import numpy as np
import requests
from io import BytesIO

load_dotenv()

def maak_lidkaarten(leden_path,template_path,download_path):
    leden = pd.read_fwf(leden_path) # reads txt file with each member on separate line 
    template = Image.open(template_path) # reads pdf of membership card template

    leden = pd.read_fwf(leden_path,header=None)[0].values.tolist() # reads txt file with each member on separate line 

    w, h = template.size

    req_fradmit = requests.get("https://github.com/xiayukun/font/blob/2eba79067a58542b8ec49ef4fd36f04d84701ca1/FRADMIT.TTF?raw=true")
    req_fradm = requests.get("https://github.com/xiayukun/font/blob/2eba79067a58542b8ec49ef4fd36f04d84701ca1/FRADM.TTF?raw=true")

    naam_font = ImageFont.truetype(BytesIO(req_fradmit.content),h/8.5)
    lidnummer_font = ImageFont.truetype(BytesIO(req_fradmit.content),h/15)

    titel_jaar = Image.new('RGBA', (int(h),int(h/3)))
    dr = ImageDraw.Draw(titel_jaar)
    titel_font = ImageFont.truetype(BytesIO(req_fradm.content), h/7.5)
    jaar_font = ImageFont.truetype(BytesIO(req_fradm.content), h/21)

    titel = 'LIDKAART'
    jaar = '2023-2024' 

    dr.text((0, 0), titel, font=titel_font, fill='white')
    dr.text((w/2.9,w/23), jaar, font=jaar_font, fill='white')
    titel_jaar = titel_jaar.rotate(90,  expand=1)

    lidkaarten = []

    for i,lid in enumerate(leden):
        lidnummer = i + 1
        lidkaart = Image.open(template_path) # reads pdf of membership card template
        lidkaart.paste(titel_jaar, (int(w/20),int(-w/25)), titel_jaar)
        naam_nummer = ImageDraw.Draw(lidkaart)
        naam_nummer.text((w*0.232,w*0.25), lid, fill='black', font=naam_font)
        naam_nummer.text((w*0.235,w*0.35),f'Lidnummer {str(lidnummer)}', fill='black', font=lidnummer_font)
        lidkaarten.append(lidkaart)
    
        template = Image.open(template_path)
        
        template.save(os.path.join(download_path, 'lidkaarten.pdf'), save_all=True, append_images=lidkaarten)
    
    return None
