import pickle
import socket, os
import time
import baralho

HOST = '127.0.0.1' 
PORT = 8081       
BUFFER_SIZE = 1024

def conectar(): 
    server_address = (HOST, PORT)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

    os.system('cls' if os.name == 'nt' else 'clear')
    print ("Conectando \nHost: %s   Porta: %s" % server_address) 
    sock.connect(server_address) 
    try: 
        nome = input('\nPara começar, \ninforme o seu nome: ')
        cidade = input('Informe sua cidade: ')
        sock.sendall('{}-{}'.format(nome, cidade).encode('utf-8'))
        while True:
            try:
                print('Aguardando Dealer...')
                data = sock.recv(BUFFER_SIZE) 
                os.system('cls' if os.name == 'nt' else 'clear')
                dealer = pickle.loads(data)
                print('Cartas do Dealer:')
                baralho.imprimirCartas(dealer[0])
                print('Suas cartas:')
                baralho.imprimirCartas(dealer[1])
            
            except Exception as e: 
                print ("Erro na execução: %s" %str(e)) 
                break

        print ("Finalizando conexão no servidor...") 
        sock.close() 

    except Exception as e: 
        print ("Erro na execução: %s" %str(e)) 

conectar()

