#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       tp2_main.py
#  Estructura: Nombre de la pelicula;Año;Director;Actor1,Actor2,...,ActorN;Genero
#Version= 1.6-final 18.05.2012 19:08:15


#NOTAS:
#Ejemplo ./main_tp2.py -a ejemplo.txt -p "Brad Pitt"




#Modulos // solo importo lo que me interesa
from csv import reader
from sys import argv
from optparse import OptionParser
from random import randint

def extraer_datos(ruta,argv):
    """Recibe: cadena, Devuelve: cadena,entero
    Extrae los datos del archivo, cierra el archivo y los devuelve,
    tambien devuelve la cantidad de lineas del archivo"""
    #variables
    handler=file #manejador de archivos
    contenido=[]
    linea=""

    #codigo
    try:
        handler=open(ruta,"r")
        for linea in handler:   #leo linea por linea
            contenido.append(linea)
        handler.close()
        return contenido, len(contenido)
    except:
        print "[E] Ocurrio algun error, el fichero puede no existir\
o no se tienen los permisos de lectura"
        if len(argv)>1: #varia segun la menera en la qeu fue ejecutado
            exit(1)
        else:
            return False, None

def csv_reader(contenido):
    """Recibe:cadena, Devuelve: manejador csv
    Interpreta lo que recive, y devuelve un manejador"""

    lector=reader(contenido, delimiter=";")
    return lector

def estructuras(lista):
    """Recibe:lista o nada Devuelve: Nada
    Muestra de manera ordenada los datos recibidos, si no recibe algun
    dato, no lo muestra, si recibe una ruta, llamara a la funcion
    escribir_archivo() para guardar los datos"""
    #variables
    indice = 0
    elemento = ""
    etiquetas = { 0:"Pelicula: " , 1:"Año: " , 2:"Director: " , 
    3:"Actores: ", 4:"genero: " }
   
    #codigo
    if not lista[-1]  :
        print "\n"  
        for indice,elemento in enumerate(lista[ : len(lista)-1]):
            if elemento != None:
                print etiquetas[indice]+elemento
    else:
        escribir_archivo(lista[-1],"\n")
        for indice,elemento in enumerate(lista[ : len(lista)-1]):
            if elemento != None:
                escribir_archivo(lista[-1],etiquetas[indice]+elemento+"\n")

def ficha_tecnica(pelicula,lector,cantidad_lineas,ruta_salida=None):
    """Recibe: cadena, _csv.reader,entero,cadena Devuelve: nada
    Busca el nombre de la pelicula, e imprime su ficha tecnica"""
    #Variables
    ano=""
    director=""
    actores=""
    genero=""
    peliculaaux="" #Para recorrer la lista de peliculas
    contador=0 #Contador de uso generico
    entrar=True

    #codigo
    if len(ruta_salida)==0:
        ruta_salida=None
        print "-----------Ficha Tecnica-----------"
    else:#Para que quede ordenado
        escribir_archivo(ruta_salida,"------------------\nFicha Tecnica:\n")
    for peliculaaux,ano,director,actores,genero in lector:
         #Recorro comparando la pelicula elegida contra las que hay
        contador+=1
        if pelicula.lower()==peliculaaux.lower():
            entrar=False
            estructuras([pelicula,ano,director,actores,genero,ruta_salida])
        elif (pelicula.lower()!=peliculaaux.lower()) and (cantidad_lineas==contador) and (entrar==True):
            print "Parece que esa pelicula no esta listada, ¿por que no"\
            " buscas otra?"
    if ruta_salida:#Para que quede ordenado
        escribir_archivo(ruta_salida,"------------------\n")

