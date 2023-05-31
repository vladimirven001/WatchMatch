from bs4 import BeautifulSoup
import requests
import pandas as pd
from time import sleep

HEADERS = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"}
database = requests.get("https://watchbase.com/watches", headers=HEADERS)
soup = BeautifulSoup(database.content, "html.parser")

proxies = [
    {'http': 'http://181.129.74.58:40667', 'https': 'https://181.129.74.58:40667'},
    {'http': 'http://105.19.63.217:9812', 'https': 'https://105.19.63.217:9812'},
    {'http': 'http://187.217.54.84:80', 'https': 'https://187.217.54.84:80'}
]

brands = [] # List to store brand of the watch (roots of the trees)
models = [] # List to store models (nodes of the tree)
modelURLs = [] # List to store the URLs of each model
referenceURLs = [] # List to store the URLs of each watch reference (leafs of the brand trees)

# Extract brand names
mainDiv = soup.find('div', id = "brand-container")
mainHeaders = mainDiv.find_all('h2')
for brand in mainHeaders:
    brands.append(brand.text.strip())

# Extract model names and model URLs
unorderedLists = mainDiv.find_all('ul')
for ul in unorderedLists:
    aTags = ul.find_all('a')
    for a in aTags:
        txt = a.get_text()
        if txt != "Brand":
            models.append(txt)
            modelURLs.append(a['href'])

# Extract reference URLs
i=0
j=1
proxy = proxies[0]
for url in modelURLs:
    i += 1
    print(i)
    modelPage = requests.get(url, headers=HEADERS)
    soupModel = BeautifulSoup(modelPage.content, "html.parser")
    divReferences = soupModel.find('div', class_ = 'watch-block-container')
    aTagsReferences = divReferences.find_all('a')
    for a in aTagsReferences:
        referenceURLs.append(a['href'])
    sleep(1)

print(referenceURLs)

data = pd.DataFrame(columns = ["brand","model","reference","name","movement","produced","caseMaterial",
                               "caseGlass","caseBack","caseShape","caseDiameter","caseHeight","dialColor",
                               "dialMaterial","dialIndexes","dialHands","description"])


