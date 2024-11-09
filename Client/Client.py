from socket import *
from utils.sendVideo import send_video_to_server

def Main():
    host= "localhost" #IP del broker, Rene se la come.
    port= 5000
    address= (host,port)

    mySocket= socket(AF_INET, SOCK_STREAM) #(AF_INET, SOCK_DGRAM) #SOCK_STREAM=TCP, SOCK_DGRAM=UDP
    mySocket.connect(address)

    #Enviar el tipo 1 para el server sepa que soy un cliente
    mySocket.send('1'.encode())
    print("Enviando el tipo ...")

    #Enviar el video.
    video_path = 'input_video.mp4'
    send_video_to_server(mySocket, video_path)

if __name__ == "__main__":
    Main()