import json
from tkinter import *
from copy import deepcopy

valDir = "values.json"
imgWidth = 1300
imgHeight = 800
boxWidth = 130
boxHeight = 17
xPadding = 35
yPadding = 9
yOffset = 50

totalYOffset = 50
totalXOffset = 50

def iterableKeys(diction):
    resList = []
    for key, value in diction.items():
        resList.append(key)
    return resList

def makeTree():
    window = Tk()
    window.title('Phylogenetic tree')
    window.geometry(f"{imgWidth}x{imgHeight}+10+20")
    canvas = Canvas(window, width=imgWidth, height=imgHeight)
    canvas.pack()

    cache = []
    linePos = []
    counter = 0
    with open(valDir, "r") as f:
        data = json.load(f)
        for kingdom in iterableKeys(data):
            # phylumStartY = deepcopy(counter)
            phylumCache = []
            phylumLine = []
            for phylum in iterableKeys(data[kingdom]):
                # classStartY = deepcopy(counter)
                classCache = []
                classLine = []
                for plantClass in iterableKeys(data[kingdom][phylum]):
                    # orderStartY = deepcopy(counter)
                    orderCache = []
                    orderLine = []
                    for order in iterableKeys(data[kingdom][phylum][plantClass]):
                        # familyStartY = deepcopy(counter)
                        familyCache = []
                        familyLine = []
                        for family in iterableKeys(data[kingdom][phylum][plantClass][order]):
                            genusStartY = deepcopy(counter)
                            genusLine = []
                            for genus in data[kingdom][phylum][plantClass][order][family]:
                                genusName = genus[:genus.find("NAME:")]
                                plantName = genus[genus.find("NAME:") + 5:]
                                genusLine.append(drawRect(canvas, 1, counter, genusName)[0])
                                drawRect(canvas, 0, counter, plantName, "#ff5e6c")
                                counter+=1
                            genusEndY = deepcopy(counter) - 1
                            familyCache.append((genusEndY - genusStartY)/2 + genusStartY)
                            origin = drawRect(canvas, 2, (genusEndY - genusStartY)/2 + genusStartY, family)
                            drawLine(canvas, origin[1], genusLine)
                            familyLine.append(origin[0])
                        # familyEndY = deepcopy(counter) - 1
                        origin = drawRect(canvas, 3, sum(familyCache)/len(familyCache), order)
                        drawLine(canvas, origin[1], familyLine)
                        orderLine.append(origin[0])
                        orderCache.append(sum(familyCache)/len(familyCache))
                    # orderEndY = deepcopy(counter) - 1
                    origin = drawRect(canvas, 4, sum(orderCache)/len(orderCache), plantClass)
                    drawLine(canvas, origin[1], orderLine)
                    classLine.append(origin[0])
                    classCache.append(sum(orderCache)/len(orderCache))
                # classEndY = deepcopy(counter) - 1
                origin = drawRect(canvas, 5, sum(classCache)/len(classCache), phylum)
                drawLine(canvas, origin[1], classLine)
                phylumLine.append(origin[0])
                phylumCache.append(sum(classCache)/len(classCache))
            # phylumEndY = deepcopy(counter) - 1
            origin = drawRect(canvas, 6, sum(phylumCache)/len(phylumCache), kingdom)
            drawLine(canvas, origin[1], phylumLine)
            # orderLine.append(origin[1])
            # cache.append(sum(cache)/len(cache))

    writeTitles(canvas, 0, 0, "Name:")
    writeTitles(canvas, 1, 0, "Genus:")
    writeTitles(canvas, 2, 0, "Family:")
    writeTitles(canvas, 3, 0, "Order:")
    writeTitles(canvas, 4, 0, "Class:")
    writeTitles(canvas, 5, 0, "Phylum:")
    writeTitles(canvas, 6, 0, "Kingdom:")
    window.mainloop()

def getY(counter):
    return (boxHeight + padding) * counter + padding

def drawLine(canvas, origin, points):
    for i in points:
        canvas.create_line(origin[0], origin[1], i[0], i[1], fill="#18091a", width="3")

def writeTitles(canvas, rightOffset, counter, label):
    x1 = imgWidth - ((boxWidth + xPadding) * rightOffset) - boxWidth - totalXOffset
    y1 = (boxHeight + yPadding) * counter + totalYOffset
    x2 = imgWidth - ((boxWidth + xPadding) * rightOffset) - totalXOffset
    y2 = (boxHeight + yPadding) * counter + boxHeight + totalYOffset

    canvas.create_rectangle(x1, y1, x2, y2, fill="#1c2a4d")
    canvas.create_text((x2 - x1)/2 + x1, (y2 - y1)/2 + y1, text=label, fill="#9db1e3", font=('Helvetica','8'))

def drawRect(canvas, rightOffset, counter, label, color = "#32a83c"):
    x1 = imgWidth - ((boxWidth + xPadding) * rightOffset) - boxWidth - totalXOffset
    y1 = (boxHeight + yPadding) * counter + yOffset + totalYOffset
    x2 = imgWidth - ((boxWidth + xPadding) * rightOffset) - totalXOffset
    y2 = (boxHeight + yPadding) * counter + boxHeight + yOffset + totalYOffset

    canvas.create_rectangle(x1, y1, x2, y2, fill=color)
    canvas.create_text((x2 - x1)/2 + x1, (y2 - y1)/2 + y1, text=label, fill="#023309", font=('Helvetica','7'))

    return ((x1, (y2 - y1)/2 + y1), (x2, (y2 - y1)/2 + y1))

def main():
    makeTree()

if __name__ == "__main__":
    main()