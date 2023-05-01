import tensorflow as tf
import os
from PIL import Image
import json
import requests
import pptx
from pptx.util import Inches
import numpy as np
import csv

from json import JSONEncoder
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

import tree_maker as tm
from bs4 import BeautifulSoup as BS
import re

valDir = "values.json"
plantsList = "plants.csv"
searchUrl = "https://www.biolib.cz/cz/main/"

resultDict = {}
resultTree = []

class plantEncoder(JSONEncoder):
        def default(self, o):
            return {o.__class__.__name__: o.__dict__}

class plant:
    def __init__(self, kingdom, phylum, plantClass, order, family, genus):
        self.kingdom = kingdom
        self.phylum = phylum
        self.plantClass = plantClass
        self.order = order
        self.family = family
        self.genus = genus

def produce_output(model):
    imgs = os.listdir(id_dir)
    prs = pptx.Presentation()
    lyt=prs.slide_layouts[0] # choosing a slide layout

    with open(map_file, "r") as f:
        eraseFile()
        data = json.load(f)
        for image in imgs:
            if image not in [".DS_Store", ".gitkeep"]:
                continue

            imgPath = os.path.join(id_dir, image)

            if imgPath[:-4] != ".ppm":
                im = Image.open(imgPath)
                ppmPath = f"{imgPath}.ppm"
                im.convert("RGB").save(ppmPath, "PPM")
                os.rename(imgPath, os.path.join("wrong_formats", image))
                imgPath = ppmPath

            img = cv2.imread(imgPath, cv2.IMREAD_COLOR)
            img = cv2.resize(img, (IMG_WIDTH, IMG_HEIGHT))
            output = model.predict(np.array([img]))

            newPath = os.path.join(id_dir, f"{str(imgs.index(image))}.jpg")
            im = Image.open(imgPath)
            im.convert("RGB").save(newPath, "JPEG")

            slide=prs.slides.add_slide(lyt) #New slide
            # title=slide.shapes.title
            imag=slide.shapes.add_picture(newPath, Inches(0), Inches(0)) #Image
            subtitle=slide.placeholders[1]
            # title.text=image

            text = requests.get(searchUrl).text

            plantName = data[str(np.argmax(output))]
            # subtitle.text = plantName #Image classification

            hierarchy = getHierarchy(plantName)
            subtitle.text = f"Class: {hierarchy.plantClass}, Order: {hierarchy.order}, Family: {hierarchy.family}, Genus: {hierarchy.genus}"

            os.remove(newPath)

        json_object = json.dumps(resultDict, indent=4)
        with open(valDir, "a") as f:
            f.write(json_object)
        prs.save("plants.pptx")

def main():
    eraseFile()
    # getHierarchy("Galega_officinalis")
    # getHierarchy("Zornia gibbosa")
    # getHierarchy("Oncostema_elongata")
    # getHierarchy("Lomatia_ferruginea")

    with open(plantsList, "r") as f:
        csvreader = csv.reader(f)
        for i in csvreader:
            for j in i:
                getHierarchy(j)

    json_object = json.dumps(resultDict, indent=4)
    with open(valDir, "a") as f:
        f.write(json_object)

    tm.main()

def eraseFile():
    open(valDir, "w").close()

def getHierarchy(plantName):
    searchterm = plantName

    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(searchUrl)

    consent = driver.find_element(By.ID, 'consentAllButton')
    consent.click()

    sbox = driver.find_element(By.XPATH, "//input[@type='text' and @autofocus='autofocus' and @name='string']")
    sbox.send_keys(searchterm)

    submit = driver.find_element(By.XPATH, "//input[@type='submit' and @class='clbutton' and @value=' OK ']")
    submit.click()

    page_source = driver.page_source
    soup = BS(page_source, features="lxml")

    #Scrape all values
    kingdom = getTypeElement(soup, "říše")
    phylum = getTypeElement(soup, "oddělení")
    plantClass = getTypeElement(soup, "třída")
    order = getTypeElement(soup, "řád")
    family = getTypeElement(soup, "čeleď")
    genus = getTypeElement(soup, "rod")

    result = plant(kingdom, phylum, plantClass, order, family, genus)

    #Create organized output
    familyDict = {family: [genus]}
    orderDict = {order: familyDict}
    classDict = {plantClass: orderDict}
    phylumDict = {phylum: classDict}
    kingdomDict = {kingdom: phylumDict}
    
    if kingdom in iterableKeys(resultDict):
        if phylum in iterableKeys(resultDict[kingdom]):
            if plantClass in iterableKeys(resultDict[kingdom][phylum]):
                if order in iterableKeys(resultDict[kingdom][phylum][plantClass]):
                    if family in iterableKeys(resultDict[kingdom][phylum][plantClass][order]):
                        if genus in resultDict[kingdom][phylum][plantClass][order][family]:
                            return result
                        else:
                            if type(resultDict[kingdom][phylum][plantClass][order][family]) == list:
                                resultDict[kingdom][phylum][plantClass][order][family].append(genus)
                            else:
                                resultDict[kingdom][phylum][plantClass][order][family] = [genus]
                    else:
                        resultDict[kingdom][phylum][plantClass][order][family] = [genus]
                else:
                    resultDict[kingdom][phylum][plantClass][order] = familyDict
            else:
                resultDict[kingdom][phylum][plantClass] = orderDict
        else:
            resultDict[kingdom][phylum] = classDict
    else:
        resultDict[kingdom] = phylumDict

    return result

def iterableKeys(diction):
    resList = []
    for key, value in diction.items():
        resList.append(key)
    return resList

def merge_dicts(dict_list):
    result = {}
    for sub_dict in dict_list:
        for key, value in sub_dict.items():
            if isinstance(value, dict):
                result[key] = merge_dicts([result.get(key, {}), value])
            elif key not in result:
                result[key] = value
            elif value != result[key]:
                result[key] = [result[key], value]
    return result

def getTypeElement(soup, input):
    identifier = soup.find(string=re.compile(input))
    latin = identifier.find_next("a")
    czech = latin.find_next("b")
    latinText = str(latin.contents[0])
    if latinText[:4] == "<em>":
        latinText = latinText[4:-5]
    return f"{czech.contents[0]} \n({latinText})"

if __name__ == "__main__":
    main()