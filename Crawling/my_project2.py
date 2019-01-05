import requests
from bs4 import BeautifulSoup as bs

url = "https://www.koreabaseball.com/Record/Player/HitterBasic/Detail1.aspx"

response = requests.get(url).text
doc = bs(response, "html.parser")
div = doc.select_one("#cphContents_cphContents_cphContents_udpContent")
table = div.select("table")

print(table[0].text)