def por_actor(actor,lector,cantidad_lineas,ruta_salida=None):
    """Recibe: cadena,cadena,entero,cadena Devuelve: nada
    Busca el nombre del actor, e imprmie los actores y actrices,
    directores con los que ah trabajado, filmografia , y genero,
    ordenado cronologicamente"""
    #variables
    contador=0 #Contador de uso generico
    indice=0 #indice de uso generico
    actoresaux=[]
    entrar=True#es para decidir si entrar en el elif
    diccionario={}
    ano_ordenado=[]
    ano_sin_salt=[]

    #codigo
    if len(ruta_salida)==0:
        ruta_salida=None
    else: #Para que quede ordenado
        escribir_archivo(ruta_salida,"------------------\n Busqueda por actor:" +actor+"\n")
    for peliculaaux,ano,director,actores,genero in lector:
        contador+=1
        if actor in (actores).split(","): #lista de actores
            entrar=False
            salt=str(randint(0,9**9))
            actoresaux = quita_actor(actores, actor)            
            diccionario[ano+"-"+salt]=[director,",".join(actoresaux),genero,peliculaaux]
            #usamos randint para implementar un pequeño "salt", ya que
            #si el actor hubiera actuado en mas de una pelicula
            #el mismo año, la ultima sobrescribiria a las anteriores
        elif (actor not in actoresaux) and ((cantidad_lineas)==contador) and (entrar==True):
            print "Parece que ese actor no esta en la base de datos"
            if ruta_salida:
                escribir_archivo(ruta_salida,"Parece que ese actor no esta en la base de datos\n")
            break
    ano_ordenado=ordena_claves(diccionario)
    for indice in range(len(diccionario)):
        ano_sin_salt = quita_salt(ano_ordenado, indice)    
        estructuras([(diccionario[ano_ordenado[indice]])[3],"".join(ano_sin_salt),\
        (diccionario[ano_ordenado[indice]])[0],\
        (diccionario[ano_ordenado[indice]])[1],\
        (diccionario[ano_ordenado[indice]])[2],ruta_salida])
        ano_sin_salt=[] #limpio la variable
    if ruta_salida:#Para que quede ordenado
        escribir_archivo(ruta_salida,"------------------\n")

def quita_salt(ano_ordenado, indice):
    """Quita la implementacion del salt"""
    ano_sin_salt = []
    for caracter in ano_ordenado[indice]:
        if caracter=="-":
            break
        else:
            ano_sin_salt.append(caracter)
    return ano_sin_salt
    

def quita_actor(actores, actor):
    """Recibe: cadena, cadena, Devuelve: lista
    quita al actor entregado, de la lista de actores pasada"""
    actoresaux=(actores).split(",") #actores con los que
    actoresaux.remove(actor)                    #trabajo
    return actoresaux
    

def ordena_claves(diccionario):
    """Recibe: diccionario, Devuelve: lista
    Ordena las claves de un diccionario, y las devuelve"""
    return sorted(diccionario.keys())

def argumentos():
    """Recibe: nada, Devuelve: los argumentos recibidos
    Interpreta el posible argumento recibido"""
    parser=OptionParser()
    parser.add_option("-a", "--archivo", dest="ruta",
                  help="Define el archivo de la base de datos",
                  type="string", action="store")
    return parser.parse_args()



def cruzar_datos(paquete,lector,cantidad_lineas,ruta_salida=None):
    """Recibe: cadena Devuelve: nada
    Busca las peliculas donde el actor y el direcctor trabajaron juntos"""
    #variables
    #codigo
    if len(ruta_salida)==0:
        ruta_salida=None
    else: #Para que quede ordenado
        escribir_archivo(ruta_salida,"\n------------------\nCruze de Datos:" +paquete+"\n")
    if len(paquete.split(","))==2:
        if ((paquete.split(","))[1].isdigit()): 
            #verifica que el segundo campo sea digito
            actor_ano(paquete,lector,cantidad_lineas,ruta_salida)                                  
        elif ((paquete.split(","))[1].isdigit()==False):
             #verifica que el segundo campo no sea digito
            actor_director(paquete,lector,cantidad_lineas,ruta_salida)
        else:
            print "Es posible que te hayas equivocado al ingresar los" \
            " datos"
    else:
        print "Parece que escribiste algo mal."

