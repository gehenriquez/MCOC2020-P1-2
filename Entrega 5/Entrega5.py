import numpy as np
from scipy.integrate import odeint
from datetime import datetime
from leer_eof import leer_eof
from time import perf_counter
import matplotlib.pyplot as plt

t0 = perf_counter()

# Datos
hr = 3600
km = 1000
Radio = 6371*km
Mt = 5.972e24
G = 6.67408e-11
omega = -7.2921150e-5
HG = 700 * km
J2 = 1.75553e10 * (1000 ** 5)  # km5⋅s−2
J3 = -2.61913e11 * (1000 ** 6)  # km6⋅s−2

FgMax = G*Mt/Radio**2

zp = np.zeros(6)


def satelite(z, t):
    c = np.cos(omega * t)
    s = np.sin(omega * t)
    R = np.array([[c, s, 0], [-s, c, 0], [0, 0, 1]])
    Rp = omega * (np.array([[-s, c, 0], [-c, -s, 0], [0, 0, 0]]))
    Rpp = (omega ** 2) * (np.array([[-c, -s, 0], [s, -c, 0], [0, 0, 0]]))

    z1 = z[0:3]
    z2 = z[3:6]

    r2 = np.dot(z1, z1)
    r = np.sqrt(r2)

    Fg = (-G*Mt/r**2) * (R@(z1/r))

    zp[0:3] = z2
    zp[3:6] = R.T@(Fg - (2*(Rp@z2) + (Rpp@z1)))
    return zp


def eulerint(zp, z0, t, Nsubdivisiones):
    Nt = len(t)
    Ndim = len(z0)

    z = np.zeros((Nt, Ndim))
    z[0, :] = z0

    for i in range(1, Nt):
        t_anterior = t[i-1]
        dt = (t[i] - t[i-1])/Nsubdivisiones
        z_temp = z[i-1, :].copy()
        for k in range(Nsubdivisiones):
            z_temp += dt*zp(z_temp, t_anterior + k*dt)
        z[i, :] = z_temp
    return z


fname = "S1A_OPER_AUX_POEORB_OPOD_20200820T121229_V20200730T225942_20200801T005942.EOF"

t, x, y, z, vx, vy, vz = leer_eof(fname)

sol_real = []
for i in range(len(t)):
    sol_real.append([x[i], y[i], z[i], vx[i], vy[i], vz[i]])

np.array(sol_real)

# Condicion inicial (m)
xi = x[0]
yi = y[0]
zi = z[0]
vxi = vx[0]
vyi = vy[0]
vzi = vz[0]

# Condicion final
xf = x[-1]
yf = y[-1]
zf = z[-1]
vxf = vx[-1]
vyf = vy[-1]
vzf = vz[-1]

z0 = np.array([xi, yi, zi, vxi, vyi, vzi])
zf = np.array([xf, yf, zf, vxf, vyf, vzf])

t1 = perf_counter()
sol_odeint = odeint(satelite, z0, t)
t2 = perf_counter()
sol_eulerint = eulerint(satelite, z0, t, 1)
t3 = perf_counter()

# --Pregunta 1--#
plt.figure()
plt.subplot(3, 1, 1)
plt.title("Posición Real vs Odeint")
plt.plot(t, x, color="b", label="Real")
plt.plot(t, sol_odeint[:, 0], color="orange", label="Odeint")
plt.ylabel("x(t)")
plt.legend()
plt.subplot(3,1,2)
plt.plot(t, y, color="b", label="Real")
plt.plot(t, sol_odeint[:, 1], color="orange", label="Odeint")
plt.ylabel("y(t)")
plt.legend()
plt.subplot(3, 1, 3)
plt.plot(t, z, color="b", label="Real")
plt.plot(t, sol_odeint[:, 2], color="orange", label="Odeint")
plt.xlabel("t")
plt.ylabel("z(t)")
plt.legend()
plt.savefig("P1-grafico_posición(x,y,z)-RealvsOdeint.png")
plt.show()  # sacar para entrega?

