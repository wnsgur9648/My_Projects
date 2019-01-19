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
    