def actor_ano(paquete,lector,cantidad_lineas,ruta_salida=None):
        """Muetra o escribie los datos, cuando recibe un actor
    y un año"""
    actor_ano=()
    contador=0 #contador de uso generico
    entrar = True

    actor_ano=((paquete.split(","))[0],(paquete.split(","))[1])
    for pelicula,ano,director,actores,genero in lector:
        contador+=1
        if (actor_ano[0] in actores.split(","))\
         and (actor_ano[1]==ano):
            entrar=False
            estructuras([pelicula,None,None,None,None,ruta_salida])
        elif ((cantidad_lineas)==contador) and (entrar==True):
            print "Parece que no hay concidencias"
            break
    if ruta_salida:#Para que quede ordenado
        escribir_archivo(ruta_salida,"------------------\n")
    
    
        
def actor_director(paquete,lector,cantidad_lineas,ruta_salida=None):
    """Muetra o escribie los datos, cuando recibe un actor
    y un director"""
    contador=0 #contador de uso generico
    actor_director=()
    entrar = True
    actor_director=((paquete.split(","))[0],(paquete.split(","))[1])
    for pelicula,ano,director,actores,genero in lector:
        contador+=1
        if (actor_director[0] in actores.split(",")) and\
         (actor_director[1]==director):
            entrar=False
            estructuras([pelicula,None,None,None,None,ruta_salida])
        elif ((cantidad_lineas)==contador) and (entrar==True):
            print "Parece que no hay concidencias"
            break
    if ruta_salida:#Para que quede ordenado
        escribir_archivo(ruta_salida,"------------------\n")
    


def escribir_archivo(ruta_salida,datos):
    """Recibe:cadena, cadena Devuelve:Nada
    Guarda en un archivo todos los datos que devolveria/imprimiria
     el programa"""
    #variables
    archivo=file
    #codigo
    try:
        archivo=open(ruta_salida,"a")
        archivo.write(datos)
        archivo.close()
    except:
        print "[E] Ocurrio algun error, puede que no tenga permisos\
        escribir sobre el archivo"
        if len(argv)>1: #varia segun la menera en la que fue ejecutado
            exit(1)

def menu():
    #varaibles
    opt=""
    opciones=["1","2","3","4","5","6","7"]
    while True:
        print "\n\n"
        print "^.^ TP2 ^.^".center(50)
        print r"""
        
        1)Ficha tecnica
        2)Buscar por actor
        3)Cruzar datos
        4)Agregar una pelicula
        5)Formatear (le da el formato que esta aplicacion usa)
        6)Releer archivos
        7)Salir""".center(50)
        opt=raw_input(" ".center(12))


        if opt in opciones:
            return opt
        else:
            print "Esa opcion no esta disponible!"

def quita_lineas_vacias(ruta):
    """Recibe: cadena Devuelve: nada
    Quita las lineas que esten vacias para mantener el formato de los
    archivos"""
    handler=file
    contenido=[]
    linea=""
    try:
        handler=open(ruta,"r")
        for linea in handler.readlines():
            if linea!="\n": # por si hay lineas en blanco en un archivo
                            #hace que funcione aunque este mal el
                            #formato
                contenido.append(linea)
        handler.close()
        handler=open(ruta,"w")
        handler.write("".join(contenido))
        handler.close()
    except:
        print "[E] Ocurrio algun error, el fichero puede no existir\
o no se tienen los permisos de lectura"

def opcion1(datos_csv,cantidad_lineas,ruta_salida):
    """Llama a las funciones de la opcion elegida"""
    pelicula=""
    mensaje_pelicula="¿De que película? "
    mensaje_escribir_archivo="Si desea guardar los datos en un archivo"\
    " escriba la ruta, de lo contrario presione Enter :"
     
    while len(pelicula)==0:
        pelicula=raw_input(mensaje_pelicula)
        ruta_salida=raw_input(mensaje_escribir_archivo)
        ficha_tecnica(pelicula,datos_csv,cantidad_lineas,ruta_salida)
        raw_input("Presione Enter")
        
