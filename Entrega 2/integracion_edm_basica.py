import numpy as np
from scipy.integrate import odeint
import matplotlib.pylab as plt


#Datos
theta = (7.27 * 10**-5) * 3600
G = (6.673 * 10**-11) * (3600**2) * (1000**-3)
mt = 5.972 * 10**24
rt = 6371
r = (rt+ 700)


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
 # z = [x, y, z, vx, vy, vz]
def satelite(z,t):
    zp = np.zeros(6)
    zp[0:3] = z[3:6]
    zp[3:6] = -(G * mt / r**3) * z[0:3] - Rt(t) @ ((Rpp(t) @ z[0:3]) + 2 * (Rp(t) @ z[3:6]))
    return zp

# vector de tiempo
t = np.linspace(0,3.528,1001)
angulo = np.linspace(0,2*np.pi,1001)

# condiciones iniciales
vt = 25175 #km/h

z0 = np.array([r, 0, 0, 0, vt, 0])

sol = odeint(satelite, z0, t)

x = sol[:,0]
y = sol[:,1]
z = sol[:, 2]

plt.figure()

plt.subplot(3,1,1)
plt.plot(t,x, color = "green", label = "x(t)")
plt.ylabel("x(t)")
plt.legend()
plt.subplot(3,1,2)
plt.plot(t,y,color = "lightblue", label = "y(t)")
plt.ylabel("y(t)")
plt.legend()
plt.subplot(3,1,3)
plt.plot(t,z, color = "brown", label = "z(t)")
plt.xlabel("t")
plt.ylabel("z(t)")
plt.legend()
plt.savefig("graficos.png")
plt.show()



plt.plot(x, y, "--", color = "green", label = "Satelite")
xt = rt*np.sin(angulo)
yt = rt*np.cos(angulo)
plt.plot(xt,yt, color = "brown", label = "Tierra")
xa = (rt+80)*np.sin(angulo)
ya = (rt+80)*np.cos(angulo)
plt.plot(xa,ya, color = "lightblue", label = "Atmosfera")
plt.xlabel("t")
plt.ylabel("r(t)")
plt.grid()
plt.tight_layout()
plt.legend()
plt.savefig(f"orbitas{vt}.png")
plt.show()

plt.plot(x, y, "--", color = "green", label = "Satelite")
xt = rt*np.sin(angulo)
yt = rt*np.cos(angulo)
plt.plot(xt,yt, color = "brown", label = "Tierra")
xa = (rt+80)*np.sin(angulo)
ya = (rt+80)*np.cos(angulo)
plt.plot(xa,ya, color = "lightblue", label = "Atmosfera")
plt.xlabel("t")
plt.ylabel("r(t)")
plt.grid()
plt.tight_layout()
plt.legend()
plt.xlim(7100,5000)
plt.ylim(-7100,7100)
plt.savefig(f"orbitaszoom{vt}.png")
plt.show()