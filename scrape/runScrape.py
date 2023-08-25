import time
import subprocess

def run_my_script():
    subprocess.run(["python", "E:\Fichiers\Programming\WatchMatch\scrape\scrapeWatchBase.py"])

if __name__ == "__main__":
    while True:
        run_my_script()
        print("Script executed. Waiting for 10 minutes...")
        time.sleep(600)