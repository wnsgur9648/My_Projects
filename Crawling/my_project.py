import requests
from bs4 import BeautifulSoup as bs

url = "https://www.youtube.com/channel/UC4ab7V7p1hW4YiuCRZL1Bzg/videos"

response = requests.get(url).text
document = bs(response, "html.parser")
a = document.select("h3 > a")

for i in a:
    url = "https://www.youtube.com/" + i["href"]
    response = requests.get(url).text
    document = bs(response, "html.parser")
    a = document.select("div")

    print(a)
            

    

