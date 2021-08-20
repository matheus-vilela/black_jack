import socket
import numpy as np
import os
from random import *
import baralho

def server():

    HOST = '127.0.0.1' 
    PORT = 8081       
    BUFFER_SIZE = 1024

    server_address = (HOST, PORT)
    sock = socket.socket(socket.AF_INET,  socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 3)
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print ("Iniciando servidor BLACKJACK \nHost: %s  Porta: %s" % server_address)
    sock.bind(server_address)
    sock.listen(3)
    deck = baralho.criar_baralho() 

    client = ['','','']
    address = ['','','']

    i=0
    while i >= 0: 
        print ('Aguardando jogador{} se conectar... '.format(i+1))
        client[i], address[i] = sock.accept() 
        data = client[i].recv(BUFFER_SIZE) 
        jogador = data.decode('utf-8').split('-')
        print("Jogador: {}\nCidade: {}".format(jogador[0], jogador[1]))
        if data:
            carta = baralho.pegarCarta(deck)
            carta2 = baralho.pegarCarta(deck)
            print ('Cartas: {} , {}'.format(carta, carta2))
            client[i].sendall('{}-{}'.format(carta, carta2).encode())
            i+=1
            if i == 3: 
                i = -1
    



server()



