#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#importamos modulo para añadir colores a la terminal
from termcolor import colored
#importamos la libreria para trabajar con comandos del sistema
import subprocess
#diseñamos un logo para el programa
logo = """
░█████╗░██████╗░██████╗░██╗░░░██╗██╗███╗░░██╗░█████╗░
██╔══██╗██╔══██╗██╔══██╗██║░░░██║██║████╗░██║██╔══██╗
███████║██████╔╝██║░░██║██║░░░██║██║██╔██╗██║██║░░██║
██╔══██║██╔══██╗██║░░██║██║░░░██║██║██║╚████║██║░░██║
██║░░██║██║░░██║██████╔╝╚██████╔╝██║██║░╚███║╚█████╔╝
╚═╝░░╚═╝╚═╝░░╚═╝╚═════╝░░╚═════╝░╚═╝╚═╝░░╚══╝░╚════╝░

████████╗░█████╗░
╚══██╔══╝██╔══██╗
░░░██║░░░██║░░██║
░░░██║░░░██║░░██║
░░░██║░░░╚█████╔╝
░░░╚═╝░░░░╚════╝░

██████╗░██╗░░░░░░█████╗░
██╔══██╗██║░░░░░██╔══██╗
██████╔╝██║░░░░░██║░░╚═╝
██╔═══╝░██║░░░░░██║░░██╗
██║░░░░░███████╗╚█████╔╝
╚═╝░░░░░╚══════╝░╚════╝░
"""

#definimos un menu
menu = """
1) Crear Ladder
2) Subir Ladder
3) Ayuda
4) Salir
"""

#definimos la forma grafica de los componentes
componentes = """
Seleccione un componente
1) --| |-- 2) --|/|-- 3) --( )-- 4) -(end)-
"""

#definimos la seccion de ajustes del Arduino
ajustes = """void setup(){
  pinMode(0,INPUT);
  pinMode(1,INPUT);
  pinMode(2,INPUT);
  pinMode(3,INPUT);
  pinMode(4,INPUT);
  pinMode(5,INPUT);
  pinMode(6,INPUT);
  pinMode(7,INPUT);
  pinMode(8,OUTPUT);
  pinMode(9,OUTPUT);
  pinMode(10,OUTPUT);
  pinMode(11,OUTPUT);
  pinMode(12,OUTPUT);
  pinMode(13,OUTPUT);
}
"""

#definmos la lectura de todas las entradas del arduino
inicio = """void loop(){
  bool i0 = digitalRead(0);
  bool i1 = digitalRead(1);
  bool i2 = digitalRead(2);
  bool i3 = digitalRead(3);
  bool i4 = digitalRead(4);
  bool i5 = digitalRead(5);
  bool i6 = digitalRead(6);
  bool i7 = digitalRead(7);\n"""

#creamos una funcion principal
def main():
    #mostramos el logotipo
    print(logo)
    #cramos un bucle infinito para soliciar una opcion
    while True:
        #mostramos el menu
        print(colored(menu, "blue"))
        #solicitamos una opcion
        opcion = input(": ")
        #si la opcion es 1...
        if opcion == "1":
            #llamamos a la funcion crear codigo ladder
            crear()
        #si la opcion es 2...
        elif opcion == "2":
            #llamamos a la funcion subir codigo al arduino
            subir()
        #si la opcion es 3...
        elif opcion == "3":
            #mostramos como usar el programa
            ayuda()
        #si la opcion es 4...
        elif opcion == "4":
            #salimos del programa
            exit()
        #en caso de que no se haya escogido una opcion similar
        else:
            #se muestra un mensaje de error
            print(colored("Comando desconocido!", "red"))
