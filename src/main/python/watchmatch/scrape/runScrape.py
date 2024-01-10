import time
import subprocess
import datetime

def run_my_script():
    subprocess.run(["python", "./src/main/python/watchmatch/scrape/scrapeWatchBase.py"])

if __name__ == "__main__":
    while True:
        run_my_script()
        print("Script executed. Waiting for 5 minutes and 2 seconds")
        time.sleep(302)