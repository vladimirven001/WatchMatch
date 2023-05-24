import sys
import csv
from selenium import webdriver
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from time import time
from time import sleep

driver = webdriver.Chrome(ChromeDriverManager().install())

option = webdriver.ChromeOptions()
option.add_argument(“ — incognito”)
driver = webdriver.Chrome(executable_path=’/Library/Application Support/Google/chromedriver’, chrome_options=option)