plt.figure()
plt.subplot(3, 1, 1)
plt.title("Posicion Real")
plt.plot(t, x, color="b", label="Real")
plt.ylabel("x(t)")
plt.subplot(3,1,2)
plt.plot(t, y, color="b", label="Real")
plt.ylabel("y(t)")
plt.subplot(3, 1, 3)
plt.plot(t, z, color="b", label="Real")
plt.xlabel("t")
plt.ylabel("z(t)")
plt.savefig("P1-grafico_posición(x,y,z)-Real.png")
plt.show()  # sacar para entrega?

# ---Pregunta 2---#
tiempo_odeint = t2-t1
tiempo_euler = t3-t2

# ---Eulerint vs Odeint---#
deriva = []

for i in range(len(t)):
    difx = sol_odeint[i][0] - sol_eulerint[i][0]
    dify = sol_odeint[i][1] - sol_eulerint[i][1]
    difz = sol_odeint[i][2] - sol_eulerint[i][2]
    deriva.append(np.sqrt(np.dot(difx, difx) + np.dot(dify, dify) + np.dot(difz, difz)))

tx = t / 3600.

plt.figure()
plt.title(f"Diferencia Eulerint vs Odeint dmax = {round(max(deriva)/1000, 2)} KM")
plt.xlabel("Tiempo")
plt.ylabel("Deriva")
plt.plot(tx, np.array(deriva) / 1000)
plt.savefig("P2-EulerintvsOdeint.png")
plt.show()

# ---Real vs Eulerint---#
deriva1 = []

for i in range(len(t)):
    difx = sol_real[i][0] - sol_eulerint[i][0]
    dify = sol_real[i][1] - sol_eulerint[i][1]
    difz = sol_real[i][2] - sol_eulerint[i][2]
    deriva1.append(np.sqrt(np.dot(difx, difx) + np.dot(dify, dify) + np.dot(difz, difz)))

plt.figure()
plt.title(f"Diferencia Real vs Eulerint dmax = {round(max(deriva1)/1000, 2)} KM")
plt.xlabel("Tiempo")
plt.ylabel("Deriva")
plt.plot(tx, np.array(deriva1) / 1000)
plt.savefig("P2-RealvsEulerint.png")
plt.show()

# ---Real vs Odeint---#
deriva2 = []

for i in range(len(t)):
    difx = sol_real[i][0] - sol_odeint[i][0]
    dify = sol_real[i][1] - sol_odeint[i][1]
    difz = sol_real[i][2] - sol_odeint[i][2]
    deriva2.append(np.sqrt(np.dot(difx, difx) + np.dot(dify, dify) + np.dot(difz, difz)))


plt.figure()
plt.title(f"Diferencia Real vs Odeint dmax = {round(max(deriva2)/1000, 2)} KM")
plt.xlabel("Tiempo")
plt.ylabel("Deriva")
plt.plot(tx, np.array(deriva2) / 1000)
plt.savefig("P2-RealvsOdeint.png")
plt.show()

print(f"La solucion de eulerint demora {tiempo_euler} segundos")
print(f"La solucion de odeint demora {tiempo_odeint} segundos")
print(f"La solucion de odeint difiere en {round((deriva[-1])/1000, 2)}  KM de la solucion eulerint al final del tiempo")
"""
# --- Pregunta 3 --- #
N=10000
error=100
while(error>=1):
    N+=1
    print(N)
    t_eu0 = perf_counter()
    sol_eulerint1 = eulerint(satelite, z0, t, N)
    t_eu1 = perf_counter()
    deriva3=[]
    for i in range(len(t)):
        difx = sol_real[i][0] - sol_eulerint1[i][0]
        dify = sol_real[i][1] - sol_eulerint1[i][1]
        difz = sol_real[i][2] - sol_eulerint1[i][2]
        deriva3.append(np.sqrt(np.dot(difx, difx)+np.dot(dify, dify)+np.dot(difz, difz)))
    errorx = (abs(difx)/sol_real[-1][0]) * 100
    errory = (abs(dify)/sol_real[-1][1]) * 100
    errorz = (abs(difz)/sol_real[-1][2]) * 100
    error = (errorx + errory + errorz)/3

print(f"Eulerint con {N} subdivisiones presenta un error de {error} < al 1%")

plt.figure()
plt.title(f"Diferencia Real vs Eulerint con {N} subdivisiones dmax = {round(max(deriva3)/1000, 2)} KM")
plt.xlabel("Tiempo")
plt.ylabel("Deriva")
plt.plot(tx, np.array(deriva3) / 1000)
plt.savefig("P3.png")
plt.show()
"""

