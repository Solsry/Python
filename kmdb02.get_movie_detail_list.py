'''
영화 진흥 위원회
제공 서비스) 영화 상세 정보
https://www.kobis.or.kr/kobisopenapi/homepg/main/main.do
'''
import requests
import json

accessToken = '268cb57735230360d3a842a55eaade81'

base_url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json'
base_url += '?key=' + accessToken

def dataExtractor(movieCD): # 20124079
    parameters = '&movieCd=' + str(movieCD)
    url = base_url + parameters
    # print(url)

    response = requests.get(url)
    # content = response.content
    # print(type(content))

    try:
        jsondata = response.json()
        return jsondata
    except Exception as err:
        print(err)
        print('JSON 데이터에 문제가 있습니다.')
        return None
# end def dataExtractor

totalData = list() # 전체 영화 상세 정보를 저장할 리스트

# 상세 정보를 찾고자 하는 영화들의 코드 목록
# 차후 2023년도 3월 '한국' 데이터만 읽어서 처리하자.
import pandas as pd

jsonFile = 'kmdb_get_movie_list(2022~2023).json'
kmdb = pd.read_json(jsonFile)

# 한국, 2023년 03월
korea = kmdb[kmdb['nationAlt']=='한국']
korea = korea[korea['openDt'].astype('str').str.startswith('202303')]
movieCodeList = korea['movieCd'].tolist()
# print(koreaMovieCode[0:5])

# movieCodeList = [20124079]#, 20231123]

# for movieCode in movieCodeList:
dataSize = len(movieCodeList)
print('총 데이터 건수 : ' + str(dataSize))
for idx in range(dataSize):
    moviedata = dataExtractor(movieCodeList[idx])
    # print(moviedata)
    # break
    print(str(idx+1) + ' / ' + str(dataSize) + ' 번째 데이터 작업 중입니다.')
    movie = moviedata['movieInfoResult']['movieInfo']
    # print(movie)
    totalData.append(movie)
# for movieCode

savedJsonFile = 'kmdb_get_movie_detail_list.json'
with open(savedJsonFile, mode='wt', encoding='UTF-8') as outfile :
    jsonObj = json.dumps(totalData, indent=4, sort_keys=False, ensure_ascii=False)
    outfile.write(jsonObj)
# end with

print(savedJsonFile + ' 파일이 생성되었습니다.')
print('finished')