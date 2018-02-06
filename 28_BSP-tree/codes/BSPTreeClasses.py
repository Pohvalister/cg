import numpy as np
import random


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Segment:
    def __init__(self,a:Point,b:Point):
        self.a=a
        self.b=b

class TreeSegm:
    """Класс описывающий отрезок"""

    def __init__(self, a: Point, b: Point, aFlag:bool, bFlag:bool):
        self.a = a
        self.b = b
        self.aFlag=aFlag
        self.bFlag=bFlag

    def turn(self, p: Point):  # сравнить, в положительное или отрицательное полупространство попадает точка
        tax = self.a.x; tay = self.a.y; tbx = self.b.x; tby = self.b.y; tpx = p.x; tpy = p.y
        return tax * tby - tax * tpy + tay * tpx - tay * tbx + tbx * tpy - tby * tpx

    def cross(self, p1: Point, p2: Point):#найдем точку пересечения нашего и данного отрезка
        x=((p1.x*p2.y-p2.x*p1.y)*(self.a.x-self.b.x)-(self.b.x*self.a.y-self.a.x*self.b.y)*(p2.x-p1.x))/((p1.y-p2.y)*(self.a.x-self.b.x)-(self.b.y-self.a.y)*(p2.x-p1.x))
        y=((self.b.y-self.a.y)*x - (self.b.x*self.a.y-self.a.x*self.b.y))/(self.a.x-self.b.x)
        return Point(x,y)



class BSPTree:
    """Двоичное дерево left - ребенок для h+, right - для h-"""

    def __init__(self, s: [TreeSegm]):
        if len(s) <= 1:
            self.s = s
        else:
            sPlus = []
            sMinus = []

            s1 = s[0]
            for s2 in s:#нахождение свободных разбиений
                if s2.aFlag and s2.bFlag:
                    s1=s2
                    break


            for s2 in s:#распределение отрезков по множествам
                if s1.turn(s1, s2.a) > 0:
                    if s1.turn(s1, s2.b) > 0:
                        sPlus.append(s2)
                    elif s1.turn(s1, s2.b)==0:
                        sPlus.append(TreeSegm(s2.a,s2.b,s2.aFlag,True))
                    else:
                        sPlus.append(TreeSegm(s2.a, s1.cross(s2),s2.aFlag,True))
                        sMinus.append(TreeSegm(s1.cross(s2), s2.b, True, s2.bFlag))
                elif s1.turn(s1, s2.a) < 0:
                    if s1.turn(s1, s2.b) < 0:
                        sMinus.append(s2)
                    elif s1.turn(s1, s2.b)==0:
                        sMinus.append(TreeSegm(s2.a,s2.b,s2.aFlag,True))
                    else:
                        sMinus.append(TreeSegm(s2.a, s1.cross(s2), s2.aFlag, True))
                        sPlus.append(TreeSegm(s1.cross(s2), s2.b, True, s2.bFlag))
                else:
                    if s1.turn(s1, s2.b) < 0:
                        sMinus.append(TreeSegm(s2.a,s2.b,True,s2.bFlag))
                    elif s1.turn(s1, s2.b) == 0:
                        self.s = s2
                    else:
                        sPlus.append(TreeSegm(s2.a,s2.b,True,s2.bFlag))

            #рекурсивный запуск
            self.left = BSPTree(sMinus)
            self.right = BSPTree(sPlus)

    def visit(self):
        pass


def Random_BSPTree(s: [Segment]):
    """Рандомизированное дерево"""
    #добавляем возможность улавливать свободное разбиение
    sUpgraded = [TreeSegm]
    for s1 in s:
        sUpgraded.append(TreeSegm(s1.a,s1.b,False,False))
    #случайно перемешаем для случайности данных
    random.shuffle(sUpgraded)
    return BSPTree(sUpgraded)
