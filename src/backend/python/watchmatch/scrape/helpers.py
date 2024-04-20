import pandas as pd
import requests
from bs4 import BeautifulSoup
import random
from time import sleep

HEADERS = [{"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"}, 
    {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36"},
    {"user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"},
    {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36"},
    {"user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"},
    {"user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1 Mobile/15E148 Safari/604.1"}]

database = requests.get("https://watchbase.com/watches", headers=HEADERS[0])
soup = BeautifulSoup(database.content, "html.parser")

def check_duplicates(csv_file):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file)

    # Check for duplicate rows
    duplicate_rows = df[df.duplicated()]

    if not duplicate_rows.empty:
        print("Duplicate rows found:")
        print(duplicate_rows)
    else:
        print("No duplicate rows found.")

def check_new_watches(txt_file):
    models = [] # List to store models (nodes of the tree)
    modelURLs = [] # List to store the URLs of each model
    newReferenceURLs = [] # List to store the URLs of each watch reference (leafs of the brand trees)
    # Extract model names and model URLs
    mainDiv = soup.find('div', id = "brand-container")
    unorderedLists = mainDiv.find_all('ul')
    for ul in unorderedLists:
        aTags = ul.find_all('a')
        for a in aTags:
            txt = a.get_text()
            if txt != "Brand":
                models.append(txt)
                modelURLs.append(a['href'])
    print("found modelURLs")

    # Extract reference URLs
    i = 0 # counter
    for url in modelURLs:
        i += 1
        print(str(i) + " i: " + url)
        randomNum = random.randint(0,5)
        modelPage = requests.get(url, headers=HEADERS[randomNum])
        soupModel = BeautifulSoup(modelPage.content, "html.parser")
        divReferences = soupModel.find('div', class_ = 'watch-block-container')
        aTagsReferences = divReferences.find_all('a')
        for a in aTagsReferences:
            newReferenceURLs.append(a['href'])
        sleep(1)

    # Compare with already existing referenceURLs
    file1 = open(txt_file,"r")
    oldReferenceURLs = eval(file1.read())
    file1.close
    missingURLs = []
    if len(oldReferenceURLs) > len(newReferenceURLs):
        print("Old referenceURLs is larger.")
        for i in range(len(newReferenceURLs)):
            if newReferenceURLs[i] not in oldReferenceURLs:
                missingURLs.append(newReferenceURLs[i])
            elif oldReferenceURLs[i] not in newReferenceURLs:
                missingURLs.append(oldReferenceURLs[i])
    elif len(oldReferenceURLs) < len(newReferenceURLs):
        print("Old referenceURLs is smaller.")
        for i in range(len(oldReferenceURLs)):
            if newReferenceURLs[i] not in oldReferenceURLs:
                missingURLs.append(newReferenceURLs[i])
            elif oldReferenceURLs[i] not in newReferenceURLs:
                missingURLs.append(oldReferenceURLs[i])
    else:
        print("Both files are same length.")
        for i in range(len(oldReferenceURLs)):
            if newReferenceURLs[i] not in oldReferenceURLs:
                missingURLs.append(newReferenceURLs[i])
            elif oldReferenceURLs[i] not in newReferenceURLs:
                missingURLs.append(oldReferenceURLs[i])
    file2 = open("./src/backend/ressources/missingURLs.txt","w")
    file2.write(str(missingURLs))
    file2.close

if __name__ == "__main__":
    check_new_watches('./src/backend/ressources/referenceURLs.txt')