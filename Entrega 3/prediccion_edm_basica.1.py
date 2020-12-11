import numpy as np
from scipy.integrate import odeint
from datetime import datetime

# Datos
hr = 3600
km = 1000
Radio = 6371*km
Mt = 5.972e24
G = 6.67408e-11
omega = 7.2921150e-5
HG = 700 * km

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

    Fg = (-G*Mt/r**2) * -(R@(z1/r))

    zp[0:3] = z2
    zp[3:6] = R.T@(Fg - (2*(Rp@z2) + (Rpp@z1)))
    return zp


ti = "2020-07-30T22:59:42.000000"
ti = ti.split("T")
ti = "{} {}".format(ti[0], ti[1])
ti = datetime.strptime(ti, '%Y-%m-%d %H:%M:%S.%f')
tf = "2020-08-01T00:59:42.000000"
tf = tf.split("T")
tf = "{} {}".format(tf[0], tf[1])
tf = datetime.strptime(tf, '%Y-%m-%d %H:%M:%S.%f')

deltaT = (tf - ti).total_seconds()

# Condicion inicial (m)
xi = -785661.172986
yi = 5344532.568063
zi = -4578143.248846
vxi = 2465.625744
vyi = -4448.693423
vzi = -5622.185053

# Condicion final
xf = 1007336.497837
yf = 5953847.886559
zf = 3680449.942054
vxf = 2311.933502
vyf = 3526.433923
vzf = -6317.196255

# vector de tiempo
t = np.linspace(0, deltaT, 9361)

# Condiciones iniciales
z0 = np.array([xi, yi, zi, vxi, vyi, vzi])
sol = odeint(satelite, z0, t)

diff_zf = np.array([xf, yf, zf, vxf, vyf, vzf]) - sol[-1]

H = np.sqrt(diff_zf[0]**2+diff_zf[1]**2+diff_zf[2]**2)

print(f"{H} metros")
