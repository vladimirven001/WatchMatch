from bs4 import BeautifulSoup
import requests
import pandas as pd

# Initialize soup
HEADERS = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"}
database = requests.get("https://www.chrono24.ca/search/browse.htm", headers=HEADERS)
soup = BeautifulSoup(database.content, "html.parser")

brands = [] # List to store brand of the watch
family=[] # List to store family of the watch
reference=[] # List to store reference of the watch
movement=[] # List to store movement of the watch
year=[] # List to store year of the watch

# Find all brands and format as list
mainDiv = soup.find_all("div", class_ = "letter-register")
for tag in mainDiv:
    brand = tag.find_all("a")
    for b in brand:
        brands.append(b.text.strip())

print(len(brands))
