import requests
import random
import drawBot as db
import json
import numpy as np
import urllib

# pageWidth, pageHeight = 496, 737

COLOR_BLACK = (56, 48, 0, 74)
COLOR_CREAM = (0, 3, 13, 8)

def cmyk(c, m, y, k):
  return (c/100, m/100, y/100, k/100)

def calculateFontSizeByWidth(text, font, textBoxWidth):
  db.font(font)
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

def calculateFontSizeByHeightGivenWidth(text, font, textBoxHeight, textBoxWidth):
  current_font_size = 1
  while True:
      db.fontSize(current_font_size)
      current_font_size += 1
      _, current_text_height = db.textSize(text, 'left', width=textBoxWidth)
      if(current_font_size > 150):
          break
      elif(current_text_height > textBoxHeight):
          current_font_size -= 2
          break
  return current_font_size

def colorWithBuffer(buffer, c, m, y, k):
  return cmyk(c + buffer*random.random(), m + buffer*random.random(), y + buffer*random.random(), k + buffer*random.random())

def constrainImageToHeight(sourceImage, targetHeight, x, y):
  _, srcHeight = sourceImage.size()
  factorWidth = factorHeight = targetHeight / srcHeight
  with db.savedState():
      db.translate(x, y)
      db.scale(factorWidth, factorHeight)
      db.image(sourceImage, (0, 0))

def drawSquareAtCenter(x, y, squareSize):
  squareSize = squareSize / 2
  # db.strokeWidth(0.5)
  # db.stroke(0)
  db.rect(x, y, squareSize, squareSize)
  db.rect(x - squareSize, y, squareSize, squareSize)
  db.rect(x, y - squareSize, squareSize, squareSize)
  db.rect(x - squareSize, y - squareSize, squareSize, squareSize)

def backgroundSquares(width, height):
  tileSize = 5

  seedColor = COLOR_BLACK
  colorBuffer = 20
  for x in range(0, width, tileSize):
    for y in range(0, height, tileSize):
      db.cmykFill( *colorWithBuffer(colorBuffer,*seedColor) )
      db.rect(x, y, tileSize, tileSize)

def borderFlowers(squareSize, tileSize):
  # tileSize = 5

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
  pageHeight = 737
  pageWidth = 496
  db.newPage(496, 737)
  
  # db.cmykFill(*cmyk(71, 50, 0, 41))
  # db.rect(0, 0, 496, 737)
  actualSquareWidth = 6/pageWidth
  backgroundSquares(496, 737)

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
        borderFlowers(squareSize,5)

    db.translate(squareSize * squaresWide - squareSize, 0)
    for h in range(0, squaresHigh):
      with db.savedState():
        db.translate(0, h * squareSize)
        borderFlowers(squareSize,5)
  with db.savedState():
    db.translate(marginLeft + squareSize, marginBottom)
    for w in range(0, squaresWide - 2):
      with db.savedState():
        db.translate(w * squareSize, 0)
        borderFlowers(squareSize,5)
  with db.savedState():
    db.translate(marginLeft + squareSize, pageHeight - marginBottom - squareSize)
    for w in range(0, squaresWide - 2):
      with db.savedState():
        db.translate(w * squareSize, 0)
        borderFlowers(squareSize,5)

  db.saveImage('output/title-page.png')

