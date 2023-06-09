from bs4 import BeautifulSoup
import requests
import pandas as pd
from time import sleep
import random

HEADERS = [{"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"}, 
    {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36"},
    {"user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"},
    {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36"},
    {"user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"},
    {"user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1 Mobile/15E148 Safari/604.1"}]

database = requests.get("https://watchbase.com/watches", headers=HEADERS[0])
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
print("found brand names")

# Extract model names and model URLs
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
# i = 0 # counter
# for url in modelURLs:
#     i += 1
#     print(str(i) + " i: " + url)
#     randomNum = random.randint(0,5)
#     modelPage = requests.get(url, headers=HEADERS[randomNum])
#     soupModel = BeautifulSoup(modelPage.content, "html.parser")
#     divReferences = soupModel.find('div', class_ = 'watch-block-container')
#     aTagsReferences = divReferences.find_all('a')
#     for a in aTagsReferences:
#         referenceURLs.append(a['href'])
#     sleep(1)

# file1 = open("referenceURLs.txt","w")
# file1.write(str(referenceURLs))
# file1.close
# print("found referenceURLs")

# Create data structure to store watch references and information
df = pd.DataFrame(columns = ["brand","family","reference","name","movement","produced","caseMaterial",
                               "caseGlass","caseBack","caseShape","caseDiameter","caseHeight","caseLugWidth","dialColor",
                               "dialMaterial","dialIndexes","dialHands"])

# Get the information for each watch reference
j=0
file1 = open("referenceURLs.txt","r")
referenceURLs = eval(file1.read())
file1.close
print("found referenceURLs")
print("len(referenceURLs) = ", "")
print(len(referenceURLs))
done = False
timeout = 10
start_index = 0

# while not done:
#     try:
#         for i in range(j, len(referenceURLs) - 1):
#             print("j: " + str(j))
#             watch = {"brand":"","family":"","reference":"","name":"","movement":"","produced":"","limited":"","caseMaterial":"",
#                                        "caseGlass":"","caseBack":"","caseShape":"","caseDiameter":"","caseHeight":"","caseLugWidth":"","dialColor":"",
#                                        "dialMaterial":"","dialIndexes":"","dialHands":""}
#             randomNum = random.randint(0,5)
#             referencePage = requests.get(referenceURLs[i], headers=HEADERS[randomNum])
#             soupModel = BeautifulSoup(referencePage.content, "html.parser")
#             table = soupModel.find('table', class_ = 'info-table')
#             tableRows = table.find_all('tr')
#             for tr in tableRows:
#                 collumn = tr.find('th').text.lower()
#                 collumn = "".join(c for c in collumn if c.isalpha())
#                 data = tr.find('td').text.lower()
#                 watch[collumn] = data
    
#             div = soupModel.find('div', class_ = 'col-xs-6')

#             # Case info
#             table = div.find('table', class_ = 'info-table')
#             tableRows = table.find_all('tr')
#             for tr in tableRows:
#                 collumn = tr.find('th').text.replace(" ","")
#                 collumn = "".join(c for c in collumn if c.isalpha())
#                 collumn = "case" + collumn
#                 data = tr.find('td').text.lower()
#                 watch[collumn] = data

#             # Dial info
#             table = table.find_next('table', class_ = 'info-table')
#             tableRows = table.find_all('tr')
#             for tr in tableRows:
#                 collumn = tr.find('th').text.replace(" ","")
#                 collumn = "".join(c for c in collumn if c.isalpha())
#                 collumn = "dial" + collumn
#                 data = tr.find('td').text.lower()
#                 watch[collumn] = data

#             # Add data to pandas df
#             df.loc[j] = watch
#             j += 1
#         done = True
#     except AttributeError:
#         print("Unexpected error: " + str(j))
#         print("sleeping...")
#         sleep(60)
#         done = False

while start_index < len(referenceURLs):
    done = False
    current_index = start_index
    
    try:
        for i in range(j, len(referenceURLs) - 1):
            print("j: " + str(j))
            watch = {"brand":"","family":"","reference":"","name":"","movement":"","produced":"","limited":"","caseMaterial":"",
                                       "caseGlass":"","caseBack":"","caseShape":"","caseDiameter":"","caseHeight":"","caseLugWidth":"","dialColor":"",
                                       "dialMaterial":"","dialIndexes":"","dialHands":""}
            randomNum = random.randint(0,5)
            referencePage = requests.get(referenceURLs[i], headers=HEADERS[randomNum], timeout=timeout)
            soupModel = BeautifulSoup(referencePage.content, "html.parser")
            table = soupModel.find('table', class_ = 'info-table')
            tableRows = table.find_all('tr')
            for tr in tableRows:
                collumn = tr.find('th').text.lower()
                collumn = "".join(c for c in collumn if c.isalpha())
                data = tr.find('td').text.lower()
                watch[collumn] = data
    
            div = soupModel.find('div', class_ = 'col-xs-6')

            # Case info
            table = div.find('table', class_ = 'info-table')
            tableRows = table.find_all('tr')
            for tr in tableRows:
                collumn = tr.find('th').text.replace(" ","")
                collumn = "".join(c for c in collumn if c.isalpha())
                collumn = "case" + collumn
                data = tr.find('td').text.lower()
                watch[collumn] = data

            # Dial info
            table = table.find_next('table', class_ = 'info-table')
            tableRows = table.find_all('tr')
            for tr in tableRows:
                collumn = tr.find('th').text.replace(" ","")
                collumn = "".join(c for c in collumn if c.isalpha())
                collumn = "dial" + collumn
                data = tr.find('td').text.lower()
                watch[collumn] = data

            # Add data to pandas df
            df.loc[j] = watch
            j += 1
        done = True
    except requests.exceptions.Timeout:
        print("Request timed out at index:", current_index)
        print("Sleeping...")
        sleep(60)
    except AttributeError:
        print("Unexpected error at index:", current_index)
        print("Sleeping...")
        sleep(60)
    finally:
        if done:
            start_index = len(referenceURLs)
        else:
            start_index = current_index + 1


# Export watch references as .csv file
df.to_csv('watches.csv')


