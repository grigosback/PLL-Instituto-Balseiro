import visa
import numpy as np
from time import sleep
import matplotlib.pyplot as plt
rm = visa.ResourceManager()
print(rm.list_resources())
psupply = rm.open_resource('ASRL3::INSTR')
osciloscopio=rm.open_resource('USB0::0x1AB1::0x04B0::DS2D163351641::INSTR')
volt=rm.open_resource('USB0::0x0957::0x0607::MY53010703::INSTR')
volt.write("CONF:VOLT:DC")
print("El oscilocopio se identifica como"+osciloscopio.query("*IDN?")+"\n")
print("El multimetro se identifica como"+volt.query("*IDN?")+"\n")
N=100
V=np.zeros(N)
F=np.zeros(N)
name="VCO-B-15V-PLL-200k"
path=name+".csv"
output = open(path, 'w')
psupply.write("o1")
vi=0.5
vf=15

for i in range (0,N):
    v=vi+i*(vf-vi)/N
    sufix=str(int(v*100)).zfill(4)
    psupply.write("su"+sufix)
    osciloscopio.write(":AUT")
    sleep(4)
    V[i]=volt.query("READ?")
    F[i]=osciloscopio.query(":MEAS:FREQ? 1")
    output.write(("%f,%f\n" % (V[i], F[i])))
psupply.write("o0")
fig=plt.figure()
plt.plot(V,F,'bo')
plt.show()
fig.savefig(name+".png")