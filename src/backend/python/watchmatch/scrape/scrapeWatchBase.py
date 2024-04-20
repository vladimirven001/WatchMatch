from bs4 import BeautifulSoup
import requests
import pandas as pd
from time import sleep
import random
import json
import traceback

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

def scrape_brand_names():
    mainDiv = soup.find('div', id = "brand-container")
    mainHeaders = mainDiv.find_all('h2')
    file3 = open("./src/backend/ressources/brandNames.txt",'w')
    for brand in mainHeaders:
        brands.append(brand.text.strip())
        file3.write(brand.text.strip())
    file3.close()
    print("found brand names")
    
def scrape_reference_URLs():
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
            referenceURLs.append(a['href'])
        sleep(1)

    # Save data
    file1 = open("./src/backend/ressources/referenceURLs.txt","w")
    file1.write(str(referenceURLs))
    file1.close
    print("found referenceURLs")

def scrape_Watchbase():
    # Create data structure to store watch references and information
    df = pd.DataFrame(columns = ["brand","family","reference","name","movement","produced","limited","caseMaterial",
                                "caseGlass","caseBack","caseShape","caseDiameter","caseHeight","caseLugWidth","dialColor",
                                "dialMaterial","dialIndexes","dialHands","image", "price"])

    # Get the information for each watch reference
    j=0
    file1 = open("./src/backend/ressources/referenceURLs.txt","r")
    referenceURLs = eval(file1.read())
    file1.close
    print("found referenceURLs")
    print("len(referenceURLs) = ", "")
    print(len(referenceURLs))
    done = False
    timeout = 10
    start_index = 0
    error_count=0

    try:
        file2 = open("./src/backend/ressources/start_index.txt", 'r')
        start_index = int(file2.read())
        file2.close()
    except:
        start_index = 0

    while start_index < len(referenceURLs):
        done = False
        curr_index = start_index
        
        try:
            for i in range(curr_index, len(referenceURLs) - 1):
                print("curr_index: " + str(curr_index))
                print("curr_watch: " + str(referenceURLs[i]))
                watch = {"brand":"","family":"","reference":"","name":"","movement":"","produced":"","limited":"","caseMaterial":"",
                                        "caseGlass":"","caseBack":"","caseShape":"","caseDiameter":"","caseHeight":"","caseLugWidth":"","dialColor":"",
                                        "dialMaterial":"","dialIndexes":"","dialHands":"","image":"", "price":""}
                randomNum = random.randint(0,5)
                referencePage = requests.get(referenceURLs[i], headers=HEADERS[randomNum], timeout=timeout)
                soupModel = BeautifulSoup(referencePage.content, "html.parser")
                table = soupModel.find('table', class_ = 'info-table')
                tableRows = table.find_all('tr')
                for tr in tableRows:
                    try:
                        collumn = tr.find('th').text.lower()
                        collumn = "".join(c for c in collumn if c.isalpha())
                        data = tr.find('td').get_text(strip = True).lower()
                        watch[collumn] = data
                    except:
                        continue
                div = soupModel.find('div', class_ = 'col-xs-6')
                
                # Case info
                table = div.find('table', class_ = 'info-table')
                tableRows = table.find_all('tr')
                for tr in tableRows:
                    try:
                        collumn = tr.find('th').text.replace(" ","")
                        collumn = "".join(c for c in collumn if c.isalpha())
                        collumn = "case" + collumn
                        data = tr.find('td').get_text(strip = True).lower()
                        watch[collumn] = data
                    except:
                        continue

                # Dial info
                table = table.find_next('table', class_ = 'info-table')
                tableRows = table.find_all('tr')
                for tr in tableRows:
                    try:
                        collumn = tr.find('th').text.replace(" ","")
                        collumn = "".join(c for c in collumn if c.isalpha())
                        collumn = "dial" + collumn
                        data = tr.find('td').get_text(strip = True).lower()
                        watch[collumn] = data
                    except:
                        continue

                # Image info
                div = div.find_next('div', class_ = 'col-xs-6')
                if div is not None:
                    picture = div.find('picture')
                    if picture is not None:
                        img = picture.find('img')
                        watch["image"] = img['src']

                # Price info
                div = soupModel.find('div', id = 'pricechart-container')
                if div is not None:
                    try:
                        canvas = div.find('canvas', id='pricechart')
                        priceURL = canvas['data-url']
                        pricePage = requests.get(priceURL, headers=HEADERS[0])
                        priceModel = BeautifulSoup(pricePage.content, "html.parser")
                        data_text = priceModel.get_text()
                        data = json.loads(data_text)
                        # Extracting the latest non-null element from 'data' list
                        latest_value = None
                        for value in reversed(data['datasets'][0]['data']):
                            if value is not None:
                                latest_value = value
                                break
                        print(latest_value)
                        watch["price"] = latest_value
                    except:
                        continue

                # Add data to pandas df
                df.loc[j] = watch
                j+=1
                curr_index += 1
            done = True

        except requests.exceptions.Timeout:
            print("Request timed out at index: ", curr_index)
            print("Sleeping...")
            sleep(30)
            error_count+=1

        except AttributeError as e:
            print("Unexpected error at index: ", curr_index)
            print("URL of index ", curr_index, ": ", referenceURLs[curr_index])
            print("error: ")
            print(traceback.format_exc())
            str_df = df.to_string
            print("current watches: " + str(str_df))
            print("Sleeping...")
            sleep(30)
            error_count+=1

        finally:
            if done:
                start_index = len(referenceURLs)
            else:
                start_index = curr_index
        if error_count == 1:
            print("reached max error amount, stopping program")
            break
        
    # Get previous data from df
    try:
        old_df = pd.read_csv('./src/backend/ressources/watches.csv')
    except:
        old_df = pd.DataFrame(columns = ["brand","family","reference","name","movement","produced","caseMaterial",
                                        "caseGlass","caseBack","caseShape","caseDiameter","caseHeight","caseLugWidth","dialColor",
                                        "dialMaterial","dialIndexes","dialHands","image", "price"])

    # Concat data
    df = pd.concat([old_df, df], ignore_index=True)

    # Export watch references as .csv file
    df.to_csv('./src/backend/ressources/watches.csv', index=False)

    file3 = open("./src/backend/ressources/start_index.txt", 'w')
    file3.write(str(curr_index))
    file3.close()

if __name__ == "__main__":
    scrape_reference_URLs()