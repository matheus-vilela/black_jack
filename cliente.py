import pickle
import socket, os
import time
import baralho

# HOST = '127.0.0.1' 
# PORT = 8081       
# BUFFER_SIZE = 1024

class Conexao():
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET,  socket.SOCK_STREAM)
        self.host = '127.0.0.1'
        self.port = 8081
        self.buffer = 1024

servers =[]

def conectar(): 

    servers.append(Conexao())
    server = servers[0]

    os.system('cls' if os.name == 'nt' else 'clear')
    print ("Conectando \nHost: %s   Porta: %s" % (server.host, server.port)) 
    server.sock.connect((server.host, server.port)) 
    try: 
        nome = input('\nPara começar, \ninforme o seu nome: ')
        cidade = input('Informe sua cidade: ')
        server.sock.sendall('{}-{}'.format(nome, cidade).encode('utf-8'))
        while True:
            try:
                game(server)
            except Exception as e: 
                print ("Erro na execução: %s" %str(e)) 
                break

        print ("Finalizando conexão no servidor...") 
        server.sock.close() 

    except Exception as e: 
        print ("Erro na execução: %s" %str(e)) 


def game(server):
    opcao = 1
    os.system('cls' if os.name == 'nt' else 'clear')
    print('\nAguardando a partida começar...')
    while True:
        print('\nAguarde...')
        data = server.sock.recv(server.buffer) 
        resposta = pickle.loads(data)
        
        if resposta[0] == 'aposta':
            os.system('cls' if os.name == 'nt' else 'clear')
            baralho.placar(resposta)
            aposta = input("Digite o valor da sua aposta: ")
            stringAposta = pickle.dumps([aposta])
            server.sock.sendall(stringAposta)
       
        elif resposta[0] == 'initial':
            os.system('cls' if os.name == 'nt' else 'clear')
            baralho.placar(resposta)
            print('Cartas do Dealer:')
            baralho.imprimirCartas(resposta[3])
            print('Suas cartas:')
            baralho.imprimirCartas(resposta[4])
            stringAposta = pickle.dumps(['ok'])
            server.sock.sendall(stringAposta)

        elif resposta[0] == 'jogada':
            os.system('cls' if os.name == 'nt' else 'clear')
            baralho.placar(resposta)
            print('Cartas do Dealer:')
            baralho.imprimirCartas(resposta[3])
            print('Suas cartas:')
            baralho.imprimirCartas(resposta[4])
            print('Pontuação: {}'.format(somaCartas(resposta[4])))

            while True:
                opcao = input("\nDigite <1> para pedir uma carta\nDigite <2> para passar\nDigite <3> para pedir uma carta e Dobrar a aposta\n\nDigite sua jogada: ")
                if opcao == '1':
                    stringCartas = pickle.dumps('pedir')
                    server.sock.sendall(stringCartas)
                    break
                
                elif opcao == '2':
                    stringCartas = pickle.dumps('passar')
                    server.sock.sendall(stringCartas)
                    break

                elif opcao == '3':
                    stringCartas = pickle.dumps('dobro')
                    server.sock.sendall(stringCartas)
                    break

                else:
                    print("Opcao invalida")
        
        elif resposta[0] == 'mostrar':
            os.system('cls' if os.name == 'nt' else 'clear')
            print('Cartas do Dealer:')
            baralho.imprimirCartas(resposta[3])
            print('Suas cartas:')
            baralho.imprimirCartas(resposta[4])
            print('Pontuação: {}'.format(somaCartas(resposta[4])))


        elif resposta[0] == 'estourou':
            os.system('cls' if os.name == 'nt' else 'clear')
            print('Suas cartas:')
            baralho.imprimirCartas(resposta[4])
            print('Pontuação: {}'.format(somaCartas(resposta[4])))
            print("\nEstourou, a soma ultrapassa os 21.")

        elif resposta[0] == 'end':
            print('')
            print(resposta[1])
            print(resposta[2])

        elif resposta[0] == 'continue':
            print('\nSalvando partida...')
            print('Iniciando nova rodada...')

        else:
            print(data)


                  
def somaCartas(mao):
    total = 0
    existe = 0
    for card in mao:
        if card[0] == 'K':
            total +=10
        elif card[0]== 'Q':
            total +=10
        elif card[0] == 'J':
            total +=10
        elif card[1] == '0':
            total += 10
        elif card[0] == 'A':
            total +=11
            existe += 1
        else:
            total += int(card[0])

    if existe > 0 and total > 21:
        total -= (10*existe)

    return total



conectar()
