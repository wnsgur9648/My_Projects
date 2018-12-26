import requests
from bs4 import BeautifulSoup as bs

url = "https://www.youtube.com/channel/UC4ab7V7p1hW4YiuCRZL1Bzg"

response = requests.get(url).text
document = bs(response, "html.parser")
div = document.select("div h3")
            
for i in div:
    print(i.text)
            

    

