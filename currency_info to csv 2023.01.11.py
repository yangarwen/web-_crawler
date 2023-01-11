import requests
from bs4 import BeautifulSoup
import csv

url = 'https://rate.bot.com.tw/xrt?Lang=zh-TW'
resp = requests.get(url)
soup = BeautifulSoup(resp.text, 'html.parser')

money = soup.find('tbody')
moneydet = money.find_all('tr')


with open("currency.csv", 'w') as f:
    csvwriter = csv.writer(f)
    csvwriter.writerow(['幣別', '本行買入', '本行賣出', '本行買入', '本行賣出'])
    
    for t in moneydet:
        currency = t.find_all('div', class_="visible-phone print_hide")
        count = t.find_all('td')
        csvwriter.writerow([currency[0].text.strip(), count[1].text.strip(), count[2].text.strip(), count[3].text.strip(), count[4].text.strip()])
f.close()
