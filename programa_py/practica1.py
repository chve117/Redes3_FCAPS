import os
from importlib_metadata import version
from pysnmp.hlapi import *
from fpdf import FPDF
from requests import delete

#funcion de consulta snmp
def consultaSNMP(comunidad, host, oid, puerto):
    iterator = getCmd(
    SnmpEngine(),
    CommunityData(comunidad, mpModel=0),
    UdpTransportTarget((host, puerto)),
    ContextData(),
    ObjectType(ObjectIdentity(oid))
    )

    errorIndication, errorStatus, errorIndex, varBinds = next(iterator)

    if (errorIndication):
     print(errorIndication)

    elif (errorStatus):
     print('%s at %s' % (errorStatus.prettyPrint(), errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))

    else:
     for varBind in varBinds:
        hola= ' = '.join([x.prettyPrint() for x in varBind])
        resultado = hola.split("=")[1]
    return resultado


#Agregar dispositivo
def agregadispositivo():
    print(" ")
    comunidad = input("Comunidad: ")
    versionp = input("version: ")
    puerto = input("puerto: ") 
    ip = input("Ip: ")

    with open("datos.txt", "a") as file:
        file.write(comunidad + " " + versionp+ " " + puerto + " " + ip + " ")
 
#Modifica informacion
def modifica():
    print(" ")
    i=1
    print("Equipos almacenados: ")
    with open("datos.txt", "r") as file:
        dattos = file.readlines()


    with open("datos.txt", "r") as file:
        for line in file:
            print(str(i)+"\t"+line)
            i=i+1

    modificacion = int(input("Indique el registro a modificar: "))
    i=1
    print(" ")
    comunidad = input("Comunidad: ")
    versionp = input("version: ")
    puerto = input("puerto: ") 
    ip = input("Ip: ")
    print(" ")
 
    with open("datos.txt", "w") as file:
        for line in dattos:
            if i != modificacion:
                file.write(line)
            else:
                file.write(comunidad + " " + versionp+ " " + puerto + " " + ip + " ")
            i=i+1

#borrar usuario
def deleate():
    i=1
    with open("datos.txt", "r") as file:
        dattos = file.readlines()
    print("Dispositivos: ")
    with open("datos.txt","r") as file:
        for line in file:
            print(str(i)+ "\t"+line)
            i=i+1
    
    borrar = int(input("Dispositivo a borrar: "))
    i=1
    with open("datos.txt", "w") as file:
        for line in dattos:
            if i !=borrar:
                file.write(line)
            i = i+1
    
#información de usuario
yo= "Vargas Espino Carlos Hassan"
grupo="3CM15" 
boleta="2015090783"
print("Practica 1 - Adquisicion de Información")
print("Sistema de Administración de red")
print("Alumno: ", yo, "Grupo: ", grupo, "Boleta: ", boleta)
print("\n")
#menu
opcion = int(input("ELige una opción:\n 1)Agregar dispositivo \n 2)Cambiar dispositivo \n 3)Eliminar dispositivo\n 4)Generar reporte\n"))
if(opcion == 1):
    print("Decidio agregar un dispositivo")
    agregadispositivo()
elif(opcion == 2):
    print("Decidio Cambiar dispositivo")
    modifica()
elif(opcion == 3):
    print("Borrar dispositivo")
    deleate()
