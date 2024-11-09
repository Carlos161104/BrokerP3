import pickle
import cv2
import threading
import socket

def create_video_from_frames(frames, output_path, fps=30):
    ## Funcion que crea un video a partir de frames individuales
    ## Resive: Los frames procesados por los nodos y el cliente
    ## Envia: Un archivo de video en formato mp4
    if frames:
        height, width, layers = frames[0].shape
        size = (width, height)
        out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, size)
        for frame in frames:
            out.write(frame)
        out.release()

def send_video_to_client(conn, video_path):
    ## Funcion para enviar el video final al cliente
    ## Resive: La conexion del cliente y la ruta del video
    ## Envia: Los datos del video en fragmentos de 1024 bytes
    with open(video_path, 'rb') as video_file:
        while True:
            video_data = video_file.read(1024)
            if not video_data:
                break
            conn.sendall(video_data)

def is_node(ip_nodes, addr):
    ## Funcion que registra un nuevo nodo en el sistema
    ## Resive: La direccion IP del nodo que se conecta
    ## Retorna: Lista actualizada de IPs de nodos
    print('Se conecto un nodo desde la ip:', addr)
    ip_nodes.append(addr)
    return ip_nodes

def is_client(addr, conn):
    ## Funcion que maneja la conexion con un cliente
    ## Resive: Frames de video desde el cliente
    ## Retorna: Lista de frames descodificados
    print(f"Cliente conectado con {addr}")
    frames = []
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
            print(f"Error resiviendo frame: {e}")
            break
    return frames

def result_video(video_final, conn):
    ## Funcion que prosesa los frames resividos de los nodos
    ## Resive: Frames procesados desde los nodos
    ## Retorna: Lista actualizada con los segmentos de video
    try:
        num_segmento = int(conn.recv(4).decode())
        arreglo_basico = []
        while True:
            frame_size_data = conn.recv(4)
            if not frame_size_data:
                break
            frame_size = int.from_bytes(frame_size_data, byteorder='big')
            frame_data = b''
            while len(frame_data) < frame_size:
                packet = conn.recv(frame_size - len(frame_data))
                if not packet:
                    break
                frame_data += packet
            frame = pickle.loads(frame_data)
            arreglo_basico.append(frame)
        video_final[num_segmento] = arreglo_basico
    except Exception as e:
        print(f"Error resiviendo video: {e}")
    return video_final

def handle_connection(conn, addr, video_final, ips_nodes, lock):
    ## Funcion principal que maneja las conexiones entrantes
    ## Identifica el tipo de conexion (cliente o nodo) y prosesa segun corresponda
    ## Resive: Conexion entrante y datos necesarios para el prosesamiento
    tipo = conn.recv(1024).decode()
    if tipo == '1':
        #Quiere decir que es un cliente que envia frames
        frames = is_client(addr, conn)
        if frames:
            video_final[0] = frames  # Cliente manda frames completos en el segmento 0
    elif tipo == '2':
        with lock:
            ips_nodes = is_node(ips_nodes, addr)
            video_final.extend([None] * len(ips_nodes))
    elif tipo == '3':
        with lock:
            video_final = result_video(video_final, conn)

    # Verificar si todos los frames estan completos
    with lock:
        if all(segment is not None for segment in video_final):
            create_video_from_frames([frame for segment in video_final for frame in segment], 'output_video.mp4')
            send_video_to_client(conn, 'output_video.mp4')

if __name__ == "__main__":
    # Configuracion inicial del servidor
    buff = 1024
    host = 'localhost'
    port = 12345

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)

    print(f"Servidor central esperando conexiones en {host}:{port}...")

    ips_nodes = []  # Lista para almasenar las IPs de los clientes
    video_final = []
    lock = threading.Lock()  # Lock para manejo seguro de concurrensia en listas

    while True:
        conn, addr = server_socket.accept()
        threading.Thread(target=handle_connection, args=(conn, addr, video_final, ips_nodes, lock)).start()
        