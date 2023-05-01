import json
from value_getter import iterableKeys
from tkinter import *
from copy import deepcopy

valDir = "values.json"
imgWidth = 1300
imgHeight = 800
boxWidth = 200
boxHeight = 50
padding = 20

def main():
    window = Tk()
    window.title('Phylogenetic tree')
    window.geometry(f"{imgWidth}x{imgHeight}+10+20")
    canvas = Canvas(window, width=imgWidth, height=imgHeight)
    canvas.pack()

    cache = []
    counter = 0
    with open(valDir, "r") as f:
        data = json.load(f)
        for kingdom in iterableKeys(data):
            # phylumStartY = deepcopy(counter)
            kingdomCache = []
            for phylum in iterableKeys(data[kingdom]):
                # classStartY = deepcopy(counter)
                classCache = []
                for plantClass in iterableKeys(data[kingdom][phylum]):
                    # orderStartY = deepcopy(counter)
                    orderCache = []
                    for order in iterableKeys(data[kingdom][phylum][plantClass]):
                        # familyStartY = deepcopy(counter)
                        familyCache = []
                        for family in iterableKeys(data[kingdom][phylum][plantClass][order]):
                            genusStartY = deepcopy(counter)
                            for genus in data[kingdom][phylum][plantClass][order][family]:
                                drawRect(canvas, 0, counter, genus)
                                counter+=1
                            genusEndY = deepcopy(counter) - 1
                            familyCache.append((genusEndY - genusStartY)/2 + genusStartY)
                            drawRect(canvas, 1, (genusEndY - genusStartY)/2 + genusStartY, family)
                        # familyEndY = deepcopy(counter) - 1
                        drawRect(canvas, 2, sum(familyCache)/len(familyCache), order)
                        orderCache.append(sum(familyCache)/len(familyCache))
                    # orderEndY = deepcopy(counter) - 1
                    drawRect(canvas, 3, sum(orderCache)/len(orderCache), plantClass)
                    classCache.append(sum(orderCache)/len(orderCache))
                # classEndY = deepcopy(counter) - 1
                drawRect(canvas, 4, sum(classCache)/len(classCache), phylum)
                kingdomCache.append(sum(classCache)/len(classCache))
            # phylumEndY = deepcopy(counter) - 1
            drawRect(canvas, 5, sum(kingdomCache)/len(kingdomCache), kingdom)
            # cache.append(sum(cache)/len(cache))

    window.mainloop()

def getY(counter):
    return (boxHeight + padding) * counter + padding

def drawRect(canvas, rightOffset, counter, label):
    x1 = imgWidth - ((boxWidth + padding) * rightOffset) - boxWidth
    y1 = (boxHeight + padding) * counter
    x2 = imgWidth - ((boxWidth + padding) * rightOffset)
    y2 = (boxHeight + padding) * counter + boxHeight

    canvas.create_rectangle(x1, y1, x2, y2, fill="red")
    canvas.create_text((x2 - x1)/2 + x1, (y2 - y1)/2 + y1, text=label, fill="black")

if __name__ == "__main__":
    main()