# --- Pregunta 4 --- #

def satelite_J2_J3(z, t):
    c = np.cos(omega * t)
    s = np.sin(omega * t)

    R = np.array([[c, s, 0], [-s, c, 0], [0, 0, 1]])

    Rp = omega * (np.array([[-s, c, 0], [-c, -s, 0], [0, 0, 0]]))

    Rpp = (omega ** 2) * (np.array([[-c, -s, 0], [s, -c, 0], [0, 0, 0]]))

    z1 = z[0:3]
    z2 = z[3:6]

    r2 = np.dot(z1, z1)
    r = np.sqrt(r2)

    FJ2 = np.zeros(3)
    FJ2[0] = (J2 * z[0] / (r ** 7)) * (6 * z[2] ** 2 - (3 / 2) * (z[0] ** 2 + z[1] ** 2))
    FJ2[1] = (J2 * z[1] / (r ** 7)) * (6 * z[2] ** 2 - (3 / 2) * (z[0] ** 2 + z[1] ** 2))
    FJ2[2] = (J2 * z[2] / (r ** 7)) * (3 * z[2] ** 2 - (9 / 2) * (z[0] ** 2 + z[1] ** 2))

    FJ3 = np.zeros(3)
    FJ3[0] = (J3 * z[0] * z[2] / (r ** 9)) * (10 * z[2] ** 2 - (15 / 2) * (z[0] ** 2 + z[1] ** 2))
    FJ3[1] = (J3 * z[1] * z[2] / (r ** 9)) * (10 * z[2] ** 2 - (15 / 2) * (z[0] ** 2 + z[1] ** 2))
    FJ3[2] = (J3 / (r ** 9)) * (4 * z[2] ** 2 * (z[2] ** 2 - 3 * (z[0] ** 2 + z[1] ** 2) + (3 / 2) * (z[0] ** 2 + z[1] ** 2) ** 2))

    zp[0:3] = z2
    Fg = (-G * Mt / r ** 2) * (R @ (z1 / r))
    zp[3:6] = R.T @ (Fg - (2 * Rp @ z2) + (Rpp @ z1)) + FJ2 + FJ3

    return zp

p4_t1 = perf_counter()
p4_sol_odeint = odeint(satelite_J2_J3, z0, t)
p4_t2 = perf_counter()
p4_sol_eulerint = eulerint(satelite_J2_J3, z0, t, 1)
p4_t3 = perf_counter()

# --Pregunta 4 - parte 1--#
plt.figure()
plt.subplot(3, 1, 1)
plt.title("Posición Real vs Odeint_J2_J3")
plt.plot(t, x, color="b", label="Real")
plt.plot(t, p4_sol_odeint[:, 0], color="orange", label="Odeint_J2_J3")
plt.ylabel("x(t)")
plt.legend()
plt.subplot(3,1,2)
plt.plot(t, y, color="b", label="Real")
plt.plot(t, p4_sol_odeint[:, 1], color="orange", label="Odeint_J2_J3")
plt.ylabel("y(t)")
plt.legend()
plt.subplot(3, 1, 3)
plt.plot(t, z, color="b", label="Real")
plt.plot(t, p4_sol_odeint[:, 2], color="orange", label="Odeint_J2_J3")
plt.xlabel("t")
plt.ylabel("z(t)")
plt.legend()
plt.savefig("P4-grafico_posición(x,y,z)-RealvsOdeint_J2_J3.png")
plt.show()  # sacar para entrega?

