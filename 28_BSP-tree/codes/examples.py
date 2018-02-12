import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy
from .BSPTreeClasses  import *


def show_bad_3D_example(N: int, E: float):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    for i in range(0, N):
        X, Y, Z = [0, N], [i, i], [0 * i, N * i]
        ax.plot(X, Y, Z)

    for i in range(0, N):
        X, Y, Z = [i, i], [0, N], [float(0 * i) + E, float(N * i) + E]
        ax.plot(X, Y, Z)

    plt.show()

def painter_interactive(s: []):
    global tree, figure
    tree =Random_BSPTree(s)

    figure = plt.figure(num=' ', figsize=(12, 5), dpi=65)
    plt.gcf().canvas.mpl_connect('button_press_event', on_click)
    # plt.gcf().canvas.mpl_connect('motion_notify_event', on_move)
    plt.plot([0, 0, 500, 500, 0], [0, 500, 500, 0, 0], 'g--')
    plt.axis('off')
    plt.margins(0.01)
    for s1 in s:
        plt.plot([s1.a.x, s1.b.x], [s1.a.y, s1.b.y])
    plt.show()


def placeLine(s, num):
    plt.plot([s.a.x, s.b.x], [s.a.y, s.b.y])
    plt.annotate(num, xy=((s.a.x + s.b.x) / 2, (s.a.y + s.b.y) / 2), )
    return num + 1


def draw(t: BSPTree, point: Point, num):
    if t.isLeaf:
        for s in t.s:
            num = placeLine(s, num)
        return num
    elif t.s[0].turn(point) > 0:
        num = draw(t.minusChild, point, num)
        for s in t.s:
            num = placeLine(s, num)

        num = draw(t.plusChild, point, num)
        return num
    elif t.s[0].turn(point) < 0:
        num = draw(t.plusChild, point, num)
        for s in t.s:
            num = placeLine(s, num)

        num = draw(t.minusChild, point, num)
        return num

    else:
        num = draw(t.plusChild, point, num)
        num = draw(t.minusChild, point, num)
        return num


def on_click(event):
    global click_point, tree
    if not event.dblclick:
        click_point = Point(int(round(event.xdata)), int(round(event.ydata)))
        # Очистим карту
        figure.clear()
        plt.axis('off')
        plt.margins(0.01)
        plt.plot([0, 0, 500, 500, 0], [0, 500, 500, 0, 0], 'g--')
        # Перерисуем карту с порядком выбора линий
        # plt.plot(X, Y_10, 'bD:', label=u'Температура 10 \u00b0C')
        draw(tree, click_point, 1)
        plt.plot(click_point.x, click_point.y, 'ro')
        plt.show()
