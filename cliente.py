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
            print('Aguardando Dealer...')
            data = sock.recv(BUFFER_SIZE) 
            os.system('cls' if os.name == 'nt' else 'clear')
            dealer = data.decode('utf-8').split('-')
            print('Cartas do Dealer:')
            baralho.imprimirCartas([dealer[0], 'back'])
            print('Suas cartas:')
            baralho.imprimirCartas(dealer)

            

        print ("Finalizando conexão no servidor...") 
        sock.close() 

    except Exception as e: 
        print ("Erro na execução: %s" %str(e)) 

conectar()

