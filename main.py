import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.animation import PillowWriter


def fun(T0):
    # Функция ищет значения коэффициентов квадратичного уравнения для аппроксимации функций x(t) и y(t)
    # и возвращает прогнозированное значение функции и ее производной,
    # а так же величину отклонения от формулы окружности.

    g0 = 9.81 + 0.05 * math.sin(2 * math.pi * t0)
    # g0 = 9.81

    # for x(t)
    F0 = -x0 * T0 / m / L
    Ax0 = F0 / 2 / m
    Bx0 = u0 - F0 / m * t0
    Cx0 = x0 - Ax0 * t0 ** 2 - Bx0 * t0
    x1 = Ax0 * (t0 + dt) ** 2 + Bx0 * (t0 + dt) + Cx0
    u1 = 2 * Ax0 * (t0 + dt) + Bx0

    # y(t)
    G0 = -y0 * T0 / m / L - g0
    Ay0 = G0 / 2 / m
    By0 = v0 - G0 / m * t0
    Cy0 = y0 - Ay0 * t0 ** 2 - By0 * t0
    y1 = Ay0 * (t0 + dt) ** 2 + By0 * (t0 + dt) + Cy0
    v1 = 2 * Ay0 * (t0 + dt) + By0

    return x1, u1, y1, v1, (x1 ** 2 + y1 ** 2) ** 0.5 - L


def findT0():
    # Итерационно ищем значение натяжения стержня Т0. Критерий - удовлетворение формуле окружности.
    # while ограничена 1000 итерациями.

    T0 = 0
    x1, u1, y1, v1, crit1 = fun(T0)
    dT0 = 10
    k = 0
    while True:
        _, _, _, _, crit2 = fun(T0 + dT0)

        if abs(crit2) < 0.001: break

        if crit1 > 0 and crit2 > 0:
            if crit1 < crit2:
                dT0 = -dT0
        elif crit1 < 0 and crit2 < 0:
            if crit1 > crit2:
                dT0 = -dT0
        elif crit1 > 0 and crit2 < 0:
            dT0 = -dT0 / 2
        elif crit1 < 0 and crit2 > 0:
            dT0 = -dT0 / 2
        T0 = T0 + dT0
        crit1 = crit2

        if k > 1000:
            print("1000 iterations reached, no convergence with T0 ", T0, dT0)
            return T0
        else:
            k = k + 1

    return T0

# Основная часть
m = 1
L = 5

t0 = 0.0
dt = 0.0001
tk = 100

x0 = 3
u0 = 0
y0 = 4
v0 = 0

data = np.zeros((int(tk / dt) + 1, 5))

for i in range(int(tk / dt) + 1):
    t0 = i * dt
    # print(t0, 9.81 + 0.05 * math.sin(2 * math.pi * t0))
    T0 = findT0()
    x1, u1, y1, v1, crit1 = fun(T0)

    # print(t0, x0, y0, crit1, T0)
    data[i] = np.array([t0, x0, y0, crit1, T0])
    x0 = x1
    u0 = u1
    y0 = y1
    v0 = v1

fig = plt.figure()
plt.xlim(0, tk)
plt.ylim(-6, 6)
plt.xlabel(r'$t$')
plt.ylabel(r'$x(t)$, $y(t)$')
plt.title(f'$Шаг dt = {dt}$')
plt.grid()
# plt.plot(data[:, 0], data[:, 2], 'ro-', linewidth=1, markersize=3)
plt.plot(data[:, 0], data[:, 2], data[:, 0], data[:, 1], 'r')
plt.show()

# Для короткого промежутка анимация не показательна, для длительного очень много весит.
# Animation starts here
# plt.xlim(-6, 6)
# plt.ylim(-6, 6)
# plt.xlabel(r'$x(t)$')
# plt.ylabel(r'$y(t)$')
# plt.title(f'$Шаг dt = {dt}$')
# plt.grid()
# l, = plt.plot([], [], 'ro-', linewidth=2, markersize=8)
# metadata = dict(title='Movie', artist='Evguran')
# fps = 10
# writer = PillowWriter(fps=fps, metadata=metadata)
#
# xlist = []
# ylist = []
#
# with writer.saving(fig, 'mayatnik.gif', 100):
#     for i in range(0, len(data), int(1 / dt / fps)):
#         l.set_data([0, data[i, 1]], [0, data[i, 2]])
#
#         writer.grab_frame()

print('done')
