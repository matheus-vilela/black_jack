import pickle
import socket, os

class Conexao():
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET,  socket.SOCK_STREAM)
        self.host = '127.0.0.1'
        self.port = 8081
        self.buffer = 1024


def conectar(): 
    server = Conexao()
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
                break
            except Exception as e: 
                print ("Erro na execução: %s" %str(e)) 
                break

        print ("Finalizando conexão com o servidor...") 
        server.sock.close() 

    except Exception as e: 
        print ("Erro na execução: %s" %str(e)) 


def game(server):
    os.system('cls' if os.name == 'nt' else 'clear')
    print('\nAguardando a partida começar...')
    x=0
    while True:
        if x!=0:
            print('\nAguardando os outros jogadores...')
        data = server.sock.recv(server.buffer) 
        resposta = pickle.loads(data)
        x=1
        if resposta[0] == 'aposta':
            os.system('cls' if os.name == 'nt' else 'clear')
            placar(resposta)
            while True:
                try:
                    aposta = int(input("Digite o valor da sua aposta: "))
                    if aposta > 0 and aposta <= resposta[1]:
                        stringAposta = pickle.dumps([aposta])
                        server.sock.sendall(stringAposta)
                        break
                    elif aposta > resposta[1]:
                        print('Aposta superior ao total disponivel.\nSaldo disponivel: {}'.format(resposta[1]))
                    else: 
                        print('Aposta inválida')
                except Exception as e: 
                    print('Aposta inválida')
       
        elif resposta[0] == 'initial':
            os.system('cls' if os.name == 'nt' else 'clear')
            placar(resposta)
            print('Cartas da Banca:')
            imprimirCartas(resposta[3])
            print('Suas cartas:')
            imprimirCartas(resposta[4])
            stringAposta = pickle.dumps(['ok'])
            server.sock.sendall(stringAposta)

        elif resposta[0] == 'jogada':
            os.system('cls' if os.name == 'nt' else 'clear')
            placar(resposta)
            print('Cartas da Banca:')
            imprimirCartas(resposta[3])
            print('Suas cartas:')
            imprimirCartas(resposta[4])
            print('Pontuação: {}'.format(somaCartas(resposta[4])))


            if len(resposta[4]) > 2:
                while True:
                    opcao = input("\nDigite <1> para pedir uma carta\nDigite <2> para passar\n\nDigite sua jogada: ")
                    if opcao == '1':
                        stringCartas = pickle.dumps('pedir')
                        server.sock.sendall(stringCartas)
                        break
                    
                    elif opcao == '2':
                        stringCartas = pickle.dumps('passar')
                        server.sock.sendall(stringCartas)
                        break

                    else:
                        print("Opcao invalida")
            else:
                while True:
                    opcao = input("\nDigite <1> para pedir uma carta\nDigite <2> para continuar\nDigite <3> para correr\n\nDigite sua jogada: ")
                    if opcao == '1':
                        stringCartas = pickle.dumps('pedir')
                        server.sock.sendall(stringCartas)
                        break
                    
                    elif opcao == '2':
                        stringCartas = pickle.dumps('passar')
                        server.sock.sendall(stringCartas)
                        break

                    elif opcao == '3':
                        stringCartas = pickle.dumps('correr')
                        server.sock.sendall(stringCartas)
                        break

                    else:
                        print("Opcao invalida")
        
        elif resposta[0] == 'mostrar':
            os.system('cls' if os.name == 'nt' else 'clear')
            placar(resposta)
            print('Cartas da Banca:')
            imprimirCartas(resposta[3])
            print('Suas cartas:')
            imprimirCartas(resposta[4])
            print('Pontuação: {}'.format(somaCartas(resposta[4])))

        elif resposta[0] == 'estourou':
            os.system('cls' if os.name == 'nt' else 'clear')
            placar(resposta)
            print('Suas cartas:')
            imprimirCartas(resposta[4])
            print('Pontuação: {}'.format(somaCartas(resposta[4])))
            print("\nEstourou, a soma ultrapassa os 21.")

        elif resposta[0] == 'end':
            os.system('cls' if os.name == 'nt' else 'clear')
            print('')
            print(resposta[1])
            print(resposta[2])
            if len(resposta) >3:
                print('\nCartas: ')
                imprimirCartas(resposta[3])
            print('\nSalvando partida...')
        
        elif resposta[0] == 'vitoria':
            os.system('cls' if os.name == 'nt' else 'clear')
            print('\nFIM DE JOGO')
            print(resposta[1])
            print(resposta[2])
            if len(resposta) >3:
                print('\nCartas: ')
                imprimirCartas(resposta[3])
            print('\nSalvando partida...')
            print('Finalizando game...')
            return

        else:
            break

                  
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

def imprimirCartas(cartas):
    lista = [cartaBaralho(carta) for carta in cartas]
    for card in zip(*lista):
            print('   '.join(card))

def cartaBaralho(carta):
    if carta == "back":
        visual = [
            '╔══════╗',
            '║░░░░░░║',
            '║░░░░░░║',
            '║░░░░░░║',
            '╚══════╝'
            ]
        return visual
    else:
        visual = [
            '╔══════╗',
            f'║ {carta:<3}  ║',
            f'║      ║',
            f'║  {carta:>3} ║',
            '╚══════╝'
            ]
        return visual

def placar(dados):
    if dados[10] == 0:
        print('\nO jogador {} zerou suas fichas'.format(dados[5]))
        print('Se perder essa rodada será eliminado\n')
    if dados[11] == 0:
        print('\nO jogador {} zerou suas fichas'.format(dados[7]))
        print('Se perder essa rodada está eliminado\n')

    print('╔══════════════════════════════════════════╗')
    print('  {} - vitorias: {}'.format(dados[5], dados[6]))
    print('  {} - vitorias: {}'.format(dados[7], dados[8]))
    print('  Banca - vitorias: {}'.format(dados[9]))
    print('╔══════════════════════════════════════════╗')
    print('  Total em fichas {} - Aposta atual: {}   '.format(dados[1], dados[2]))
    print('╚══════════════════════════════════════════╝\n')   


conectar()
