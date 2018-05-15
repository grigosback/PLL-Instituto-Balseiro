import visa
import numpy as np
from time import sleep
import matplotlib.pyplot as plt

rm = visa.ResourceManager()
print(rm.list_resources())
gen=rm.open_resource('USB0::0x1AB1::0x0641::DG4E163251558::INSTR')
osciloscopio=rm.open_resource('USB0::0x1AB1::0x04B0::DS2D163351641::INSTR')

print("El oscilocopio se identifica como"+osciloscopio.query("*IDN?")+"\n")
print("El multimetro se identifica como"+gen.query("*IDN?")+"\n")

wavename="SQU"
N=100
fin=np.zeros(N)
fout=np.zeros(N)
name="PLL-B-COMP1-"+wavename+"-"
path=(name+".csv")
output = open(path, 'w')

fi=17700
ff=17600

gen.write(":SOUR1:APPL:"+wavename+" "+str(fi)+",10,0,0")
gen.write(":OUTPUT1 ON")

for i in range (0,N):
    f=int(fi+i*(ff-fi)/N)
    gen.write(":SOUR1:FREQ "+str(f))
    osciloscopio.write(":AUT")
    sleep(4)
    fout[i]=osciloscopio.query(":MEAS:FREQ? CHAN1")
    fin[i]=f

    output.write(("%f,%f\n" % (fin[i], fout[i])))

gen.write(":OUTPUT1 OFF")
gen.write(":OUTPUT2 OFF")
fig=plt.figure()
plt.plot(fin,fout,'bo')
plt.show()
fig.savefig(name+".png")