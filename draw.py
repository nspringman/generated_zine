import requests
import random
import drawBot as db
import json
import numpy as np

pageWidth, pageHeight = 496, 737

COLOR_BLACK = (56, 48, 0, 74)
COLOR_CREAM = (0, 3, 13, 8)

def cmyk(c, m, y, k):
  return (c/100, m/100, y/100, k/100)

def calculateFontSizeByWidth(text, font, textBoxWidth):
  currentFontSize = 10
  if text == "&":
    return 75
  while True:
    db.fontSize(currentFontSize)
    currentFontSize += 1
    currentTextWidth, _ = db.textSize(text, 'left', width=textBoxWidth)
    if(currentFontSize > 120):
        break
    elif(currentTextWidth > textBoxWidth * 0.95):
        currentFontSize -= 2
        break
  return currentFontSize

def colorWithBuffer(buffer, c, m, y, k):
  return cmyk(c + buffer*random.random(), m + buffer*random.random(), y + buffer*random.random(), k + buffer*random.random())

def drawSquareAtCenter(x, y, squareSize):
  squareSize = squareSize / 2
  # db.strokeWidth(0.5)
  # db.stroke(0)
  db.rect(x, y, squareSize, squareSize)
  db.rect(x - squareSize, y, squareSize, squareSize)
  db.rect(x, y - squareSize, squareSize, squareSize)
  db.rect(x - squareSize, y - squareSize, squareSize, squareSize)

def backgroundSquares():
  tileSize = 5

  seedColor = COLOR_BLACK
  colorBuffer = 20
  for x in range(0, pageWidth, tileSize):
    for y in range(0, pageHeight, tileSize):
      db.cmykFill( *colorWithBuffer(colorBuffer,*seedColor) )
      db.rect(x, y, tileSize, tileSize)

def borderFlowers(squareSize):
  tileSize = 5

  #background white
  seedColor = (0, 2, 6, 3)
  colorBuffer = 20
  for x in range(0, squareSize, tileSize):
    for y in range(0, squareSize, tileSize):
      db.cmykFill( *colorWithBuffer(colorBuffer,*seedColor) )
      db.rect(x, y, tileSize, tileSize)

  #border gold
  seedColor = (0, 22, 83, 24)
  colorBuffer = 20
  for x in range(0, squareSize, tileSize):
    db.cmykFill( *colorWithBuffer(colorBuffer,*seedColor) )

    db.rect(x, 0, tileSize, tileSize)
    db.rect(x, squareSize - tileSize, tileSize, tileSize)

    db.rect(0, x, tileSize, tileSize)
    db.rect(squareSize - tileSize, x, tileSize, tileSize)
  
  #inset border black
  seedColor = COLOR_BLACK
  colorBuffer = 20
  for x in range(tileSize, squareSize - tileSize, tileSize):
    db.cmykFill( *colorWithBuffer(colorBuffer,*seedColor) )

    db.rect(x, tileSize, tileSize, tileSize)
    db.rect(x, squareSize - tileSize * 2, tileSize, tileSize)

    db.rect(tileSize, x, tileSize, tileSize)
    db.rect(squareSize - tileSize * 2, x, tileSize, tileSize)

  #circles
  seedColor = COLOR_BLACK
  colorBuffer = 20
  centerPoint = squareSize/2, squareSize/2
  radius = squareSize / 4
  for x in np.arange(0, 360, 360/28):
    with db.savedState():
      db.rotate(x, centerPoint)
      db.cmykFill( *colorWithBuffer(colorBuffer,*seedColor) )
      drawSquareAtCenter(centerPoint[0], centerPoint[1] + radius, tileSize)
  seedColor = (72, 37, 0, 21)
  colorBuffer = 20
  radius = radius - tileSize
  for x in np.arange(0, 360, 360/22):
    with db.savedState():
      db.rotate(x, centerPoint)
      db.cmykFill( *colorWithBuffer(colorBuffer,*seedColor) )
      drawSquareAtCenter(centerPoint[0], centerPoint[1] + radius, tileSize)
  seedColor = (52, 27, 0, 21)
  colorBuffer = 20
  radius = radius - tileSize
  for x in np.arange(0, 360, 360/16):
    with db.savedState():
      db.rotate(x, centerPoint)
      db.cmykFill( *colorWithBuffer(colorBuffer,*seedColor) )
      drawSquareAtCenter(centerPoint[0], centerPoint[1] + radius, tileSize)
  seedColor = (36, 18, 0, 21)
  colorBuffer = 20
  radius = radius - tileSize
  for x in np.arange(0, 360, 360/8):
    with db.savedState():
      db.rotate(x, centerPoint)
      db.cmykFill( *colorWithBuffer(colorBuffer,*seedColor) )
      drawSquareAtCenter(centerPoint[0], centerPoint[1] + radius, tileSize)

  seedColor = COLOR_BLACK
  colorBuffer = 20
  radius = squareSize / 8
  for x in np.arange(0, 360, 360/4):
    with db.savedState():
      db.rotate(x, centerPoint)
      db.translate(0, 2 * radius)
      for x in np.arange(0, 360, 360/12):
        with db.savedState():
          db.rotate(x, centerPoint)
          db.cmykFill( *colorWithBuffer(colorBuffer,*seedColor) )
          drawSquareAtCenter(centerPoint[0], centerPoint[1] + radius, tileSize)
      for x in np.arange(0, 360, 360/6):
        db.cmykFill( *colorWithBuffer(colorBuffer,*COLOR_CREAM) )
        drawSquareAtCenter(*centerPoint, tileSize)
        with db.savedState():
          db.rotate(x, centerPoint)
          db.cmykFill( *colorWithBuffer(colorBuffer,*COLOR_CREAM) )
          drawSquareAtCenter(centerPoint[0], centerPoint[1] + radius * 0.5, tileSize)

