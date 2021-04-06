import requests
import json
from bs4 import BeautifulSoup

urls = []
containerPage = 'https://www.liquor.com/classic-cocktails-4779424'
page = requests.get(containerPage)
soup = BeautifulSoup(page.content, 'html.parser')
for y in range(2, 12, 2):
    cardWrapperID = 'card-list_' + str(y-1) + '-0'
    cardsWrapper = soup.find(id=cardWrapperID).find_all('a', class_='comp card')

    for card in cardsWrapper:
        urls.append(card['href'])

drinkDict = {}

for url in urls:
    page = requests.get(url)

    soup = BeautifulSoup(page.content, 'html.parser')

    drinkName = soup.find(id="heading_1-0").find('h1').text
    firstPar = soup.find(id='mntl-sc-block_1-0').text

    # r = requests.post(
    #     "https://api.deepai.org/api/text-generator",
    #     data={
    #         'text': firstPar,
    #     },
    #     headers={'api-key': 'quickstart-QUdJIGlzIGNvbWluZy4uLi4K'}
    # )

    drinkDef = {
        'url': url,
        'description': firstPar
    }

    drinkDict[drinkName] = drinkDef
    
    # print(r.json()['output'])

with open('data/drinks.json', 'w+') as outfile:
    json.dump(drinkDict, outfile)