plt.figure()
plt.subplot(3, 1, 1)
plt.title("Posicion Real")
plt.plot(t, x, color="b", label="Real")
plt.ylabel("x(t)")
plt.subplot(3,1,2)
plt.plot(t, y, color="b", label="Real")
plt.ylabel("y(t)")
plt.subplot(3, 1, 3)
plt.plot(t, z, color="b", label="Real")
plt.xlabel("t")
plt.ylabel("z(t)")
plt.savefig("P4-grafico_posición(x,y,z)-Real.png")
plt.show()  # sacar para entrega?

# ---Pregunta 4 - parte 2 ---#
p4_tiempo_odeint = p4_t2-p4_t1
p4_tiempo_euler = p4_t3-p4_t2

# ---Eulerint vs Odeint_J2_J3---#
p4_deriva = []

for i in range(len(t)):
    difx = p4_sol_odeint[i][0] - p4_sol_eulerint[i][0]
    dify = p4_sol_odeint[i][1] - p4_sol_eulerint[i][1]
    difz = p4_sol_odeint[i][2] - p4_sol_eulerint[i][2]
    p4_deriva.append(np.sqrt(np.dot(difx, difx) + np.dot(dify, dify) + np.dot(difz, difz)))

tx = t / 3600.

plt.figure()
plt.title(f"Diferencia Eulerint vs Odeint_J2_J3 dmax = {round(max(p4_deriva)/1000, 2)} KM")
plt.xlabel("Tiempo")
plt.ylabel("Deriva")
plt.plot(tx, np.array(p4_deriva) / 1000)
plt.savefig("P4-EulerintvsOdeint_J2_J3.png")
plt.show()

# ---Real vs Eulerint_J2_J3---#
p4_deriva1 = []

for i in range(len(t)):
    difx = sol_real[i][0] - p4_sol_eulerint[i][0]
    dify = sol_real[i][1] - p4_sol_eulerint[i][1]
    difz = sol_real[i][2] - p4_sol_eulerint[i][2]
    p4_deriva1.append(np.sqrt(np.dot(difx, difx) + np.dot(dify, dify) + np.dot(difz, difz)))

plt.figure()
plt.title(f"Diferencia Real vs Eulerint_J2_J3 dmax = {round(max(p4_deriva1)/1000, 2)} KM")
plt.xlabel("Tiempo")
plt.ylabel("Deriva")
plt.plot(tx, np.array(p4_deriva1) / 1000)
plt.savefig("P4-RealvsEulerint_J2_J3.png")
plt.show()

# ---Real vs Odeint_J2_J3---#
p4_deriva2 = []

for i in range(len(t)):
    difx = sol_real[i][0] - p4_sol_odeint[i][0]
    dify = sol_real[i][1] - p4_sol_odeint[i][1]
    difz = sol_real[i][2] - p4_sol_odeint[i][2]
    p4_deriva2.append(np.sqrt(np.dot(difx, difx) + np.dot(dify, dify) + np.dot(difz, difz)))


plt.figure()
plt.title(f"Diferencia Real vs Odeint_J2_J3 dmax = {round(max(p4_deriva2)/1000, 2)} KM")
plt.xlabel("Tiempo")
plt.ylabel("Deriva")
plt.plot(tx, np.array(p4_deriva2) / 1000)
plt.savefig("P4-RealvsOdeint_J2_J3.png")
plt.show()

p4_tf = perf_counter()
print(f"La solucion de eulerint_J2_J3 demora {p4_tiempo_euler} segundos")
print(f"La solucion de odeint_J2_J3 demora {p4_tiempo_odeint} segundos")
print(f"La solucion de odeint_J2_J3 difiere en {round((p4_deriva[-1])/1000, 2)}  KM de la solucion eulerint al final del tiempo")


print(f"La Parte 4 demora {p4_tf-p4_t1} segundos en correr")
print(f"Todo el archivo demora {p4_tf-t0} segundos en correr (sin la parte 3)")










