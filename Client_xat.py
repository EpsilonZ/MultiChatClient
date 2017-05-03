import socket
import thread
import sys



def recv_data():            #Recibir los datos de los otros clientes conectados al Servidor
    while 1:
        
            recv_data = client_socket.recv(4096)           
            print recv_data

def send_data():                #Enviar la informacion al Servidor
    while 1:
        send_data = str(raw_input())
      	client_socket.send(send_data)
        
if __name__ == "__main__":

    print "Cliente TCP"
    serverPort = int(input("Puerto: ")) #tiene que retornar un entero que sera el puerto con que establezcamos conexion
    serverIP = raw_input("Direccion IP: ") #retorna un string que sera la ip a la que nos conectemos
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #creamos socket
    client_socket.connect((serverIP, serverPort)) #conectamos el socket con la IP y puerto introducidos por el usuario

    thread.start_new_thread(recv_data,()) #creamos un thread para recibir los mensajes
    thread.start_new_thread(send_data,()) #creamos un thread para enviar los mensajes
    print "Si quieres saber todos los comandos que puedes usar, escribe help/Help"
    try: #mientras el usuario no finalice el Cliente se seguira ejecutando
        while 1:
            continue
    except:
        print "Cliente finaliza...." #si entra aqui es que el usuario ha parado el Cliente
        client_socket.close()        #cerramos el Socket
