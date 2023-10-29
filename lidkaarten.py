from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import numpy as np
import PySimpleGUI as sg
import os

layout = [
    [sg.Text("Upload een excel bestand met in de eerste kolom de namen van de leden")],
    [sg.Text("      - Bestandstype: .xlsx")],
    [sg.InputText(key="LEDENLIJST_BROWSE"), sg.FileBrowse("Browse")],
    [sg.Button("Upload",key = 'uploadbutton1')],
    [sg.Text("Upload een foto van een template voor de lidkaarten")],
    [sg.Text("      - Bestandstype: .png")],
    [sg.Text("      - Aspect ratio: 16:9")],
    [sg.InputText(key="TEMPLATE_BROWSE"), sg.FileBrowse("Browse")],
    [sg.Button("Upload",key = 'uploadbutton2')],
    [sg.Text("Kies waar je de lidkaarten wil opslaan en klik op op 'Download'")],
    [sg.InputText(key='DOWNLOAD_BROWSE'), sg.FolderBrowse("Browse")],
    [sg.Button("Download",key='downloadbutton')],
]

custom_font = ('Open Sans', 14,"bold")

sg.LOOK_AND_FEEL_TABLE['MyCreatedTheme'] = {
    'BACKGROUND': '#014D22',
    'TEXT': '#FFFFFF',        
    'INPUT': '#FFFFFF',       
    'TEXT_INPUT': '#014D22',  
    'SCROLL': '#014D22',      
    'BUTTON': ('#014D22', '#FFFFFF'),  
    'PROGRESS': ('#014D22', '#FFFFFF'),  
    'BORDER': 1,
    'SLIDER_DEPTH': 0,
    'PROGRESS_DEPTH': 0,
}
  
sg.theme('MyCreatedTheme') 

window = sg.Window("KaartjesGenerator", layout,font=custom_font)

while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED:
        break

    if event == "uploadbutton1":
        ledenlijst_path = values["LEDENLIJST_BROWSE"]

    if event == "uploadbutton2":
        template_path = values["TEMPLATE_BROWSE"]
        
    if event == "downloadbutton":
        download_path = values["DOWNLOAD_BROWSE"]
        
        df = pd.read_excel(ledenlijst_path)
        ledenlijst = np.array(df)

        file = template_path

        naam_font = ImageFont.truetype('FRADMIT',350) # getal na lettertype = lettergrootte
        lidnummer_font = ImageFont.truetype('FRADMIT',200)


        tim = Image.new('RGBA', (3000,1000), (0,0,0,0))
        dr = ImageDraw.Draw(tim)
        ft = ImageFont.truetype('FRADM', 400)
        ft2 = ImageFont.truetype('FRADM', 125)


        titel = 'LIDKAART'
        jaar = '2022-2023' 

        dr.text((0, 0), titel, font=ft, fill='white')
        dr.text((1820,225), jaar, font=ft2, fill='white')
        tim = tim.rotate(90,  expand=1)

        lidkaarten = [0] * (len(ledenlijst))
        for i in range(0,len(ledenlijst)):
            achtergrond = Image.open(file)
            achtergrond.paste(tim, (240,-280), tim)
            letters = ImageDraw.Draw(achtergrond)
            letters.text((1200,1500),str(ledenlijst[i]).replace('[','').replace(']','').replace("'",'')  
        ,fill='black',font=naam_font)
            letters.text((1200,2100),'Lidnummer ' + str(i+1),fill='black',font=lidnummer_font)
            lidkaarten[i]=achtergrond

        achtergrond = Image.open(file)
        achtergrond.save(os.path.join(download_path, "lidkaarten.pdf"),save_all=True,append_images=lidkaarten[1:])

        sg.popup(f"Lidkaarten opgeslagen als pdf in :\n{download_path}")

window.close()