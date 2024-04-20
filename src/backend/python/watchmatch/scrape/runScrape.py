import time
import subprocess

def run_my_script():
    subprocess.run(["python", "./src/backend/python/watchmatch/scrape/scrapeWatchBase.py"])

if __name__ == "__main__":
    while True:
        run_my_script()
        n = 30
        mins = n // 60
        secs = n - (mins * 60)
        print("Script executed. Waiting for ", mins ," minutes and ", secs," seconds")
        time.sleep(n)