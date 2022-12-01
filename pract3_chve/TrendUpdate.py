import time
import rrdtool
from getSNMP import consultaSNMP
rrdpath = '/home/chve117/Documentos/pract3-20221130T151730Z-001/pract3/RRD'
carga_CPU = 0
carga_cpu2 = 0
ram_total = 0
memory_ram = 0
disk_total = 0
disk = 0
chargeCPU = 0
ramPorcent = 0
diskPorcent = 0


while 1:
    carga_CPU = int(consultaSNMP('ernesto','localhost','1.3.6.1.2.1.25.3.3.1.2.196608'))
    """carga_cpu2 = int(consultaSNMP('ernesto','localhost','1.3.6.1.2.1.25.3.3.1.2.196609'))"""
    disk_total = 4096*int(consultaSNMP('ernesto','localhost','1.3.6.1.2.1.25.2.3.1.5.1'))
    disk = 4096*int(consultaSNMP('ernesto','localhost','1.3.6.1.2.1.25.2.3.1.6.1'))
    ram_total = 65536*int(consultaSNMP('ernesto','localhost','1.3.6.1.2.1.25.2.3.1.5.3'))
    memory_ram = 65536*int(consultaSNMP('ernesto','localhost','1.3.6.1.2.1.25.2.3.1.6.3'))
    
    chargeCPU = (carga_CPU + carga_cpu2)/2
    ramPorcent = (memory_ram * 100)/ram_total
    diskPorcent =(disk * 100)/disk_total
    ramPorcent = round(ramPorcent,2)
    diskPorcent = round(diskPorcent,2)
    
    valor = "N:" + str(chargeCPU) + ":" + str(ramPorcent) + ":" + str(diskPorcent) 
    print (valor)
    rrdtool.update(rrdpath+'/trend.rrd', valor)
    time.sleep(5)

if ret:
    print (rrdtool.error())
    time.sleep(300)
