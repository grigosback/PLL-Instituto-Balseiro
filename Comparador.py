import visa
import numpy as np
from time import sleep
import matplotlib.pyplot as plt

rm = visa.ResourceManager()
print(rm.list_resources())
gen=rm.open_resource('USB0::0x1AB1::0x0641::DG4E163251558::INSTR')
osciloscopio=rm.open_resource('USB0::0x1AB1::0x04B0::DS2D163351641::INSTR')
volt=rm.open_resource('USB0::0x0957::0x0607::MY53010703::INSTR')
volt.write("CONF:VOLT:DC")
print("El oscilocopio se identifica como"+osciloscopio.query("*IDN?")+"\n")
print("El multimetro se identifica como"+gen.query("*IDN?")+"\n")
print("El multimetro se identifica como"+volt.query("*IDN?")+"\n")

wavename="SIN"
N=100
Phi=np.zeros(N)
V=np.zeros(N)
name="comparador2-b-"+wavename+"-5"
path=(name+".csv")
output = open(path, 'w')

phii=90
phif=270

gen.write(":SOUR1:APPL:"+wavename+" 10000,10,0,0")
gen.write(":SOUR2:APPL:"+wavename+" 10000,10,0,0")
gen.write(":OUTPUT1 ON")
gen.write(":OUTPUT2 ON")
gen.write(":SOUR1:PHAS:INIT")

for i in range (0,N):
    phi=int(phii+i*(phif-phii)/N)
    gen.write(":SOUR1:PHAS "+str(phi))
    osciloscopio.write(":AUT")
    sleep(4)
    V[i]=volt.query("READ?")
    phiosc=osciloscopio.query(":MEAS:FPH?")
    if(float(phiosc)<0):
        phiosc=str(float(phiosc)+360)
    Phi[i]=phiosc
    output.write(("%f,%f\n" % (Phi[i], V[i])))

gen.write(":OUTPUT1 OFF")
gen.write(":OUTPUT2 OFF")
fig=plt.figure()
plt.plot(Phi,V,'bo')
plt.show()
fig.savefig(name+".png")