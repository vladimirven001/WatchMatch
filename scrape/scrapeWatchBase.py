from bs4 import BeautifulSoup
import requests
import pandas as pd
from time import sleep

HEADERS = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"}
database = requests.get("https://watchbase.com/watches", headers=HEADERS)
soup = BeautifulSoup(database.content, "html.parser")

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
i = 0 # counter
for url in modelURLs:
    i += 1
    modelPage = requests.get(url, headers=HEADERS)
    soupModel = BeautifulSoup(modelPage.content, "html.parser")
    divReferences = soupModel.find('div', class_ = 'watch-block-container')
    aTagsReferences = divReferences.find_all('a')
    for a in aTagsReferences:
        referenceURLs.append(a['href'])
    sleep(1)

print(referenceURLs)

# Create data structure to store watch references and information
data = pd.DataFrame(columns = ["brand","family","reference","name","movement","produced","caseMaterial",
                               "caseGlass","caseBack","caseShape","caseDiameter","caseHeight","dialColor",
                               "dialMaterial","dialIndexes","dialHands","description"])

# Get the information for each watch reference
for url in referenceURLs:
    watch = {"brand":"","family":"","reference":"","name":"","movement":"","produced":"","caseMaterial":"",
                               "caseGlass":"","caseBack":"","caseShape":"","caseDiameter":"","caseHeight":"","dialColor":"",
                               "dialMaterial":"","dialIndexes":"","dialHands":"","description":""}
    
    referencePage = requests.get(url, headers=HEADERS)
    soupModel = BeautifulSoup(referencePage.content, "html.parser")
    table = soupModel.find('table', class_ = 'info-table')
    tableRows = table.find_all('tr')
    for tr in tableRows:
        collumn = tr.find('th').text.lower()
        data = tr.find('td').text.lower()
        watch[collumn]
    div = soupModel.find('div', class_ = 'col-xs-6')
    



# Export watch references as .csv file



