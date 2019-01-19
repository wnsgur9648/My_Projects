# Movie_api 사용

app.py(주간 boxoffice)

```python
import requests
import os
import time
from datetime import date
import csv

names=[]
result=[]
for i in range(1, 11):
    day = date.fromtimestamp(time.time() - 60*60*24*(i*7-2))
    day = day.strftime("%Y%m%d")

    url = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchWeeklyBoxOfficeList.json"
    params = {
        "key": os.getenv("MOVIE_KEY"),
        "targetDt": day,
        "weekGb": "0"
    }
    response = requests.get(url, params = params).json()
    
    for i in range(10):
        if response['boxOfficeResult']['weeklyBoxOfficeList'][i]['movieNm'] not in names:
            result.append(
                {
                    'movie_code' : response['boxOfficeResult']['weeklyBoxOfficeList'][i]['movieCd'],
                    'title' : response['boxOfficeResult']['weeklyBoxOfficeList'][i]['movieNm'],
                    'audience' : response['boxOfficeResult']['weeklyBoxOfficeList'][i]['audiAcc'],
                    'recorded_at' : day
                }
            )
            names.append(response['boxOfficeResult']['weeklyBoxOfficeList'][i]['movieNm'])

with open('boxoffice.csv', 'w') as f:   #파일을 열고 닫는 코드를 넣지 않아도 됨
    field = tuple(result[0].keys())
    writer = csv.DictWriter(f, fieldnames=field)
    writer.writeheader()
    for r in result:
        writer.writerow(r)

```

```python
import requests
import os
from datetime import datetime, timedelta
import csv

class BoxofficeInfo:
    stored_movie_names = []
    def __init__(self, data, day):
        self.__rawdata = data['boxOfficeResult']['weeklyBoxOfficeList']
        self.__day = day
        
    def putName(self, name):
        BoxofficeInfo.stored_movie_names.append(name)
                
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
    for i in range(10):
        day = datetime(2019, 1, 13)
        day = day + timedelta(days=(-7*i))
        url = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchWeeklyBoxOfficeList.json"
        params = {
            "key": os.getenv("MOVIE_KEY"),
            "targetDt": day.strftime("%Y%m%d"),
            "weekGb": "0"
        }
        movies = BoxofficeInfo(requests.get(url, params = params).json(), day.strftime("%Y%m%d"))
        for movie in movies.movielist:
            if movie["title"] not in BoxofficeInfo.stored_movie_names:
                movies.putName(movie["title"])
                writer.writerow(movie)

```



*app1.py*(영화 세부내용)

```python
import requests
import os
from pprint import pprint as pp
import csv

class MovieInfo:
    def __init__(self, data):
        self.__actors = data["movieInfoResult"]["movieInfo"]["actors"]
        self.__audits = data["movieInfoResult"]["movieInfo"]["audits"]
        self.__directors = data["movieInfoResult"]["movieInfo"]["directors"]
        self.__genres = data["movieInfoResult"]["movieInfo"]["genres"]
        self.__prdtYear = data["movieInfoResult"]["movieInfo"]["prdtYear"]
        self.__movieNmEn = data["movieInfoResult"]["movieInfo"]["movieNmEn"]
        self.__movieNmOg = data["movieInfoResult"]["movieInfo"]["movieNmOg"]
        self.__movieNm = data["movieInfoResult"]["movieInfo"]["movieNm"]
        self.__movieCd = data["movieInfoResult"]["movieInfo"]["movieCd"]
    
    @property
    def actors(self):
        return [person["peopleNm"] for person in self.__actors]
        
    @property
    def watchGradeNm(self):
        return [element["watchGradeNm"] for element in self.__audits]
        
    @property
    def directors(self):
        return [person["peopleNm"] for person in self.__directors]
        
    @property
    def genres(self):
        return [genre["genreNm"] for genre in self.__genres]
        
    @property
    def prdtYear(self):
        return self.__prdtYear
        
    @property
    def movieNmEn(self):
        return self.__movieNmEn
        
    @property
    def movieNmOg(self):
        return self.__movieNmOg
        
    @property
    def movieNm(self):
        return self.__movieNm
        
    @property
    def movieCd(self):
        return self.__movieCd


with open('movie.csv', 'w') as fm:
    field = ('movie_code','movie_name_ko','movie_name_en','movie_name_og','prdt_year','genres','directors','watch_grade_nm','actor1','actor2','actor3')
    writer = csv.DictWriter(fm, fieldnames=field)
    writer.writeheader()
    with open('boxoffice.csv', newline='') as fb:
        reader = csv.reader(fb)
        for i, row in enumerate(reader):
            if i:
                url = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json"
                params = {
                    "key": os.getenv("MOVIE_KEY"),
                    "movieCd": row[0]
                }
                movie_info = MovieInfo(requests.get(url, params = params).json()) 
                tmp = {}
                tmp['movie_code'] = movie_info.movieCd
                tmp['movie_name_ko'] = movie_info.movieNm
                tmp['movie_name_en'] = movie_info.movieNmEn
                tmp['movie_name_og'] = movie_info.movieNmOg
                tmp['prdt_year'] = movie_info.prdtYear
                tmp['genres'] = "/".join(movie_info.genres)
                tmp['directors'] = "/".join(movie_info.directors)
                tmp['watch_grade_nm'] = "/".join(movie_info.watchGradeNm)
                if len(movie_info.actors) >= 3:
                    for i in range(3):
                        tmp[f'actor{i+1}'] = movie_info.actors[i]
                elif len(movie_info.actors) == 2:
                    for i in range(2):
                        tmp[f'actor{i+1}'] = movie_info.actors[i]
                    tmp['actor3'] = ""
                elif len(movie_info.actors) == 1:
                    tmp['actor1'] = movie_info.actors[0] 
                    tmp['actor2'] = ""  
                    tmp['actor3'] = ""  
                writer.writerow(tmp)
    
```

