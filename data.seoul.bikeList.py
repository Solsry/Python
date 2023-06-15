import requests
from itertools import count

'''
서울 특별시 공공 자전거 실시간 대여 정보
'''
accessToken = '인증키발급받으세요' # 인증키

totallist = list() # 모든 데이터가 저장될 list
pageSize = 1000 # 한번에 읽어올 데이터 개수

print('크롤링을 시작합니다. 잠시만 기다려 주세요.')

for pageNumber in count():
    # print(pageNumber)
    beginRow = str(pageNumber * pageSize + 1)
    endRow = str((pageNumber+1) * pageSize)

    url = 'http://openapi.seoul.go.kr:8088/' + accessToken + '/json/bikeList/' + beginRow + '/' + endRow
    # print(url)

    message = '범위 : ' + beginRow + '~' + endRow
    print(message)

    response = requests.get(url) # response : 응답 객체
    # print(dir(response))

    content = response.content
    # print(type(content)) # byte 타입

    jsondata = response.json() # json 형식으로 변환
    # print(jsondata)
    # print('-'*30)

    try:
        datalist = jsondata['rentBikeStatus']['row']
        # print(len(datalist))
        for data in datalist:
            totallist.append(data)

    except Exception as err:
        print('더 이상 데이터가 없어 오류가 발생하였습니다.')
        print(err)
        break

    # if pageNumber == 1 :
    #     break
# end for pageNumber

print('크롤링이 종료 되었습니다.')

# print(totallist)

import pandas as pd

filename = './../data/bikeList.csv'
myframe = pd.DataFrame(totallist)
myframe.to_csv(filename)
print(filename + ' 파일이 저장되었습니다.')