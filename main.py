import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import functions as f

T = 0.5   #Nm

OD = 24     #mm
ID = 22     #mm
G = 1.8      #GPa
L = 100     #mm

k = (180/np.pi)*(32*L*(1e-3))/(G*1e9*np.pi*(np.power(OD*(1e-3),4)-np.power(ID*(1e-3),4)))
deflection = k*T

shearStress = (1e-6)*T*(OD*(1e-3)/2)/(np.pi*(np.power(OD*(1e-3),4)-np.power(ID*(1e-3),4))/32)
shearStrength = 207
sf = shearStrength/shearStress


fs = 4800
cycles = 10
rpm = 100
offset1 = 0                 #degrees
offset2 = deflection        #degrees

time, s1 = f.signal(fs,cycles,rpm,offset1)
s2 = f.signal(fs,cycles,rpm,offset2)[1]

crossV = 5
tc1, Vc1 = f.V_cross(time, s1, crossV)
tc2, Vc2 = f.V_cross(time, s2, crossV)

dt = abs(tc1-tc2)
dp = dt*360*(rpm/60)
Torque = dp/k

dp_avg = np.mean(dp)
Torque_avg = np.mean(Torque)
err = abs((T-Torque_avg)/(T))*100



sigfig = 3
print(f"Shear Stress: {round(shearStress,sigfig)} MPa")
print(f"Safety Factor: {round(sf,sigfig)}")
print(f"Torsional Stiffness: {round(1/k,sigfig)} Nm/deg")
print(f"Deflection: {round(deflection,sigfig)} deg")
print("Phase Difference:", round(dp_avg,sigfig), "deg")
print(f"Torque: {T} Nm")
print(f"Measured Torque: {round(Torque_avg,sigfig)} Nm")
print(f"Error: {round(err,sigfig)} %")

printf = 0
if printf == 1:
    plt.figure(1)
    plt.grid()
    plt.plot(time*1000, s1, '.-r')
    plt.plot(time*1000, s2, '.-b')
    plt.plot(tc1*1000, Vc1, 'ok')
    plt.plot(tc2*1000, Vc2, 'ok')
    plt.xlabel("Time [ms]")
    plt.ylabel("Volts [V]")
    plt.show()