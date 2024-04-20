import requests
from bs4 import BeautifulSoup 

def scrape_brand_names():
    database = requests.get("https://watchbase.com/watches", headers={"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"})
    soup = BeautifulSoup(database.content, "html.parser")
    brands = [] # List to store brand of the watch (roots of the trees)
    mainDiv = soup.find('div', id = "brand-container")
    mainHeaders = mainDiv.find_all('h2')
    file3 = open("./src/backend/ressources/brandNames.txt",'w')
    for brand in mainHeaders:
        brands.append(brand.text.strip())
        file3.write(brand.text.strip() + "\n")
    file3.close()
    print("found brand names")
