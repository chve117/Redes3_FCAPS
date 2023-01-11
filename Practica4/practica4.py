import telnetlib
from ftplib import FTP
import subprocess

user = "rcp"
password = "rcp"

def generarArchivo():
	print("\nProporcione la ip para realizar la conexion con el router:")
	host = input()
	tn = telnetlib.Telnet()
	tn.open(host)
	tn.read_until(b"User: ")
	tn.write(user.encode("ascii")+b"\r\n")
	tn.read_until(b"Password: ")
	tn.write(password.encode("ascii")+b"\r\n")
	tn.write(b"en\r\n")
	tn.write(b"config\r\n")
	tn.write(b"copy run start\r\n")
	tn.write(b"exit\r\n")
	tn.write(b"exit\r\n")
	tn.write(b"exit\r\n")
	tn.read_all()
	tn.close()
	print("Se genero el archivo de configuración")
	
def extraerArchivo():
	print("\nProporcione la ip para realizar la conexion con el router:")
	host = input()
	print("\nProporcione el nombre del route:")
	name = input()
	tn = telnetlib.Telnet()
	tn.open(host)
	tn.read_until(b"User: ")
	tn.write(user.encode("ascii")+b"\r\n")
	tn.read_until(b"Password: ")
	tn.write(password.encode("ascii")+b"\r\n")
	tn.write(b"en\r\n")
	tn.write(b"config\r\n")
	tn.write(b"service ftp\r\n")
	tn.write(b"exit\r\n")
	tn.write(b"exit\r\n")
	tn.write(b"exit\r\n")
	tn.read_all()
	tn.close()
	
	ftp = FTP (host)
	ftp.login(user,password)
	ftp.retrbinary('RETR startup-config',open('startup-config-' + name , 'wb').write)
	ftp.quit()
	print("Se descargo el archivo de configuración")
	
def importarArchivo():
	print("\nProporcione la ip para realizar la conexion con el router:")
	host = input()
	print("\nProporcione el nombre del route:")
	name = input()
	tn = telnetlib.Telnet()
	tn.open(host)
	tn.read_until(b"User: ")
	tn.write(user.encode("ascii")+b"\r\n")
	tn.read_until(b"Password: ")
	tn.write(password.encode("ascii")+b"\r\n")
	tn.write(b"en\r\n")
	tn.write(b"config\r\n")
	tn.write(b"service ftp\r\n")
	tn.write(b"exit\r\n")
	tn.write(b"exit\r\n")
	tn.write(b"exit\r\n")
	tn.read_all()
	tn.close()
	
	ftp = FTP (host)
	ftp.login(user,password)
	f = open('startup-config-'+name,'rb')
	ftp.storbinary('STOR startup-config',f)
	f.close()
	ftp.quit()
	print("Se envio el archivo de configuración")
	menu()
	
def menu():
	print("Sistema de administración")
	print("1. Generar el archivo de configuración")
	print("2. Extraer el archivo de configuración.")
	print("3. Importar el archivo de configuración.")
	opc = input()
	if opc =="1":
		generarArchivo()
	if opc == "2":
		extraerArchivo()
	if opc == "3":
		importarArchivo()

	else:
	 exit()
	

menu()
