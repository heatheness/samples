#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
Статистическое исследование сообществ Вконтакта - немного измененное задание из курса Python ШАДа
http://courses.busin.usu.ru/wiki/index.php?title=Курс_ШАД_Python_(Иван_Бибилов)
Нужно сформировать статистику на основе 100 случайных клубов. Количество клубов можно увеличить, однако вконтаке выдает
ошибку при попытыке загрузить более одной страницы в секунду, что значительно увеличивает время выполнения. Использование
свободных прокси не помогает - они работают довольно медленно. Оптимальнее просто стучаться вконтакт и ждать страницы.
Информацию о клубе получаем, загружая HTML-страницу по адресу http://vk.com/club<id клуба>.
Например, http://vk.com/club2433350. Id клуба  берется как случайное число в диапазоне (1 000 000, 30 000 000), чтобы с
большой вероятностью попадать на "нормальные" (не приватные, не удаленные) клубы.
В итоге программа должна выдать 10 самых популярных слов в названиях клубов. Склонения, спряжения, падежи не учитываем,
все приводим к нижнему регистру. Словом считаем любую буквенную последовательность в Юникоде длинной более единицы
(внутри слова может быть символ дефис '-'). Есть список заранее определенных слов, которые нас не интересуют и в
статистике не учитываются.

Пример выводы результата по словам:
'группа', 8
'встреча', 7
'любителей', 6
'клуб', 5
'naruto', 5
'день', 5
'друзья', 5
'очень', 4
'хочет', 2

Статистика по количеству людей в группах:
В 10% клубов -- не более 51 человека.
В 20% клубов -- не более 102 человек.
...
В 100% клубов -- не более 200 000 человек.

"""

import re
from random import randrange
from HTMLParser import HTMLParser
from urllib2 import urlopen
from collections import Counter
import time
import codecs


start_time = time.time()
visited_clubs = set([])
words_in_club_titles = []
quantity_of_members = []

words_to_exclude = set([u'на', u'что', u'когда', u'где' ,u'куда', u'тут', u'из' ,u'по', u'не',
                        u'от', u'от', u'не', u'для', u'за']) #слова, которые мы отбрасываем
quantity_of_clubs = 100 # должно быть кратно 10
rx1 = re.compile(u'[^\w-]', re.UNICODE)
rx2 = re.compile(u'[\d+]', re.UNICODE)
rx3 = re.compile(u'-+', re.UNICODE)

f = codecs.open('vk.txt', mode = 'a', encoding= 'utf-8')
f.write('--------------------\n')
f.write(u'количество клубов - ' + str(quantity_of_clubs) + u'\n')

i = 1
while i <= quantity_of_clubs:
    club_number = randrange(1000000, 30000000)
    if club_number not in visited_clubs:
        visited_clubs.add(club_number)
        data = urlopen('http://vk.com/club%s' % club_number).read().decode('utf8')
        title = HTMLParser().unescape(re.findall('<title>(.*)</title>', data)[0])
        if title not in ([u'Ошибка', u'Частная группа']):
            quantity = HTMLParser().unescape(re.findall(u'Участники\s+<em class="pm_counter">(\d+)</em>',data))
            if quantity:
                quantity_of_members.append(int(quantity[0]))
                words = title.lower().split(' ')
                for word in words:
                    # отбрасываем слова единичной длины и слова из списка
                    if len(word) != 1 and word not in words_to_exclude:
                        new_word = rx3.sub(u'-', (rx2.sub(u'', rx1.sub(u'',word)))) # удаляем все кроме букв и '-'
                        # отбрасываем пустые слова, слова единичной длины и слова из списка
                        if new_word != '' and len(new_word) != 1 and new_word not in words_to_exclude:
                            words_in_club_titles.append(new_word)
                i +=1


counts = Counter(words_in_club_titles)
top = counts.most_common(10)
for element in top:
    print "'%s', %d " %(element[0], element[1])
    f.write("'%s', %d " %(element[0], element[1]))
    f.write('\n')


quantity_of_members.sort()
bins_length = quantity_of_clubs/10
quantity_of_members = [quantity_of_members[i:i+bins_length] for i in range(0,quantity_of_clubs,bins_length)]


n = 0
for i in range(10,110,10):
    print 'В %d%% клубов -- не более %d человек' %(i, (quantity_of_members[n][-1]))
    f.write(u'В %d%% клубов -- не более %d человек' %(i, (quantity_of_members[n][-1])))
    f.write('\n')
    n+=1

common_time = time.time() - start_time
f.write (u'общее время -  %f' %(common_time))
print 'общее время - %f' %(common_time)



