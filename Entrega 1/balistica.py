import numpy as np
from scipy.integrate import odeint
import matplotlib.pylab as plt

# Parametros
#Unidades base
cm = 0.01  # metros
inch = 2.54 * cm
g = 9.81  # m / s**2

#Coef. de arrastre
p = 1.225  # kg / m**3 (densidad del aire)
cd = 0.47
D = 8.5 * inch
r = D / 2
A = np.pi * r ** 2
CD = 0.5 * p * cd * A

#Masa
m = 15  # kg

# Funcion a integrar
# z es vector de estado

# z = [x, y, vs, vy]
# dz/dt = bala(z,t)
#           [z2            ]
#   dz/dt = [              ]   (modelo)
#           [ FD/m   -g    ]

#Vector de estado
#   z[0]  -> x
#   z[1]  -> y
#   z[2]  -> vx
#   z[3]  -> vy

def bala(z, t):
    zp = np.zeros(4)
    zp[0] = z[2]
    zp[1] = z[3]
    v = z[2:4]  # saca los ultimos dos componente
    v[0] = v[0] - V
    v2 = np.dot(v, v)
    vnorm = np.sqrt(v2)
    FD = -CD * v2 * (v / vnorm)
    zp[2] = FD[0] / m
    zp[3] = FD[1] / m - g

    return zp

# vector de tiempo
t = np.linspace(0, 30, 1001)

# Parte en el origen y tiene vx = vy = vi m/s
vi = 100 * 1000 / 3600
z0 = np.array([0, 0, vi, vi])

V = 0
sol = odeint(bala, z0, t)

V = 10
sol1 = odeint(bala, z0, t)

V = 20
sol2 = odeint(bala, z0, t)

x = [sol[:, 0], sol1[:, 0], sol2[:, 0]]
y = [sol[:, 1], sol1[:, 1], sol2[:, 1]]

fig = plt.figure(1)

plt.plot(x[0], y[0], label="V = 0 m/s")
plt.plot(x[1], y[1], label="V = 10 m/s")
plt.plot(x[2], y[2], label="V = 20 m/s")
plt.grid()
axes = plt.gca()
axes.set_xlim([0, 150])
axes.set_ylim([0, 50])
plt.xlabel("X (m)")
plt.ylabel("Y (m)")
plt.title("Trayectoria para distintos vientos")
plt.tight_layout()
plt.legend()
plt.savefig("Balistica.png", dpi=150)