def titlePage(drinkName, drinkData):
  db.newPage(496, 737)
  
  # db.cmykFill(*cmyk(71, 50, 0, 41))
  # db.rect(0, 0, 496, 737)
  actualSquareWidth = 6/pageWidth
  backgroundSquares()

  margin = 130
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
    drinkText.append(drink, font='BalboaPlus-Primary', fontSize=fontSize, align='center', cmykFill=cmyk(*COLOR_CREAM))
    if firstLineHeight == 0:
      _, firstLineHeight = db.textSize(drinkText)

  drinkTextWidth, drinkTextHeight = db.textSize(drinkText)
  db.textBox(drinkText, ((pageWidth - drinkTextWidth) / 2, (pageHeight - drinkTextHeight) / 2, drinkTextWidth, drinkTextHeight) )
  squareSize = 80
  squaresHigh = 8
  squaresWide = 5
  marginBottom = (pageHeight - (squareSize * squaresHigh)) / 2
  marginLeft = (pageWidth - (squareSize * squaresWide)) / 2
  with db.savedState():
    db.translate(marginLeft, marginBottom)
    for h in range(0, squaresHigh):
      with db.savedState():
        db.translate(0, h * squareSize)
        borderFlowers(squareSize)

    db.translate(squareSize * squaresWide - squareSize, 0)
    for h in range(0, squaresHigh):
      with db.savedState():
        db.translate(0, h * squareSize)
        borderFlowers(squareSize)
  with db.savedState():
    db.translate(marginLeft + squareSize, marginBottom)
    for w in range(0, squaresWide - 2):
      with db.savedState():
        db.translate(w * squareSize, 0)
        borderFlowers(squareSize)
  with db.savedState():
    db.translate(marginLeft + squareSize, pageHeight - marginBottom - squareSize)
    for w in range(0, squaresWide - 2):
      with db.savedState():
        db.translate(w * squareSize, 0)
        borderFlowers(squareSize)

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