import numpy as np
import random

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Segment:
    def __init__(self, a: Point, b: Point):
        self.a = a
        self.b = b


class TreeSegm:
    """Класс описывающий отрезок"""

    def __init__(self, a: Point, b: Point, aFlag: bool, bFlag: bool):
        self.a = a
        self.b = b
        self.aFlag = aFlag
        self.bFlag = bFlag

    def turn(self, p: Point):  # сравнить, в положительное или отрицательное полупространство попадает точка
        tax, tay, tbx, tby, tpx, tpy = self.a.x, self.a.y, self.b.x, self.b.y, p.x, p.y
        return tax * tby - tax * tpy + tay * tpx - tay * tbx + tbx * tpy - tby * tpx

    def cross(self, p1: Point, p2: Point):  # найдем точку пересечения нашего и данного отрезка
        x1, x2, y1, y2, x3, x4, y3, y4 = self.a.x, self.b.x, self.a.y, self.b.y, p1.x, p2.x, p1.y, p2.y
        x = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / (
                (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4))
        y = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / (
                (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4))

        return Point(x, y)


class BSPTree:
    """Двоичное дерево left - ребенок для h+, right - для h-"""

    def __init__(self, s: []):
        self.s = []
        if len(s) <= 1:
            self.s = s
            self.isLeaf = True
        else:
            self.isLeaf = False
            sPlus = []
            sMinus = []

            s1 = s[0]
            for s2 in s:  # нахождение свободных разбиений
                if s2.aFlag and s2.bFlag:
                    s1 = s2
                    break

            for s2 in s:  # распределение отрезков по множествам
                if s1.turn(s2.a) > 0:
                    if s1.turn(s2.b) > 0:
                        sPlus.append(s2)
                    elif s1.turn(s2.b) == 0:
                        sPlus.append(TreeSegm(s2.a, s2.b, s2.aFlag, True))
                    else:
                        sPlus.append(TreeSegm(s2.a, s1.cross(s2.a, s2.b), s2.aFlag, True))
                        sMinus.append(TreeSegm(s1.cross(s2.a, s2.b), s2.b, True, s2.bFlag))
                elif s1.turn(s2.a) < 0:
                    if s1.turn(s2.b) < 0:
                        sMinus.append(s2)
                    elif s1.turn(s2.b) == 0:
                        sMinus.append(TreeSegm(s2.a, s2.b, s2.aFlag, True))
                    else:
                        sMinus.append(TreeSegm(s2.a, s1.cross(s2.a, s2.b), s2.aFlag, True))
                        sPlus.append(TreeSegm(s1.cross(s2.a, s2.b), s2.b, True, s2.bFlag))
                else:
                    if s1.turn(s2.b) < 0:
                        sMinus.append(TreeSegm(s2.a, s2.b, True, s2.bFlag))
                    elif s1.turn(s2.b) == 0:
                        self.s.append(s2)
                    else:
                        sPlus.append(TreeSegm(s2.a, s2.b, True, s2.bFlag))

            # рекурсивный запуск
            self.minusChild = BSPTree(sMinus)
            self.plusChild = BSPTree(sPlus)


def Random_BSPTree(s: []):
    """Рандомизированное дерево"""
    # добавляем возможность улавливать свободное разбиение
    sUpgraded = []
    for s1 in s:
        sUpgraded.append(TreeSegm(s1.a, s1.b, False, False))
    # случайно перемешаем для случайности данных
    random.shuffle(sUpgraded)
    return BSPTree(sUpgraded)
