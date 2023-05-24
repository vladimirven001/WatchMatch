from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import pandas as pd

HEADERS = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"}
database = requests.get("https://www.chrono24.ca/search/browse.htm", headers=HEADERS)
soup = BeautifulSoup(database.content, "html.parser")
section = soup.find_all("section")
print(len(section))
# print(section)

brands = soup.find_all("a") # List to store brand of the watch
family=[] # List to store family of the watch
reference=[] # List to store reference of the watch
movement=[] # List to store movement of the watch
year=[] # List to store year of the watch

print(brands)
for b in brands:
    print(b)