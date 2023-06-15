'''
영화 진흥 위원회
제공 서비스) 영화 목록
https://www.kobis.or.kr/kobisopenapi/homepg/main/main.do
'''
import math
import requests
import json

accessToken = '268cb57735230360d3a842a55eaade81'

base_url = 'http://kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieList.json'
base_url += '?key=' + accessToken

itemPerPage = 100 # 사이트에서 최대 100까지만 제공하고 있음

# curPage : 현재 진행중인 페이지, thisyear : 검색 년도, getAllData : True이면 전체 검색
def dataExtractor(curPage, thisyear, getAllData=False):
    parameters = '&curPage=' + str(curPage)
    parameters += '&itemPerPage=' + str(itemPerPage)

    if getAllData == False :
        # openStartDt : YYYY 형식의 조회 시작 개봉 연도
        parameters += '&openStartDt=' + str(thisyear)

    url = base_url + parameters
    # print(url)

    response = requests.get(url)
    # content = response.content
    # print(type(content))

    try :
        jsondata = response.json()
        return jsondata
    except Exception as err :
        print(err)
        print('JSON 데이터에 문제가 있습니다.')
        return None
# end def dataExtractor

print('크롤링 중입니다. 잠시만 기다려 주세요.')

startYear, endYear = 2022, 2023 # 검색 시작, 종료 년도

totalData = list() # 전체 영화 목록을 저장할 리스트

for thisyear in range(startYear, endYear+1):
    print('\n%s년도 크롤링 중입니다.' % (thisyear))
    curPage = 1 # 현재 페이지를 의미합니다.

    while True:
        moviedata = dataExtractor(curPage, thisyear)
        # print(moviedata)

        totCnt = moviedata['movieListResult']['totCnt']
        if curPage == 1 :
            print('데이터 총 개수 : ' + str(totCnt))

        if totCnt == 0:
            break  # 데이터가 없으면 종료

        totalPage = math.ceil(totCnt/itemPerPage) # 전체 페이지수
        print('현재 진행 중인 페이지 : ' + str(curPage) + '/' + str(totalPage))

        for movie in moviedata['movieListResult']['movieList']:
            totalData.append(movie) # 각 영화를 리스트에 저장하기
        #end for

        if curPage == totalPage:
        # if curPage == 3:
            break

        curPage += 1
# end for thisyear

# print(totalData)

print('크롤링이 끝났습니다.')

# csv 파일 또는 Json 파일로 만들기
savedJsonFile = 'kmdb_get_movie_list(' + str(startYear) + '~' + str(endYear) + ').json'
with open(savedJsonFile, mode='wt', encoding='UTF-8') as outfile :
    jsonObj = json.dumps(totalData, indent=4, sort_keys=True, ensure_ascii=False)
    outfile.write(jsonObj)
# end with

print(savedJsonFile + ' 파일이 생성되었습니다.')
print('finished')