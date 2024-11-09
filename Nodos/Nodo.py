# Pasos a seguir para el nodo
## 1. Conectarse directamente al server y enviar primero el tipo que va a ser 2
## 2. Quedarse en modo servidor 
    ### Aqui se va a resivir primero el indice o numero de segmento y se almacenara en una variable.
    ### Se resivira en sugunda instancia el video.
## 3. Una vez que se reciva el segmento de video se deve cerrar el servidor 
## 4. Con un funcion se trata el video
## 5. Se conectara con el servidor 
    ### Se enviara primero  un tipo 3 para que el server lo trate como el resultado de la chamba
    ### Se envia el numero de segmento 
    ### Se envia el segmento
## 6. Se setean las variables de datos para despues regresar al modo servidor en espera de mas segmentos de video.
from socket import *


def Main():
    host= "localhost"
    port= 5000
    address= (host,port)

    mySocket= socket(AF_INET, SOCK_STREAM) #(AF_INET, SOCK_DGRAM) #SOCK_STREAM=TCP, SOCK_DGRAM=UDP
    mySocket.connect(address)

    #Enviar el tipo 1 para el server sepa que soy un cliente
    mySocket.send('2'.encode())
    print("Enviando el tipo ...")