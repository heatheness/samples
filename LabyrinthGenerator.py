# -*- coding: utf-8 -*-


"""Генерирует проходимые лабиринты m x n. Каждая из m строк лабринта содержит n символов: «.» — проходимый участок и «#»
—  непроходимый. Левый верхний и правый нижний участки лабиринта проходимы. С одного проходимого участка можно попасть
на соседний либо по вертикали, либо по горизонтали. Для удобства вывода лабиринт представлен одной строкой, разделенной
символами перехода но новую строку"""

import random

def gen_lab(m,n):
    """генерирует лабиринт"""

    def lab_to_string(lab):
        """преобразует лабиринт (лист листов) в строку"""
        s = ''
        for i in lab:
            s = s + ''.join(i) + '\n'
        return s

    def gen_filed(m):
        """генерирует поле точек размером m x n"""
        l = [ ['.'] * n for i in xrange(m)]
        return l


    def gen_route(l):
        """генерирует случайный мрашрут"""
        visited = []
        route = []
        plan = [[(0,0),None]] # координаты точки и координаты точки-родителя
        u = m-1
        v = n-1
        while True:
            cur = plan.pop()
            directs = []
            if cur[0] in visited:
                continue
            elif cur[0] == (u,v):
                break
            else:
                route.append(cur[0])
                visited.append(cur[0])
                i,j = cur[0]
                if (j-1) >= 0 and ((i,j-1) not in visited):
                    directs.append([(i,j-1),cur[0]])
                if (i+1) <= u and ((i+1,j) not in visited):
                    directs.append([(i+1,j),cur[0]])
                if (j+1) <= v and ((i,j+1) not in visited):
                    directs.append([(i,j+1),cur[0]])
                if (i-1) >= 0 and ((i-1,j)not in visited):
                    directs.append([(i-1,j),cur[0]])
                if not directs:
                    # если идти больше некуда, и выход не достигнут, то нужно откатиться к той точке, из которой
                    # можно двигаться. т.е. удаляем из маршрута те точки, которые завели в тупик
                    route.pop()
                    new_cur_par = plan[-1][1]# верхняя точка в плане
                    while True:
                        # если верхняя точка листа маршрута не является родителем верхней точки в плане,
                        # удаляем эту точку из маршрута (верхнюю точку маршрута). это и есть откат к перспективной
                        #  точке. идет коррекция маршрута - отсекаем тупиковую ветвь
                        if route[-1] != new_cur_par:
                            route.pop()
                        else:
                            break
                    continue
                else:
                    random.shuffle(directs) # перемешиваем направления движения
                    plan.extend(directs) # добавляем направления в план обхода
        route.append((u,v))
        return route


    def gen_walls(l, route):
        """генерирует стены в лабиринте"""
        w = len(l)*len(l[0])
        # вероятность построения стен зависит от отношения длины пути к размеру лабиринта
        # чем больше путь, тем больше вероятность, что на свободных местах появятся стены
        if w <= 100:
            p = 8
        else:
            p = max(int(len(route)*10.0/w**2),4) # корректировка, чтобы не было совсем пусто
        for i in xrange(m):
            for j in xrange(n):
                if (i,j) not in route:
                    key = random.randint(0,11)
                    if key <= p:
                        l[i][j]='#'



    l = gen_filed(m)

    while True:
        way = gen_route(l)
        w = len(way)
        if (w != m**2) or (w==1) :
            break

    gen_walls(l,way)

    return lab_to_string(l)


dim = raw_input().split(',')
m = int(dim[0])
n = int(dim[1])
s = gen_lab(m,n)
print s







