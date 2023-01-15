import requests
from bs4 import BeautifulSoup
import time

url = "https://www.freepik.com/free-photos-vectors/abstract-background"

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
}

resp = requests.get(url, headers=headers)

soup = BeautifulSoup(resp.text, "html.parser")
section = soup.find("section").find_all("a", class_="showcase__link js-detail-data-link" )

for i in section:
    href = i.get("href")
    href_free_d = href.split("/")[-2].split("-")[0]
    if href_free_d == "free":
        print(href)
    time.sleep(1)