elif(opcion == 4):
    print("Generar reporte")
    #Imprimo dispositivos registrados
    with open ("datos.txt", "r") as file:
        dispositivos = file.readlines()
    
    i=1
    print("Dispositivos: ")
    with open("datos.txt", "r") as file:
        for linea in file:
            print(str(i) + "\t" + linea)
            i=i+1
    ndispositivo = int(input("Ingrese el dispositivo pal reporte: ")) -1
    datos = dispositivos[ndispositivo].split()
    #separa el txt por componentes de datos
    comunidad = datos[0]
    versionsnmp = datos[1]
    puerto = datos[2]
    ip = datos[3]
    #hacer consulta snmp
    RespuestaSNMP = consultaSNMP(comunidad, ip,"1.3.6.1.2.1.1.1.0",puerto)
    os="No importa"
    if RespuestaSNMP.find("Linux") ==1:
        os = RespuestaSNMP.split()[0]
    else:
        os = RespuestaSNMP.split()[12]

    nombre = consultaSNMP(comunidad, ip,"1.3.6.1.2.1.1.5.0",puerto)
    contact = consultaSNMP(comunidad, ip,"1.3.6.1.2.1.1.4.0",puerto)
    ubicacion = consultaSNMP(comunidad, ip,"1.3.6.1.2.1.1.6.0",puerto)
    numInter = consultaSNMP(comunidad, ip,"1.3.6.1.2.1.2.1.0",puerto)
    
    print("nombre" +nombre,"contacto" +contact,"ubicacion: "+ ubicacion,"Interfaz:" + numInter)
    i=1
    interfaz =[]
    while i<=2:
        interfa = consultaSNMP(comunidad, ip, "1.3.6.1.2.1.2.2.1.7."+str(i), puerto)
        interfaz.append(interfa)
        i=i+1
    #generar pdf   
    pdf = FPDF()
    pdf.add_page()
    #TEXTO
    pdf.set_font('Arial', '', 15)
    pdf.text(x= 20, y= 30, txt='Administración de servicios de red')
    pdf.text(x= 20, y= 40, txt='Práctica 1')
    pdf.text(x= 20, y= 55, txt='Nombre: '+ yo + " Grupo: " + grupo)
    pdf.text(x= 20, y= 70, txt='Información del Inventario')
    pdf.text(x= 20, y= 85, txt='Información de interfaces')
    #Imagen
    pdf.image('ublogo.png',x=75, y= 120, w=50, h=50)
    #informaciondispositivo
    pdf.text(x= 20, y= 100, txt='Dispositivo: ' + nombre)
    pdf.text(x= 20, y= 110, txt='Contacto: ' + contact)
    pdf.text(x= 20, y= 120, txt='Ubicacion: ' + ubicacion)
    pdf.text(x= 20, y= 130, txt='N interfaz: ' + numInter)
    #tabla
    pdf.set_xy(20,180)
    pdf.cell(w=180, h=15, txt="Reporte", border=1, ln=1, align= 'C', fill=0)
    #celda
    pdf.set_xy(20,195)
    pdf.cell(w=90, h=15, txt="Interfaz", border=1, ln=0, align= 'C', fill=0)
    pdf.cell(w=90, h=15, txt="Estado", border=1, ln=0, align= 'C', fill=0)
    i=1
    y= 210
    while i<=3:
        if os.find("Linux") !=-1:
            Hinterfaz = consultaSNMP(comunidad,ip,"1.3.6.1.2.1.2.2.1.2."+str(i),puerto)
        else:
            respu = consultaSNMP(comunidad,ip,"1.3.6.1.2.1.2.2.1.2."+str(i),puerto)[3:]
            Hinterfaz = bytes.fromhex(respu).decode('utf-8')
        
        estadoI = consultaSNMP(comunidad,ip,"1.3.6.1.2.1.2.2.1.7."+str(i),puerto)
        if estadoI == " 1":
             pdf.set_xy(20,y)
             pdf.cell(w=90, h=15, txt=Hinterfaz, border=1, ln=0, align= 'C', fill=0)
             pdf.cell(w=90, h=15, txt="UP", border=1, ln=0, align= 'C', fill=0)
             y = y+20
        elif estadoI ==" 2":
             pdf.set_xy(20,y)
             pdf.cell(w=90, h=15, txt=Hinterfaz, border=1, ln=0, align= 'C', fill=0)
             pdf.cell(w=90, h=15, txt="DOWN", border=1, ln=0, align= 'C', fill=0)
             y = y+20
        else:
             pdf.set_xy(20,y)
             pdf.cell(w=90, h=15, txt=Hinterfaz, border=1, ln=0, align= 'C', fill=0)
             pdf.cell(w=90, h=15, txt="TESTING", border=1, ln=0, align= 'C', fill=0)
             y = y+20
        i=i+1
        
    pdf.output('Reporte.pdf')
else:
    exit()

