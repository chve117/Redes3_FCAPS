from reportlab.platypus import (SimpleDocTemplate, PageBreak, Image, Spacer,
Paragraph, Table,)
from pysnmp.hlapi import *
from reportlab.pdfgen import canvas
from datetime import datetime
import time
import rrdtool


def consultaSNMP(comunidad,host,oid, puerto):
    errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(SnmpEngine(),
               CommunityData(comunidad),
               UdpTransportTarget((host, int(puerto))),
               ContextData(),
               ObjectType(ObjectIdentity(oid))))

    if errorIndication:
        print(errorIndication)
    elif errorStatus:
        print('%s at %s' % (errorStatus.prettyPrint(),errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
    else:
        for varBind in varBinds:
            varB=(' = '.join([x.prettyPrint() for x in varBind]))
            resultado= varB.split("=")[1]
    return resultado


def agregarAgente():
    print()
    comunidad = input("Comunidad: ")
    version = input("Version: ")
    puerto = input("Puerto: ")
    ip = input("IP: ")

    with open("Agente.txt", "a") as file:
        file.write(comunidad + " " + version + " " + puerto + " " + ip + "\n")


def modificar():
    print()
    i = 1
    print("Dispositivos: ")
    with open("Agente.txt", "r") as file:
        datos = file.readlines()

    with open("Agente.txt", "r") as file:
        for line in file:
            print(str(i) + "\t" + line)
            i = i + 1

    borrar = int(input("Dispositivo a modificar: "))
    i = 1
    print()
    comunidad = input("Comunidad: ")
    version = input("Version: ")
    puerto = input("Puerto: ")
    ip = input("IP: ")
    print()

    with open("Agente.txt", "w") as file:
        for line in datos:
            if i != borrar:
                file.write(line)
            else:
                file.write(comunidad + " " + version + " " + puerto + " " + ip + "\n")
            i = i + 1



def delete():
    print()
    i = 1
    
    with open("Agente.txt", "r") as file:
        datos = file.readlines()
    print("Dispositivos: ")
    with open("Agente.txt", "r") as file:
        for line in file:
            print(str(i) + "\t" + line)
            i = i + 1
    
    borrar = int(input("Dispositivo a borrar: "))
    i = 1
    with open("Agente.txt", "w") as file:
        for line in datos:
            if i != borrar:
                file.write(line)
            i = i + 1

def generarReporte():
    print()
    
    with open("Agentes.txt", "r") as file:
        devices = file.readlines()

    i = 1
    print("Dispositivos: ")
    with open("Agentes.txt", "r") as file:
        for line in file:
            print(str(i) + "\t" + line)
            i = i + 1
    numero = 0
    datos = devices[numero].split()

    comunidad = datos[0]
    version = datos[1]
    puerto = datos[2]
    ip = datos[3]

    datosSNMP = consultaSNMP(comunidad, ip, "1.3.6.1.2.1.1.1.0", puerto)
    os = "hola"
    if datosSNMP.find("Linux") == 1:
        os = datosSNMP.split()[0]
    else:
        os = datosSNMP.split()[12]
    
    name = consultaSNMP(comunidad, ip, "1.3.6.1.2.1.1.5.0", puerto)
    contact = consultaSNMP(comunidad, ip, "1.3.6.1.2.1.1.4.0", puerto)
    ubi = consultaSNMP(comunidad, ip, "1.3.6.1.2.1.1.6.0", puerto)
    numInter = consultaSNMP(comunidad, ip, "1.3.6.1.2.1.2.1.0", puerto)


    i = 1
    interfaces = []
    while i <= 6:
        interfaz = consultaSNMP(comunidad, ip, "1.3.6.1.2.1.2.2.1.7." + str(i), puerto)
        interfaces.append(interfaz)
        i = i + 1
    
    timestr = time.strftime("%Y%m%d-%H%M%S")
    
    
    output = canvas.Canvas("reporteAgente" + timestr + ".pdf")
    output.setTitle("SNMPReport")
    output.drawString(50, 800, "Administración de Servicios en Red")
    output.drawString(50, 775, "Práctica 2 - adminitracion de contabilidad")
    output.drawString(50, 750, "Vargas Espino CArlos Hassan \t 4CM13")

    output.drawString(75, 700, "Nombre del dispositivo: " + name)
    output.drawString(75, 725, "S.O.: " + os)
    output.drawString(75, 675, "Contacto: " + contact)
    output.drawString(75, 650, "Ubicacion: " + ubi)
    output.drawString(75, 625, "No. de interfaces: " + numInter)

    i = 1
    matriz = [["INTERFACE", "STATUS"]]
    while i <= 6:
        if os.find("Linux") != -1:
            descrInterfaz = consultaSNMP(comunidad, ip, "1.3.6.1.2.1.2.2.1.2." + str(i), puerto)
        else:
            res = consultaSNMP(comunidad, ip, "1.3.6.1.2.1.2.2.1.2." + str(i), puerto)[3:]
            descrInterfaz = bytes.fromhex(res).decode('utf-8')

        estadoInterfaz = consultaSNMP(comunidad, ip, "1.3.6.1.2.1.2.2.1.7." + str(i), puerto)

        if estadoInterfaz == "1":
            matriz.append([descrInterfaz, "UP"])
        elif estadoInterfaz == "2":
            matriz.append([descrInterfaz, "DOWN"])
        else:
            matriz.append([descrInterfaz, "TESTING"])
        i = i + 1

    width = 200
    height = 400
    x = 50
    y = 450
    f = Table(matriz)
    f.wrapOn(output, width, height)
    f.drawOn(output, x, y)
    
    output.showPage()

    output.drawString(50, 800, "Administración de Servicios en Red")
    output.drawString(50, 775, "Práctica 2 - administracion de contabiliad")
    output.drawString(50, 750, "version: 1")
    output.drawString(50, 725, "device: " + consultaSNMP(comunidad, ip, "1.3.6.1.2.1.1.5.0", puerto))
    output.drawString(50, 700, "date: " + time.strftime("%d/%m/%Y - %H:%M:%S"))
    output.drawString(50, 675, "dafaultProtocol: radius")
    output.drawString(50, 650, "rdate: " + time.strftime("%d/%m/%Y - %H:%M:%S"))
    output.drawString(50, 625, "")
    output.drawString(50, 600, "#User-Name")
    output.drawString(50, 575, "1: " + consultaSNMP(comunidad, ip, "1.3.6.1.2.1.1.4.0", puerto))
    output.drawString(50, 550, "#Acct-Input-Octets")
    output.drawString(50, 525, "42: " + consultaSNMP(comunidad, ip, "1.3.6.1.2.1.2.2.1.10.3", puerto))
    output.drawString(50, 500, "#Acct-Output-Octets")
    output.drawString(50, 475, "43: " + consultaSNMP(comunidad, ip, "1.3.6.1.2.1.2.2.1.16.3", puerto))
    output.drawString(50, 450, "#Acct-Session-Time")
    output.drawString(50, 425, "46: " + consultaSNMP(comunidad, ip, "1.3.6.1.2.1.1.3.0", puerto))
    output.drawString(50, 400, "#Acct-Input-Packets")
    output.drawString(50, 375, "47: " + consultaSNMP(comunidad, ip, "1.3.6.1.2.1.2.2.1.11.3", puerto))
    output.drawString(50, 350, "#Acct-Output-Packets")
    output.drawString(50, 325, "48: " + consultaSNMP(comunidad, ip, "1.3.6.1.2.1.2.2.1.17.3", puerto))

    output.showPage()

    output.drawString(50, 800, "Administración de Servicios en Red")
    output.drawString(50, 775, "Práctica 2 - aministracion de contabilidad")
    output.drawInlineImage( "./unicastPaq.png", 50, 600, 200, 125)
    output.drawInlineImage( "./ipv4Paq.png", 300, 600, 200, 125)
    output.drawInlineImage( "./echoICMP.png", 50, 450, 200, 125)
    output.drawInlineImage( "./segmentoEntrada.png", 300, 450, 200, 125)
    output.drawInlineImage( "./datagramaSalida.png", 50, 300, 200, 125)
    
    output.showPage()
    output.save()

    
def graficar():
    print("Fecha inicio (a/m/d):")
    fechaInicial = input()
    print("Fecha final (a/m/d H:M:S):")
    fechaFinal = input()
    tiempo_final =  int(datetime.strptime(fechaFinal, "%Y/%m/%d %H:%M:%S").timestamp())
    tiempo_inicial = int(datetime.strptime(fechaInicial, "%Y/%m/%d %H:%M:%S").timestamp())

    ret = rrdtool.graphv( "unicastPaq.png",
                     "--start",str(tiempo_inicial),
                     "--end","N",
                     "--vertical-label=Paquetes",
                     "--title= Paquetes unicast recibidos \n por la interfaz",
                     "DEF:eweEntrada=segmentosRed.rrd:unicastPaq:AVERAGE",
                      "VDEF:paqEntradaLast=eweEntrada,LAST",
                      "VDEF:paqEntradaFirst=eweEntrada,FIRST",
                      "VDEF:paqEntradaMax=eweEntrada,MAXIMUM",
                      "VDEF:paqEntradaDev=eweEntrada,STDEV",
                      "CDEF:Nivel1=eweEntrada,7,GT,0,eweEntrada,IF",
                      "PRINT:paqEntradaLast:%6.2lf",
                      "PRINT:paqEntradaFirst:%6.2lf",
                     "GPRINT:paqEntradaMax:%6.2lf %S segEntMAX",
                     "GPRINT:paqEntradaDev:%6.2lf %S STDEV",
                     "LINE3:eweEntrada#FF0000:Paquetes recibidos" )
                    
                    
    ret = rrdtool.graphv( "ipv4Paq.png",
                     "--start",str(tiempo_inicial),
                     "--end","N",
                     "--vertical-label=Paquetes",
                     "--title= Paquetes recibidos a \n protocolos IPV4",
                     "DEF:eweEntrada=segmentosRed.rrd:ipv4Paq:AVERAGE",
                      "VDEF:paqEntradaLast=eweEntrada,LAST",
                      "VDEF:paqEntradaFirst=eweEntrada,FIRST",
                      "VDEF:paqEntradaMax=eweEntrada,MAXIMUM",
                      "VDEF:paqEntradaDev=eweEntrada,STDEV",
                      "CDEF:Nivel1=eweEntrada,7,GT,0,eweEntrada,IF",
                      "PRINT:paqEntradaLast:%6.2lf",
                      "PRINT:paqEntradaFirst:%6.2lf",
                     "GPRINT:paqEntradaMax:%6.2lf %S segEntMAX",
                     "GPRINT:paqEntradaDev:%6.2lf %S STDEV",
                     "LINE3:eweEntrada#F0F0000:Paquetes recibidos" )
                     
                     
                     
    ret = rrdtool.graphv( "echoICMP.png",
                     "--start",str(tiempo_inicial),
                     "--end","N",
                     "--vertical-label=Segmentos",
                     "--title= Mensajes ICMP echo \n que ha enviado el agente",
                     "DEF:eweEntrada=segmentosRed.rrd:echoICMP:AVERAGE",
                      "VDEF:paqEntradaLast=eweEntrada,LAST",
                      "VDEF:paqEntradaFirst=eweEntrada,FIRST",
                      "VDEF:paqEntradaMax=eweEntrada,MAXIMUM",
                      "VDEF:paqEntradaDev=eweEntrada,STDEV",
                      "CDEF:Nivel1=eweEntrada,7,GT,0,eweEntrada,IF",
                      "PRINT:paqEntradaLast:%6.2lf",
                      "PRINT:paqEntradaFirst:%6.2lf",
                     "GPRINT:paqEntradaMax:%6.2lf %S segEntMAX",
                     "GPRINT:paqEntradaDev:%6.2lf %S STDEV",
                     "LINE3:eweEntrada#0000FF:Mensajes ICMP echo" )
                     
                     
                     
    ret = rrdtool.graphv( "segmentoEntrada.png",
                     "--start",str(tiempo_inicial),
                     "--end","N",
                     "--vertical-label=Segmentos",
                     "--title= Segmentos recibidos",
                     "DEF:eweEntrada=segmentosRed.rrd:segmentoEntrada:AVERAGE",
                      "VDEF:paqEntradaLast=eweEntrada,LAST",
                      "VDEF:paqEntradaFirst=eweEntrada,FIRST",
                      "VDEF:paqEntradaMax=eweEntrada,MAXIMUM",
                      "VDEF:paqEntradaDev=eweEntrada,STDEV",
                      "CDEF:Nivel1=eweEntrada,7,GT,0,eweEntrada,IF",
                      "PRINT:paqEntradaLast:%6.2lf",
                      "PRINT:paqEntradaFirst:%6.2lf",
                     "GPRINT:paqEntradaMax:%6.2lf %S segEntMAX",
                     "GPRINT:paqEntradaDev:%6.2lf %S STDEV",
                     "LINE3:eweEntrada#FF0000:Segmentos recibidos" )
                     
                     
                     
    ret = rrdtool.graphv( "datagramaSalida.png",
                     "--start",str(tiempo_inicial),
                     "--end","N",
                     "--vertical-label=Segmentos",
                     "--title= Paquetes unicast recibidos \n por la interfaz",
                     "DEF:eweEntrada=segmentosRed.rrd:datagramaSalida:AVERAGE",
                      "VDEF:paqEntradaLast=eweEntrada,LAST",
                      "VDEF:paqEntradaFirst=eweEntrada,FIRST",
                      "VDEF:paqEntradaMax=eweEntrada,MAXIMUM",
                      "VDEF:paqEntradaDev=eweEntrada,STDEV",
                      "CDEF:Nivel1=eweEntrada,7,GT,0,eweEntrada,IF",
                      "PRINT:paqEntradaLast:%6.2lf",
                      "PRINT:paqEntradaFirst:%6.2lf",
                     "GPRINT:paqEntradaMax:%6.2lf %S segEntMAX",
                     "GPRINT:paqEntradaDev:%6.2lf %S STDEV",
                     "LINE3:eweEntrada#0F0FFF:DatagramasUDP" )







graficar()
generarReporte()











