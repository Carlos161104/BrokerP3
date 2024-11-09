from socket import *


def Main():
    host= "localhost" #IP del broker, Rene se la come.
    port= 5000
    address= (host,port)

    mySocket= socket(AF_INET, SOCK_STREAM) #(AF_INET, SOCK_DGRAM) #SOCK_STREAM=TCP, SOCK_DGRAM=UDP
    mySocket.connect(address)

    #Enviar el tipo 1 para el server sepa que soy un cliente
    mySocket.send('2'.encode())
    print("Enviando el tipo ...")