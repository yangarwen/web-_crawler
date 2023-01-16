import requests
from lxml import etree
import openpyxl

wb = openpyxl.Workbook()
sheet = wb.create_sheet("電影分數",0)

url = "https://www.litv.tv/vod/movie/list.do"

resp = requests.get(url)
#print(resp.text)

tree = etree.HTML(resp.text)
cell = tree.xpath("/html/body/div[3]/div[2]/div[2]/div")

for i in cell:
    allatonce = i.xpath("./a[2]/*/text()")
    #score = i.xpath("./a[2]/span/text()")
    #title = i.xpath("./a[2]/h2/text()")
    #description = i.xpath("./a[2]/p/text()")
    sheet.append(allatonce)
wb.save("movie_0116.xlsx")
