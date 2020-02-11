import os
outputCMD = os.popen('ls /dev/ttyU*').read()
devices = outputCMD.split("\n")
devices.remove('')

import serial
seriales = []
sensores = []
f = open("GAS.txt", "a")
for i in range(len(devices)):
    seriales.append(serial.Serial(devices[i]))
    seriales[i].write(b'e')
    for j in range(20):
        if j == 17:
            sensores.append(seriales[i].readline().decode("utf-8").split("= ")[1].rstrip('\r\n'))
        else:
            seriales[i].readline()
    print("Sensor "+str(i)+": "+sensores[i]+".")
    f.write(sensores[i]+"\t")
f.write("T (C)")

import time
running = True
cero = False
unaHora = 60*60
end = unaHora*3
start = time.time()
while running:
    try:
        f.write("\n")
        print("Iniciando bloque...")
        temp = 0.0
        for ser in seriales:
            ser.write(b'\r')
            reading = ser.readline()
            output = reading.decode("utf-8").rstrip('\r\n').split(',')
            rpt = float(output[1])/1000.0
            temp += float(output[2])
            
            if rpt < 0:
                if rpt >= -2:
                    rpt = 0.0
                else:
                    rpt = -1
            print(ser.name)       
            f.write(str(rpt)+"\t")
        f.write(str(temp/len(devices)))
        print(output[-3]+":"+output[-2]+":"+output[-1]+" Done...")
        
        if time.time() - start > unaHora and cero == False:
            for ser in seriales:
                ser.write(b'Z')
                ser.readline()
                ser.readline()
                print("Seteando a cero "+ser.name)
            cero = True
            f.write("Seteando a cero todos los sensores")
            print("Done...")
        
        # if time.time() - start > end:
        #     running = False 
    except KeyboardInterrupt:
        f.close()

if running == False:
    f.close()
    print("Tu tiempo se termino.")