from konlpy.tag import Komoran

sentence = '아버지가방에들어가신다.'
print('# before use r dic')
komo = Komoran()
print(komo.pos(sentence))