#definimos una función para crear el programa del Arduino usando lenguaje Ladder
def crear():
    #creamos un archivo de texto para guardar el diagrama
    with open("plc.txt", "w") as ladder:
        #escribimos en el diagrama el inicio
        ladder.write("-(start)-\n")
    #creamos un nuevo archivo para arduino
    with open("programa/programa.ino", "w") as arduino:
        #escribimos en el las configuraciones de salidas y entradas
        arduino.write(ajustes)
        #escribimos en el la funcion que siempre se estara repitiendo
        arduino.write(inicio)
        #cuenta de componentes
        cuenta = 0
        #tipo de componentes
        tipos = []
        #pines usados
        pines = []
        #creamos un bucle para añadir componentes
        while True:
            #mostramos los componentes
            print(colored(componentes, "blue"))
            #solicitamos que componente usar
            componente = input(": ")
            #escribimos el componente
            escribir(componente)
            #mostramos el diagrama
            mostrar()
            #si la opcion del componente fue 1
            if componente == "1":
                #sumamos un 1 a los componentes usados
                cuenta += 1
                #agregamos el tipo de componente
                tipos.append("NA")
            #si la opcion del componente fue 2
            elif componente == "2":
                #sumamos un 1 a los componentes usados
                cuenta += 1
                #agregamos el tipo de componente
                tipos.append("NC")
            #si la opcion del componente fue 3
            elif componente == "3":
                #sumamos un 1 a los componentes usados
                cuenta += 1
                #agregamos el tipo de componente
                tipos.append("OUT")
                #recorremos cada componente
                for valor in range(cuenta):
                    #solicitaos el pin del componente
                    pin = input(colored("Ingresa un pin: ", "green"))
                    #agregamos a la lista el numero del pin usado
                    pines.append(pin)
                    #agregamos el pin al diagrama
                    enumerar(pin)
                #abrrimos el diagrama txt
                with open("plc.txt", "a") as diagrama_enumerado:
                    #escribimos un salto de linea
                    diagrama_enumerado.write("\n")
                #mostraos el diagrama
                mostrar()
                #recorremos los pines ingresados
                for valor in range(cuenta):
                    #si es el primer elemento
                    if valor == 0:
                        #si es un contacto abierto
                        if tipos[valor] == "NA":
                            #escribimos el inicio de una condicion
                            arduino.write("  if(i{}".format(pines[valor]))
                        #si el contacto es cerrado
                        elif tipos[valor] == "NC":
                            #escribimos el inicio de una condicion negada
                            arduino.write("  if(not i{}".format(pines[valor]))
                    # si no es el primer componente ni el ultimo
                    elif valor != 0 and valor != cuenta-1:
                        #si es abirto
                        if tipos[valor] == "NA":
                            # agregamos la condicional and y el pin
                            arduino.write(" and i{}".format(pines[valor]))
                        #si es cerrado
                        elif tipos[valor] == "NC":
                            # agregamos la condicional and y el pin negado
                            arduino.write(" and not i{}".format(pines[valor]))
                    #y si es el ultimo componente
                    elif valor == cuenta-1:
                        #cerramos la  condicion
                        arduino.write("){\n")
                        #encendemos la salida indicada
                        arduino.write("    digitalWrite({}, HIGH);\n".format(pines[valor]))
                        #cerramos la funcion
                        arduino.write("  }\n")
                        #agregamos unna condion en caso de que no se cumpla la condicion
                        arduino.write("  else{\n")
                        #apagamos la salida indicada
                        arduino.write("    digitalWrite({}, LOW);\n".format(pines[valor]))
                        #escribimos el final del programa
                        arduino.write("  }\n")
                #reseteamos la cuenta de los componentes
                cuenta = 0
                #reseteamos los tipos de componentes
                tipos = []
                #reseteamos los pines
                pines = []
            #si la opcion del componente fue 4
            elif componente == "4":
                #si la opcion fue 4 salimos de la creacion del diagrama
                break
        #escribimos el final del programa
        arduino.write("}")
#definimos una funcion para escribir cada componente en un diagrama
def escribir(componente):
    #abrimos archivo de texto para el diagrama
    with open("plc.txt", "a") as archivo:
        #si la opcion fue 1
        if componente == "1":
            #escribimos un contacto abierto
            archivo.write("--| |--")
        #si la opcion fue 2
        elif componente == "2":
            #escribimos un contacto cerrado
            archivo.write("--|/|--")
        #si la opcion fue 3
        elif componente == "3":
            #escribimos una bobina
            archivo.write("--( )--\n")
        #si la opcion fue 4
        elif componente == "4":
            #escribimos el final del diagrama
            archivo.write("-(end)-\n")
        #si la opcion fue desconocida
        else:
            #mostramos un error
            print(colored("Comando desconocido!","red"))
#definimos una funcion para enumerar cada componente
def enumerar(pin):
    #abrimos el diagrama
    with open("plc.txt", "a") as enumerados:
        #escribimos el pin del componente
        enumerados.write("   {}   ".format(pin))
#definimos una funcion para mostrar el diagrama que llevamos hasta el momentos
def mostrar():
    #abrimos el diagrama
    with open("plc.txt", "r") as lectura:
        #damos un salto de linea
        print("")
        #iteramos por el documento
        for linea in lectura:
            #mostramos cada linea del diagrama
            print(colored(linea, "yellow"))
#definimos una función para subir el programa al Arduino
def subir():
    #nos movemos a la carpeta del programa
    Comando = subprocess.run(["cd", "programa"], shell=True)
    #abrimos el programa
    Comando = subprocess.run(["arduino", "programa.ino"])
#definimos una funcion que muestra como usar el programa
def ayuda():
    #mostramos una ayuda
    print(colored("-------------------------------------------------------------", "yellow"))
    #mostramos una ayuda
    print(colored("                        Menu", "yellow"))
    #mostramos una ayuda
    print(colored("-------------------------------------------------------------", "yellow"))
    #mostramos una ayuda
    print(colored("\n1) Crear ladder", "blue") + """ Funcion que permite crear un diagrama
                ladder y un codigo para arduino.\n""")
    #mostramos una ayuda
    print(colored("2) Subir ladder", "blue") + """ Funcion que permite subir un diagrama
                ladder y un codigo para arduino.\n""")
    #mostramos una ayuda
    print(colored("3) Ayuda", "blue") + " Funcion que permite mostrar la funcion de cada elemento.\n")
    #mostramos una ayuda
    print(colored("4) Salir", "blue") + " Funcion que permite cerrar el programa.\n")
    #mostramos una ayuda
    print(colored("-------------------------------------------------------------", "yellow"))
    #mostramos una ayuda
    print(colored("                     Componentes", "yellow"))
    #mostramos una ayuda
    print(colored("-------------------------------------------------------------", "yellow"))
    #mostramos una ayuda
    print(colored("\n--| |--", "blue") + " Funcion que permite añadir un contacto NA.\n")
    #mostramos una ayuda
    print(colored("--|/|--", "blue") + " Funcion que permite añadir un contacto NC.\n")
    #mostramos una ayuda
    print(colored("--( )--", "blue") + " Funcion que permite añadir una bobina.\n")
    #mostramos una ayuda
    print(colored("--end--", "blue") + " Funcion que permite añadir el final del programa.\n")
    #mostramos una ayuda
    print(colored("-------------------------------------------------------------", "yellow"))
#creamos un punto de acceso
if __name__ == '__main__':
    #llamamos a la funcion principal
    main()
