# -*- coding: utf-8 -*-
import sys
import socket
import threading
import select
import string

	
def envia (sock, message, usr): #Enviamos el mensaje recibido por el mensaje a todos los clientes conectados (menos al que lo ha enviado) y lo imprimos por pantalla(la del Servidor incluida)
    for socket in CLIST:
        if socket != server_socket and socket != sock:
            print 'Mensaje recibido: ', message
            socket.send(message)
						
def envia_privat(nomUsuari):
    # Si quiere enviar un mensaje privado a alguien
    sock.send("A quien le quieres enviar el mensaje privado")
    usuarioReceptor = sock.recv (4096, )
    if not usuarioReceptor in usuarisTotal:
        sock.send("Este usuario no existe")
    else:
		  i = 0											
		  for usuario in usuarisTotal:
		      if usuarioReceptor == usuario:
		          break
		      else: 
		          i = i + 1 
		  socketReceptor = CLIST[i+1]
		  sock.send("Introduce el mensaje privado que quieres enviarle")
		  mensajeEmisor = sock.recv(4096, )
		  mensajeTotal = "Mensaje privado enviado por " + nomUsuari + ": " + mensajeEmisor
		  socketReceptor.send(mensajeTotal)

#TODO: Falla cuando es el ultimo cliente que se ha conectado, hacer un if o algo
   

if __name__ == "__main__":

    CLIST=[]  
    canalLista=[]
    usuarisTotal=[]
    usuarisCanal=[]


    print 'Server TCP'

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #creamos socket
    server_socket.bind(('localhost', 6666)) # le damos la ip y el puerto
    server_socket.listen(10) # el numero de clientes que como maximo se conecten
 
    CLIST.append(server_socket) # anadimos a la lista el server_socket
    canalLista.append("General")
    while 1: #mientras que alguien no finalice el Servidor seguira ejecutandose
        
        read_sockets,write_sockets,error_sockets = select.select(CLIST,[],[])

        for sock in read_sockets:

            if sock == server_socket: 
                sockfd, addr = server_socket.accept()			  
                CLIST.append(sockfd)   
#TODO: mirar si existe un usuario con ese nombre
                usuarioCorrecto = 0
                sockfd.send("Que nombre de usuario quiere?")
                while (usuarioCorrecto == 0):
                    nomUsuari = sockfd.recv(4096, )
                    i = [item for item in range(len(usuarisTotal)) if usuarisTotal[item] == nomUsuari]
                    if len(i) == 0 : 
                        usuarioCorrecto = 1 
                    else : 
                        sockfd.send("Este nombre de usuario ya existe, escoja otro") 
                usuarisCanal.append("General")
                usuarisTotal.append(nomUsuari)								                 
                print "Client [%s, %s] conectado" % addr

            else:
                try:
                    data = sock.recv(4096, )            
                except:
                    envia(sock, "Client (%s, %s) esta desconectado" % addr,
                            addr)
                    print "Client (%s, %s) esta desconectado" % addr
                    sock.close()
                    CLIST.remove(sock)
                    continue

                if data:
										#TODO -> Comando privat error
                    indiceNomUsuari = [item for item in range(len(CLIST)) if CLIST[item] == sock ]	
                    nomUsuari = usuarisTotal[indiceNomUsuari[0]-1]
										 #Si el cliente quiere salirse                             
                    if data == "q" or data == "Q":     
                        print "Client (%s, %s) quit" % addr
                        sock.close()                    
                        CLIST.remove(sock)
                    elif data == "help" or data == "Help":
                        envia =  "Todos los comandos\n CREAR: Creara un nuevo canal con el nombre que le indiques, si existia no creara y te contestara diciendo que ya estaba creado. \n CANVIA: El 	    servidor te cambiara de canal, en caso de que no exista el servidor te dira que no existe. \n PRIVAT: Enviara un mensaje privado al usuario que le indiques. \n MOSTRA CANALS: Te enviara la lista de canales que existen en el servidor. \n MOSTRA TOTS: Te enviara una lista de todos los usuarios de todos los canales. \n MOSTRA USUARIS: Te enviará una lista de usuarios del canal actual. \n QUIN CANAL CADA USUARI: Te enviara la lista con cada usuario y al canal al que pertence." 
                        sock.send(envia)			
                    elif data == "PRIVAT":    
												print "Has elegido la comanda privat"      
												envia_privat(nomUsuari)
                    elif data == "MOSTRA CANALS":		
												# Si quiere la lista de todos los canales
                        print "Los canales son: "
                        for i in canalLista:
														sock.send(i)
														sock.send(" ") 
                    elif data == "MOSTRA USUARIS":	
												print "Comanda para enseñar los usuarios del canal actual"
												# Si quiere la lista de usuarios del canal actual
												nomCanal = usuarisCanal[indiceNomUsuari[0]-1]
												i = 0
												for j in usuarisCanal:
													if j == nomCanal:
														sock.send(usuarisTotal[i])	
														sock.send(" ")
													i = i + 1
                    elif data == "QUIN CANAL CADA USUARI":
												j = 0													
												for i in usuarisCanal:
														mensaje = "Usuario " + usuarisTotal[j] + ": " + i + " | "
														sock.send(mensaje)
														sock.send(" ")		
														j = j + 1							                       
                    elif data == "MOSTRA TOTS":
												# Si quiere todos los usuarios de todos los canales
                        sock.send("Los usuarios son: ")													
                        for i in usuarisTotal:
														sock.send(i)
														sock.send(" ")                                
                    elif data == "CANVIA":
												# Si quiere cambiar de canal
												print "Comanda para cambiar de canal"
												sock.send("A que canal te quieres cambiar?")
												nomCanal = sock.recv(4096, )
												if not nomCanal in canalLista:
													sock.send("El nombre del canal no existe, no puede realizarse el cambio") 
												else :
													print usuarisTotal[indiceNomUsuari[0]-1]
													print nomCanal										    		
													usuarisCanal[indiceNomUsuari[0]-1] = nomCanal
													sock.send("Ahora te encuentras en el canal: " + nomCanal )
                    elif data == "CREA":
												# Si quiere crear un canal
                        sock.send("Con que nombre quieres crear el canal?")
                        nomCanal = sock.recv(4096, )
                        #mirar si existe este nombre
                        if nomCanal in canalLista:
														#si existe enviamos un mensaje al usuario diciendo que ya existe
												    sock.send("El nombre del canal ya existe, no se puede crear")
                        else:   
														#si no existe lo añadimos a la lista de nombres y creamos el canal
												    canalLista.append(nomCanal)  
												    i = 0 
												    flag = 0
												    while (flag == 0):
												    	if usuarisTotal[i] == nomUsuari:
												    		usuarisCanal[i] = nomCanal	
												    		flag = 1				
												    	i = i + 1							                                         	
												    sock.send("Has creado el canal: " + nomCanal)																								
                    else:
                        missatge = nomUsuari + ": " + data
                        envia(sock,missatge,addr)                    
                
    server_socket.close()    
