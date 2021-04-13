import requests
import random
import drawBot as db
import json

pageWidth, pageHeight = 496, 737

def cmyk(c, m, y, k):
  return (c/100, m/100, y/100, k/100)

def calculateFontSizeByWidth(text, font, textBoxWidth):
  currentFontSize = 10
  if text == "&":
    return 100
  while True:
    db.fontSize(currentFontSize)
    currentFontSize += 1
    currentTextWidth, _ = db.textSize(text, 'left', width=textBoxWidth)
    if(currentFontSize > 200):
        break
    elif(currentTextWidth > textBoxWidth * 0.95):
        currentFontSize -= 2
        break
  return currentFontSize

def titlePage(drinkName, drinkData):
  db.newPage(496, 737)
  
  db.cmykFill(*cmyk(71, 50, 0, 41))
  db.rect(0, 0, 496, 737)

  margin = 80
  textBoxHeight = 400
  textBoxWidth = pageWidth - 2 * margin

  splitDrink = drinkName.split()
  firstLineHeight = 0
  drinkText = db.FormattedString()

  for i in range(0,len(splitDrink)):
    drink = splitDrink[i]
    if i != len(splitDrink):
      drink += "\n"

    fontSize = calculateFontSizeByWidth(drink, 'BalboaPlus-Primary', textBoxWidth)
    drinkText.append(drink, font='BalboaPlus-Primary', fontSize=fontSize, align='center', cmykFill=cmyk(0,0,0,0))
    if firstLineHeight == 0:
      _, firstLineHeight = db.textSize(drinkText)

  drinkTextWidth, drinkTextHeight = db.textSize(drinkText)
  # print((pageWidth / 2, pageHeight - drinkTextHeight))
  db.textBox(drinkText, ((pageWidth - drinkTextWidth) / 2, (pageHeight - drinkTextHeight) / 2, drinkTextWidth, drinkTextHeight) )

  db.saveImage('output/title-page.png')

if __name__ == '__main__':
  db.newDrawing()

  with open('data/drinks.json') as f:
    data = json.load(f)

  drink, drinkData = random.choice(list(data.items()))

  titlePage(drink, drinkData)

  # r = requests.post(
  #     "https://api.deepai.org/api/text2img",
  #     data={
  #         'text': drink,
  #     },
  #     headers={'api-key': 'cba42b1d-0cf8-40f1-b37f-6615ac018163'}
  # )
  # imageData = r.json()
  # print(imageData)
  # db.image(imageData['output_url'], (0,0))
  db.endDrawing()