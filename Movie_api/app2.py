import requests
import os
from pprint import pprint as pp
import urllib.request
import csv

class Naver_movie:
    def __init__(self, title, movie_code):
        headers = {
            "X-Naver-Client-Id" : os.getenv("naver_id"),
            "X-Naver-Client-Secret" : os.getenv("naver_secret")
        }
             
        params = {
            "query" : title
        }
        url = 'https://openapi.naver.com/v1/search/movie.json'
        response = requests.get(url, headers = headers, params = params).json()

        self.__thumb_url = response['items'][0]['image']
        self.__link_url = response['items'][0]['link']
        self.__userRating = response['items'][0]['userRating']
        self.__movie_code = movie_code

    @property
    def movie_info(self):
        return {
            "thumb_url" : self.__thumb_url,
            "link_url" : self.__link_url,
            "userRating" : self.__userRating,
            "movie_code" : self.__movie_code
        }

with open('movie_naver.csv', 'w') as fm:
    field = ('movie_code','thumb_url','link_url','userRating')
    writer = csv.DictWriter(fm, fieldnames=field)
    writer.writeheader()
    with open('boxoffice.csv', newline='') as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            if i:
                movie = Naver_movie(row[1], row[0])
                writer.writerow(movie.movie_info)
                urllib.request.urlretrieve(movie.movie_info['thumb_url'], f"images/{movie.movie_info['movie_code']}.jpg")
