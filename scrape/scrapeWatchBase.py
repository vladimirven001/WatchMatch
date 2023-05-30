from bs4 import BeautifulSoup
import requests
import pandas as pd

HEADERS = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"}
database = requests.get("https://watchbase.com/watches", headers=HEADERS)
soup = BeautifulSoup(database.content, "html.parser")

brands = [] # List to store brand of the watch (roots of the trees)
models = [] # List to store models (nodes of the tree)
modelURLs = [] # List to store the URLs of each model
referenceURLs = [] # List to store the URLs of each watch reference (leafs of the brand trees)

mainDiv = soup.find("div", id = "brand-container")
mainHeaders = mainDiv.find_all("h2")
for brand in mainHeaders:
    brands.append(brand.text.strip())

unorderedLists = mainDiv.find_all("ul")
for ul in unorderedLists:
    aTags = ul.find_all('a')
    for a in aTags:
        txt = a.get_text()
        if txt != "Brand":
            models.append(txt)
            modelURLs.append(a['href'])

for url in modelURLs:
    modelPage = requests.get(url, headers=HEADERS)
    soupModel = BeautifulSoup(modelPage.content, "html.parser")
    div = soup.find("div", class_ = "watch-block-container")


