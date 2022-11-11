import time
import rrdtool
from getSNMP import consultaSNMP
while 1:
    paquetes_unicast = int(consultaSNMP('ernesto','localhost','1.3.6.1.2.1.2.2.1.11.2'))
	
    paquetes_ipv4 = int(consultaSNMP('ernesto','localhost','1.3.6.1.2.1.4.3.0'))
    
    mensajes_icmp = int(consultaSNMP('ernesto','localhost','1.3.6.1.2.1.5.8.0'))
    
    segmentos_entrada = int(consultaSNMP('ernesto','localhost','1.3.6.1.2.1.6.10.0'))
    
    datagramas_udp = int(consultaSNMP('ernesto','localhost','1.3.6.1.2.1.7.1.0'))
	
    
    valor = "N:" + str(paquetes_unicast) + ':' + str(paquetes_ipv4) + ':' + str(mensajes_icmp) + ':' + str(segmentos_entrada) + ':' + str(datagramas_udp)
    print (valor)
    rrdtool.update('segmentosRed.rrd', valor)
    rrdtool.dump('segmentosRed.rrd','traficoRED.xml')
    time.sleep(1)

if ret:
    print (rrdtool.error())
    time.sleep(300)