def opcion2(datos_csv,cantidad_lineas,ruta_salida):
    """Llama a las funciones de la opcion elegida"""

    actor=""
    mensaje_actor="Ingrese el nombre del actor: "
    mensaje_escribir_archivo="Si desea guardar los datos en un archivo"\
    " escriba la ruta, de lo contrario presione Enter :"
    
    print "Use las mayusculas donde se debe!"
    while len(actor)==0:
        actor=raw_input(mensaje_actor)
    ruta_salida=raw_input(mensaje_escribir_archivo)
    por_actor(actor,datos_csv,cantidad_lineas,ruta_salida)
    raw_input("Presione Enter")
    
def opcion3(datos_csv,cantidad_lineas,ruta_salida):
    """Llama a las funciones de la opcion elegida"""
    paquete=""
    mensaje_cruze="Ingrese un actor y un año/director: "
    mensaje_escribir_archivo="Si desea guardar los datos en un archivo"\
    " escriba la ruta, de lo contrario presione Enter :"
    
    print "El formato es actor,año o actor,director"
    while len(paquete)==0:
        paquete=raw_input(mensaje_cruze)
    ruta_salida=raw_input(mensaje_escribir_archivo)
    cruzar_datos(paquete,datos_csv,cantidad_lineas,ruta_salida)
    raw_input("Presione Enter")

def opcion4(ruta):
    """Llama a las funciones de la opcion elegida"""
    preguntas=["Nombre de la pelicula: ","Año: ","Director: ","Actores [a,b,c,...]:","Genero :"]
    for indice in range(5):
        if indice==0: #para mantener el formato
            datos="\n"+raw_input(preguntas[indice])
        else:
            datos=datos+";"+raw_input(preguntas[indice])
    escribir_archivo(ruta,datos)
    quita_lineas_vacias(ruta)

    print "Hecho!! :D"
    raw_input("Presione Enter")

def main():
    """Recibe: Nada Devuelve:Nada
    Funcion principal, desde donde se llama al resto de las funciones"""
    #varaibles
    ruta=""
    ruta_salida=""
    datos=""
    datos_csv=""
    cantidad_lineas=0
    mensaje_ruta="Ingrese la ruta de la base de datos: "
    datos=False
    ruta_salida=""


    #codigo
    if len(argv)>1: #Verifica si se ingresaron argumentos
        (opciones,args)=argumentos()
        if (opciones.ruta):
            ruta=opciones.ruta
            datos,cantidad_lineas=extraer_datos(ruta,argv)
            datos_csv=csv_reader(datos)
    else:
        while datos==False: #False, por que si hay error la funcion\
                            #extraer_datos devuelve eso
            ruta=raw_input(mensaje_ruta)
            datos,cantidad_lineas=extraer_datos(ruta,argv)
        datos_csv=csv_reader(datos)
    while True:
        rta=menu()
        if rta=="7":
            break #salgo de programa
        
        elif rta=="1": #Ficha tecnica
            opcion1(datos_csv,cantidad_lineas,ruta_salida)
        elif rta=="2": #por actor
            opcion2(datos_csv,cantidad_lineas,ruta_salida)                
            
        elif rta=="3": #Cruzar datos
            opcion3(datos_csv,cantidad_lineas,ruta_salida)
            
        elif rta=="4":#Agregar pelicula
            opcion4(ruta)
            datos,cantidad_lineas=extraer_datos(ruta,argv)

        elif rta=="5":#Reparar archivo
            quita_lineas_vacias(ruta)
            #Releo automaticamente
            datos,cantidad_lineas=extraer_datos(ruta,argv)
            print "Hecho :D"
            raw_input("Presione Enter")

        elif rta == "6": #Releer archivo
            datos,cantidad_lineas=extraer_datos(ruta,argv)
            print "Hecho :D"
            raw_input("Presione Enter")
            
        datos_csv=csv_reader(datos) #Para poder volver a
        pelicula=""                 #recorrer la lista
        actor=""
        paquete=""


#Llamada al main()
main()
