import requests
from bs4 import BeautifulSoup as bs

url = "https://www.youtube.com/channel/UC69uMhRJcUnvMnMxKT2SS0w/videos"

response = requests.get(url).text
document = bs(response, "html.parser")
a = document.select("h3 > a")

url = "https://www.youtube.com/" + a[0]["href"]
response = requests.get(url).text
document = bs(response, "html.parser")
spans = document.select("span.view-count")

for span in spans:
    print(span.text)
    

    