def spread(drinkName, drinkData, drinkJSON):
  pageHeight = 737
  pageWidth = 992
  db.newPage(992, 737)

  backgroundSquares(992, 737)

  squareSize = 51
  squaresHigh = 12
  squaresWide = 16
  marginBottom = (pageHeight - (squareSize * squaresHigh)) / 2
  marginLeft = (pageWidth - (squareSize * squaresWide)) / 2
  with db.savedState():
    db.translate(marginLeft, marginBottom)
    for h in range(0, squaresHigh):
      with db.savedState():
        db.translate(0, h * squareSize)
        borderFlowers(squareSize,3)

    db.translate(squareSize * squaresWide - squareSize, 0)
    for h in range(0, squaresHigh):
      with db.savedState():
        db.translate(0, h * squareSize)
        borderFlowers(squareSize,3)
  with db.savedState():
    db.translate(marginLeft + squareSize, marginBottom)
    for w in range(0, squaresWide - 2):
      with db.savedState():
        db.translate(w * squareSize, 0)
        borderFlowers(squareSize,3)
  with db.savedState():
    db.translate(marginLeft + squareSize, pageHeight - marginBottom - squareSize)
    for w in range(0, squaresWide - 2):
      with db.savedState():
        db.translate(w * squareSize, 0)
        borderFlowers(squareSize,3)
  
  db.cmykFill(*cmyk(*COLOR_CREAM))
  db.rect(marginLeft + squareSize, marginBottom + squareSize, (squaresWide - 2) * squareSize, (squaresHigh - 2) * squareSize)

  drinkDetails = drinkJSON['drinks'][0]
  drinkThumbnailURL = drinkDetails['strDrinkThumb']
  drinkIngredients = []
  drinkIngredientsMeasures = []
  for x in range (1,16):
    ingredientKey = 'strIngredient' + str(x)
    measureKey = 'strMeasure' + str(x)
    if(drinkDetails[ingredientKey] != None):
      drinkIngredients.append(drinkDetails[ingredientKey])
      drinkIngredientsMeasures.append(drinkDetails[measureKey])

  i = 0
  for ingredient in drinkIngredients:
    if ingredient == "":
      break
    ingredientUrl = 'http://www.thecocktaildb.com/images/ingredients/' + urllib.parse.quote(drinkIngredients[i]) + '.png'
    ingredientImgObj = db.ImageObject(ingredientUrl)
    with ingredientImgObj:
      ingredientImgObj.dotScreen()
      ingredientImgObj.falseColor((28/255,34/255,66/255,1), (0,0,0,0))
    with db.savedState():
      db.blendMode('multiply')
      constrainImageToHeight(ingredientImgObj, 100, marginLeft + squareSize + (50 * i), marginBottom + squareSize + 20)
    i += 1
  
  generatedText = requests.post(
      "https://api.deepai.org/api/text-generator",
      data={
          'text': drinkData['description'],
      },
      headers={'api-key': 'cba42b1d-0cf8-40f1-b37f-6615ac018163'}
  )
  generatedText = generatedText.json()['output'] + '.'

  textBoxWidth = pageWidth/2 - (marginLeft + 2 * squareSize) 
  textBoxHeight = pageHeight - (marginBottom * 2 + 2 * squareSize + 180)

  current_font_size = calculateFontSizeByHeightGivenWidth(generatedText, 'CenturyGothic', textBoxHeight, textBoxWidth)
  generatedTextSize = current_font_size
  db.font('CenturyGothic', current_font_size)
  db.fill(28/255,34/255,66/255,1)
  db.textBox(
      generatedText,
      (
          marginLeft + squareSize + 20,
          marginBottom + squareSize + 140,
          textBoxWidth,
          textBoxHeight
      ),
      'left'
  )

  current_font_size = 1
  textBoxWidth = pageWidth/2 - (marginLeft + 2 * squareSize) 
  textBoxHeight = 25
  current_font_size = calculateFontSizeByHeightGivenWidth(drink, 'BalboaPlus-Fill', 30, textBoxWidth)
  drinkNameFontSize = current_font_size
  db.font('BalboaPlus-Fill', current_font_size)
  db.fill(28/255,34/255,66/255,1)
  db.textBox(
      drink,
      (
          marginLeft + squareSize + 20,
          pageHeight - (marginBottom + squareSize + 55),
          textBoxWidth,
          40
      ),
      'center'
  )
  
  db.font('BalboaPlus-Fill', drinkNameFontSize - 4)
  db.textBox(
      'Ingredients',
      (
          pageWidth/2 + squareSize + 20,
          pageHeight - (marginBottom + squareSize + 55),
          textBoxWidth,
          40
      ),
      'left'
  )

  ingredientsText = ''
  for i in range(0, len(drinkIngredients)):
    ingredientName = drinkIngredients[i]
    ingredientMeasure = drinkIngredientsMeasures[i]
    if(ingredient == None or ingredient.strip() == ''):
      break
    ingredientsText += ingredientMeasure + '  ' + ingredientName
    if(i != len(drinkIngredients) - 1):
      ingredientsText += '\n'

  db.font('BalboaPlus-Fill', drinkNameFontSize - 8)
  db.lineHeight(drinkNameFontSize)
  _, ingredientsHeight = db.textSize(ingredientsText, 'left', width=textBoxWidth)
  db.textBox(
      ingredientsText,
      (
          pageWidth/2 + squareSize + 20 + 20,
          pageHeight - (marginBottom + squareSize + 55 + ingredientsHeight - 15),
          textBoxWidth,
          ingredientsHeight
      ),
      'left'
  )

  db.font('BalboaPlus-Fill', drinkNameFontSize - 4)
  _, prepHeight = db.textSize('Preparation', 'left', width=textBoxWidth)
  db.textBox(
      'Preparation',
      (
          pageWidth/2 + squareSize + 20,
          pageHeight - (marginBottom + squareSize + 55 + ingredientsHeight + prepHeight + 20),
          textBoxWidth,
          40
      ),
      'left'
  )

  textBoxWidth = textBoxWidth - 60 #-60 for indent
  db.font('CenturyGothic', (drinkNameFontSize - 8))
  db.lineHeight(drinkNameFontSize - 7)
  _, prepDetailsHeight = db.textSize(drinkDetails['strInstructions'].strip(), 'left', width=textBoxWidth)

  db.textBox(
      drinkDetails['strInstructions'].strip(),
      (
          pageWidth/2 + squareSize + 20 + 20,
          pageHeight - (marginBottom + squareSize + 55 + ingredientsHeight + prepHeight + 20 + prepDetailsHeight),
          textBoxWidth,
          prepDetailsHeight
      ),
      'left'
  )

  drinkThumbnailURL = drinkDetails['strDrinkThumb']
  drinkImgObj = db.ImageObject(drinkThumbnailURL)
  with drinkImgObj:
    drinkImgObj.dotScreen()
    drinkImgObj.falseColor((28/255,34/255,66/255,1), (0,0,0,0))
  with db.savedState():
    db.blendMode('multiply')
    constrainImageToHeight(drinkImgObj, 100, pageWidth / 2 + ((squaresWide - 2) * squareSize) / 4 - 50, marginBottom + squareSize + 20)
  i += 1

  db.saveImage('output/spread.pdf')

if __name__ == '__main__':
  db.newDrawing()

  with open('data/drinks.json') as f:
    data = json.load(f)

  validDrink = False
  drink, drinkData = random.choice(list(data.items()))
  
  searchString = 'http://www.thecocktaildb.com/api/json/v1/1/search.php?s=' + urllib.parse.quote(drink)
  r = requests.get(searchString)
  drinkJSON = r.json()
  if(drinkJSON['drinks'] is None):
    while(drinkJSON['drinks'] is None):
      drink, drinkData = random.choice(list(data.items()))
      
      searchString = 'http://www.thecocktaildb.com/api/json/v1/1/search.php?s=' + urllib.parse.quote(drink)
      r = requests.get(searchString)
      drinkJSON = r.json()

  # titlePage(drink, drinkData)
  spread(drink, drinkData, drinkJSON)

  db.endDrawing()