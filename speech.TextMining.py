dataInFolder = './../data/'
filename = dataInFolder + '윤석열 제20대 대통령 취임사.txt'

speech = open(filename, encoding='UTF-8').read()
#print(speech)




# 참조 url : https://konlpy.org/ko/latest/
from konlpy.tag import Komoran

# 사용자 정의 단어들을 정하고, 사용자 정의 사전에 추가하도록 합니다.
user_dict = dataInFolder + 'user_dic.txt' # 사용자 정의 사전
komo = Komoran(userdic=user_dict) # 객체 생성
token_list = komo.nouns(speech) # nouns : 명사만 추출
print('토큰 목록')
print(token_list)

# 불용어(stopword) : 빈도는 많지만, 분석시 중요하지 않다고 판단하는 단어들
stopword_file = dataInFolder + 'stopword.txt' # 불용어 파일
stop_file = open(stopword_file, encoding='UTF-8').readlines()
stop_words = [word.strip() for word in stop_file]
print('불용어 리스트')
print(stop_words)


new_token_list = [word for word in token_list if word not in stop_words]
print('불용어 제외된 토큰 목록')
print(new_token_list)

# 집합을 이용하여 불용어로 처리된 내용을 확인합니다.
set_token_list = set(token_list)
set_new_token_list = set(new_token_list)
diff = set_token_list.difference(set_new_token_list)
print('불용어 처리된 단어 확인')
print(diff)


import nltk # national language toolkit

nltk_token = nltk.Text(tokens=new_token_list)
bindo_size = 500 # 빈도수가 많은 500개
token_data = nltk_token.vocab().most_common(bindo_size)
print('토큰과 빈도수 확인')
print(token_data)

# 단어의 길이가 2이상, 빈도수가 2이상인 데이터만 추출하기
wordlist = list() # 튜플(단어, 빈도수)를 저장할 리스트
for word, bindo in token_data:
    if (len(word) >= 2 and bindo >= 2):
        wordlist.append((word, bindo))


# token_data 파일로 저장하기
print(wordlist)

import pandas as pd

savedWordFile = dataInFolder + 'word_list.csv'
dataframe = pd.DataFrame(wordlist, columns=['단어','빈도수'])
dataframe.to_csv(savedWordFile, encoding='CP949', index=False)
print(savedWordFile + '파일 저장이 완료 되었습니다.')


print('상위 top 10 개 막대 그래프')
barcount = 10
chartdata = dataframe.set_index('단어').iloc[0:barcount]

import matplotlib.pyplot as plt
plt.rc('font', family='Malgun Gothic')

chartdata.plot(kind='bar', rot=10, grid=True, use_index=True, legend=False)

plt.title('빈도' + str(barcount) + '개 상위 단어' ,size = 20)
plt.xlabel('주요 키워드', size = 12)
plt.ylabel('빈도 수' ,size = 12)

barFileName = dataInFolder + 'bar_chart.png'
plt.savefig(barFileName) # 저장하기
# plt.show() # 실행 시 그래프를 볼 수 있음
print(barFileName + ' 그래프가 생성 되었습니다.')

print('빈도를 이용한 워드 클라우드')
# 참조 url : https://amueller.github.io/word_cloud/index.html

import numpy as np
from PIL import Image # PIL : Python Image Library
from wordcloud import WordCloud

alice_color_file = dataInFolder + 'alice_color.png'
alice_color_array = np.array(Image.open(alice_color_file)) # 이미지 배열

word_dict = dict(wordlist) # 단어 사전


font_name = 'malgun.ttf' # 글꼴
mycloud = WordCloud(font_path=font_name, mask=alice_color_array,
                    background_color='white')
mycloud = mycloud.generate_from_frequencies(word_dict)

from wordcloud import ImageColorGenerator
# ImageColorGenerator : 컬러 이미지의 색상 톤을 유지하고자 할 때 사용되는 라이브러리
color_generator = ImageColorGenerator(alice_color_array)

mycloud = mycloud.recolor(color_func=color_generator)

plt.figure(figsize=(16, 8)) # 새 도화지 준비
plt.axis('off') # 그래프 테두리 없애기
plt.imshow(mycloud)

cloudFileName = dataInFolder + 'word_cloud.png'
plt.savefig(cloudFileName)

print(cloudFileName + ' 그래프가 생성 되었습니다.')


print('finished')






