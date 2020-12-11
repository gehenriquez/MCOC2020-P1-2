import numpy as np
from scipy.integrate import odeint
from datetime import datetime


 # Datos
theta = (7.27* 10**-5)
G = (6.67*10**-11)*(3600**2)*(1000**-3)
mt = 5.972*10**24
r = (6371+700)*1000
rt = 6371*1000

def R(t):
    r0= np.array([[np.cos(theta*t),-np.sin(theta*t), 0],[np.sin(theta*t),np.cos(theta*t), 0],[0, 0, 1]])
    return r0

def Rt(t):
    rt = np.array([[np.cos(theta*t),np.sin(theta*t), 0],[-np.sin(theta*t),np.cos(theta*t), 0],[0, 0, 0]])
    return rt

def Rp(t):
    rp = theta * (np.array([[-np.sin(theta*t),-np.cos(theta*t), 0],[np.cos(theta*t),-np.sin(theta*t), 0],[0, 0, 0]]))
    return rp

def Rpp(t):
    rpp = (theta**2) * (np.array([[-np.cos(theta*t),np.sin(theta*t), 0],[-np.sin(theta*t),-np.cos(theta*t), 0],[0, 0, 0]]))
    return rpp

 # Funcion a integrar
 # z es el vector de estado
 # z = [x, y, vx, vy]

def satelite(z,t):
    zp = np.zeros(6)
    zp[0:3] = z[3:6]
    zp[3:6] = -(G * mt / r**3) * z[0:3] - Rt(t) @ ((Rpp(t) @ z[0:3]) + 2 * (Rp(t) @ z[3:6]))
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