import requests
import os
from datetime import datetime, timedelta
from pprint import pprint as pp
import csv

class BoxofficeInfo:
    stored_movie_names = []
    def __init__(self, data, day):
        self.__rawdata = data['boxOfficeResult']['weeklyBoxOfficeList']
        self.__day = day
        for l in data['boxOfficeResult']['weeklyBoxOfficeList']:
            if l['movieNm'] not in BoxofficeInfo.stored_movie_names:
                BoxofficeInfo.stored_movie_names.append(l['movieNm'])

    @property
    def movielist(self):
        result = []
        for l in self.__rawdata:
            tmp = {}
            for key in l:
                if key == "movieCd":
                    tmp["movie_code"] = l[key]
                elif key == "movieNm":
                    tmp["title"] = l[key]
                elif key == "audiAcc":
                    tmp["audience"] = l[key]
            else:
                tmp["recorded_at"] = self.__day
                result.append(tmp)
        return result
        
with open('boxoffice.csv', 'w') as f: 
    field = ('movie_code','title','audience','recorded_at')
    writer = csv.DictWriter(f, fieldnames=field)
    writer.writeheader()
    for i in range(0):
        day = datetime(2019, 1, 13)
        day = day + timedelta(days=(-7*i))
        
        url = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchWeeklyBoxOfficeList.json"
        params = {
            "key": os.getenv("MOVIE_KEY"),
            "targetDt": day.strftime("%Y%m%d"),
            "weekGb": "0"
        }
        movies = BoxofficeInfo(requests.get(url, params = params).json(), day.strftime("%Y%m%d"))
        print("BoxofficeInfo.stored_movie_names")
        pp(BoxofficeInfo.stored_movie_names)
        print("movies.movielist")
        pp(movies.movielist)
        for movie in movies.movielist:
            if movie["title"] not in BoxofficeInfo.stored_movie_names:
                writer.writerow(movie)
