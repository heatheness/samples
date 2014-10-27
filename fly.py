# -*- coding: utf-8 -*-

__author__ = 'dmitrymakhotin'



import math
import matplotlib.pyplot as plt
import numpy as np

g = 9.81
start_velocity = 80.0
mass = 1.0
alpha = 40.0
friction_coefficient = 0.4
delta_t = 0.01


def analitic_solving(start_velocity, mass, alpha, friction_coefficient, delta_t):
    """
    Аналитическое решение для задачи полета тела, брошенного под углом к горизонту, с учетом трения.
    Возвращает лист всех координат тела в полете и максимальную высоту в формате:
    [[координаты по x], [координаты по y]]
    Величины обезразмерены
    """
    alpha = math.radians(alpha)
    mu = friction_coefficient/mass
    xlist = np.array([0.0],dtype=float)
    ylist = np.array([0.0], dtype=float)
    max_high = start_velocity**2 * math.sin(alpha)**2 / (2*g) # для обезразмеривания
    print(max_high)
    t = delta_t
    y = 0
    while y >= 0:
        x = (start_velocity * math.cos(alpha)/mu) * (1 - math.exp(-1*mu*t)) / max_high
        y = (((mu*start_velocity*math.sin(alpha) + g)/(mu**2)) * (1-math.exp(-1*mu*t)) - (g*t)/mu) /max_high
        t += delta_t
        xlist = np.append(xlist,x)
        ylist = np.append(ylist,y)

    solution = []
    solution.append(xlist)
    solution.append(ylist)
    return solution

def runge_kutta (start_velocity, mass, alpha, friction_coefficient, delta_t):
    """
    метод Рунге - Кутта
    """

    def function(v_0, mu, alpha, vx, vy):
        sinus_alpha = math.sin(alpha)
        dvx_dt = (-mu*v_0*sinus_alpha/g)*vx
        dvy_dt = -sinus_alpha*((mu*v_0*vy/g)+1)
        dx_dt = 2*vx/sinus_alpha
        dy_dt = 2*vy/sinus_alpha
        return (dvx_dt, dvy_dt, dx_dt, dy_dt)


    alpha = math.radians(alpha)
    mu = friction_coefficient/mass
    xlist = np.array([0.0],dtype=float)
    ylist = np.array([0.0], dtype=float)
    vx_current = math.cos(alpha)
    vy_current = math.sin(alpha)
    y = 0
    h = delta_t/6.0 # 1/6 шага


    while y>=0:
        k1_vx, k1_vy, k1_x, k1_y = function(start_velocity, mu, alpha, vx_current, vy_current)
        k2_vx, k2_vy, k2_x, k2_y = function(start_velocity, mu, alpha, vx_current + k1_vx/2.0*delta_t,
                                      vy_current + k1_vy/2.0*delta_t)
        k3_vx, k3_vy, k3_x, k3_y = function(start_velocity, mu, alpha, vx_current + k2_vx/2.0*delta_t,
                                      vy_current + k2_vy/2.0*delta_t)
        k4_vx, k4_vy, k4_x, k4_y = function(start_velocity, mu, alpha, vx_current + k3_vx*delta_t,
                                      vy_current + k3_vy*delta_t)
        vx_current = vx_current + h*(k1_vx + 2*k2_vx + 2*k3_vx + k4_vx)
        vy_current = vy_current + h*(k1_vy + 2*k2_vy + 2*k3_vy + k4_vy)
        x = xlist[-1] + h*(k1_x + 2*k2_x + 2*k3_x + k4_x)
        y = ylist[-1] + h*(k1_y + 2*k2_y + 2*k3_y + k4_y)
        xlist = np.append(xlist,x)
        ylist = np.append(ylist,y)

    solution = []
    solution.append(xlist)
    solution.append(ylist)
    return solution

analitic_solution = analitic_solving (start_velocity, mass, alpha, friction_coefficient, delta_t)
analitic_xlist = analitic_solution[0]
analitic_ylist = analitic_solution[1]

rc_solution = runge_kutta(start_velocity, mass, alpha, friction_coefficient, delta_t)
rc_xlist = rc_solution[0]
rc_ylist = rc_solution[1]

print (u'Max high analitic: \t', max(analitic_ylist))
print (u'Max high Runge-Kutta: \t ', max(rc_ylist))

print (u'Max distance analitic: \t', analitic_xlist[-2])
print (u'Max distance Runge-Kutta: \t', rc_xlist[-2])

plt.grid()
plt.xlabel(u'Дальность')
plt.ylabel(u'Высота')
plt.title(u'Полет тела, брошенного под углом к горизонту')
line_1 = plt.plot (analitic_xlist[analitic_ylist[:] >= 0], analitic_ylist[analitic_ylist[:] >= 0], 'b-',
                                  label = u"Аналитическое решение", linewidth = 2)
line_2 = plt.plot (rc_xlist[rc_ylist[:] >= 0], rc_ylist[rc_ylist[:] >= 0], 'y--',
                                  label = u"Рунге - Кутта", linewidth = 2)
plt.legend (loc = 'best')
plt.show()





