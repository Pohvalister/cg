import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy


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
