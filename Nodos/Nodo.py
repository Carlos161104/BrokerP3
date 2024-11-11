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
import cv2

def recibir_frames(conn, frames):
    ## Función que maneja la conexión con un cliente.
    ## Recibe: Frames de video desde el cliente.
    ## Retorna: Lista de frames descodificados.
    print("Conectado al servidor")
    while True:
        try:
            frame_size = conn.recv(4)
            if not frame_size:
                break
            frame_size = int.from_bytes(frame_size, byteorder='big')
            frame_data = b''
            while len(frame_data) < frame_size:
                packet = conn.recv(frame_size - len(frame_data))
                if not packet:
                    return None
                frame_data += packet
            frame = cv2.imdecode(frame_data, cv2.IMREAD_COLOR)
            frames.append(frame)
        except Exception as e:
            print(f"Error recibiendo frame: {e}")
            break
    return frames

def Recive_Video(frames):
    host = socket.gethostname(socket.gethostname())
    buff = 1024
    port = 5000
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    
    print(f"Esperando el video en la conexion {host}:{port}...")

    
    while True: 
        conn, addr = server_socket.accept()
        print("Cluster enviando video...")
        
        frames = recibir_frames(conn, frames)
        break;
    server_socket.close()
    return frames  

def Main():
    host= "localhost"
    port= 5000
    address= (host,port)

    mySocket= socket(AF_INET, SOCK_STREAM) #(AF_INET, SOCK_DGRAM) #SOCK_STREAM=TCP, SOCK_DGRAM=UDP
    mySocket.connect(address)

    #Enviar el tipo 1 para el server sepa que soy un cliente
    mySocket.send('2'.encode())
    print("Enviando el tipo ...")
    frames = []
    
    frames = Recive_Video()
    
    #En este punto ua tenemos el arreglo de frames.
    
    