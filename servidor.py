import socket
import pickle
import time
import os
from random import *
import baralho

class Jogador:
    def __init__(self, nome, cidade, client, address):
        self.nome = nome
        self.cidade = cidade
        self.client = client
        self.address = address
        self.saldo = 1000
        self.aposta = 0
        self.pontuacao = 0
        self.vitorias = 0
        self.mao = []

class Banca:
    def __init__(self):
        self.pontuacao = 0
        self.vitorias = 0
        self.mao = []
        self.totalApostas = 0   

class Server():
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET,  socket.SOCK_STREAM)
        self.host = '127.0.0.1'
        self.port = 8081
        self.buffer = 1024

class Partida():
    def __init__(self):
        self.rodada = 0

servers = []

def init():
    servers.append(Server())
    server = servers[0]
    server.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 3)

    os.system('cls' if os.name == 'nt' else 'clear')
    print ("Iniciando servidor BLACKJACK \nHost: %s  Porta: %s" % (server.host, server.port))
    server.sock.bind((server.host, server.port))
    server.sock.listen(3)

    jogadores = []
    
    banca = []
    banca.append(Banca())
    i=0
    while i < 2: 
        print ('\nAguardando jogador{} se conectar... '.format(i+1))
        client, address = server.sock.accept() 
        data = client.recv(server.buffer) 
        jogador = data.decode('utf-8').split('-')

        jogadores.append(Jogador(jogador[0], jogador[1], client, address))
        
        print("Jogador{} se conectou.\nNome: {}\nCidade: {}".format(i+1, jogador[0], jogador[1]))
        i+=1
        while i >= 2:
            game(jogadores, banca, server)


def game(jogadores, banca,server):
    rodada = 'aposta'
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\nIniciando partida...")
    while True:
        if rodada == 'aposta':
            i = 0
            print("\nRodada de apostas")
            while i < 2:
                jogadores[i].aposta = 0
                dados = enviarDados('aposta', jogadores, banca, i)
                jogadores[i].client.sendall(dados)
                data = jogadores[i].client.recv(server.buffer)
                resposta = pickle.loads(data)
                print("Jogador: {} == apostou: {}".format(jogadores[i].nome, resposta[0]))
                jogadores[i].aposta = int(resposta[0])
                jogadores[i].saldo -= jogadores[i].aposta 
                i+=1
                if i==2:
                    rodada = 'initial'

        elif rodada == 'initial':
            i=0
            deck = baralho.criar_baralho()
            banca[i].mao = []
            banca[i].mao.append(baralho.pegarCarta(deck))
            banca[i].mao.append(baralho.pegarCarta(deck))
            print("\nDistribuindo cartas")
            while i < 2:
                jogadores[i].mao = []
                jogadores[i].mao.append(baralho.pegarCarta(deck))
                jogadores[i].mao.append(baralho.pegarCarta(deck))
                dados = enviarDados('initial', jogadores, banca, i)
                             
                jogadores[i].client.sendall(dados)
                print("Jogador: {}  \ncartas: {}  \npontos: {}\n".format(jogadores[i].nome, jogadores[i].mao, somaCartas(jogadores[i].mao)))
                data = jogadores[i].client.recv(server.buffer)
                i+=1
                if i==2:
                    rodada = 'jogada'

        elif rodada == 'jogada':
            i=0
            j=0
            while i < 2:
                if j==0:
                    print("\nAguardando a jogada de {}\n".format(jogadores[i].nome)) 
                    j+=1
                
                dados = enviarDados('jogada', jogadores, banca, i)
                jogadores[i].client.sendall(dados)

                data = jogadores[i].client.recv(server.buffer)
                resposta = pickle.loads(data)

                if resposta == 'passar':
                    print("{} passou.  \nCartas: {}\nTotal de pontos: {} \naposta: {}".format(jogadores[i].nome,jogadores[i].mao, somaCartas(jogadores[i].mao),jogadores[i].aposta)) 
                    i+=1
                    if i == 2:
                        rodada = 'banca'
                    else: 
                        j=0

                elif resposta == 'pedir':
                    jogadores[i].mao.append(baralho.pegarCarta(deck))
                    if int(somaCartas(jogadores[i].mao)) > 21:
                        dados = enviarDados('estourou', jogadores, banca, i)
                        jogadores[i].client.sendall(dados)
                        print("{} estourou. \nCartas: {}\nTotal de pontos: {} \naposta: {}".format(jogadores[i].nome,jogadores[i].mao ,somaCartas(jogadores[i].mao),jogadores[i].aposta)) 
                        i+=1
                        if i == 2:
                            rodada = 'banca'
                        else: 
                            j=0
                    else:
                        print("{} pediu mais uma carta. \nCartas: {}\nTotal de pontos: {} \naposta: {}".format(jogadores[i].nome,jogadores[i].mao ,somaCartas(jogadores[i].mao),jogadores[i].aposta)) 

                elif resposta == 'dobro':
                    jogadores[i].saldo -= jogadores[i].aposta
                    jogadores[i].aposta = jogadores[i].aposta * 2
                    jogadores[i].mao.append(baralho.pegarCarta(deck))
                    dados = enviarDados('mostrar', jogadores, banca, i)
                    jogadores[i].client.sendall(dados)
                    print("{} dobrou.  \nCartas: {}\nTotal de pontos: {} \naposta: {}".format(jogadores[i].nome,jogadores[i].mao, somaCartas(jogadores[i].mao),jogadores[i].aposta)) 
                    i+=1
                    if i == 2:
                        rodada = 'banca'
                    else: 
                        j=0
        
        elif rodada == 'banca':
           
            jog1 = int(somaCartas(jogadores[0].mao))
            jog2 = int(somaCartas(jogadores[1].mao))

            if jog1 > 21 and jog2 > 21:
                banca[0].vitorias += 1
                i=0
                while i<2:
                    dados = pickle.dumps(['end','Banca','\nA banca ganhou - ambos jogadores estouraram\n'])
                    jogadores[i].client.sendall(dados)

                    i+=1
                    if i== 2:
                        input("Digite para continuar")
                        rodada = 'aposta'
            
            else:
                if somaCartas(banca[0].mao) < 17:
                    while somaCartas(banca[0].mao) < 17:
                        banca[0].mao.append(baralho.pegarCarta(deck))
                
                i=0
                while i<2:
                    dados = verificarGanhador(jogadores, banca)
                    jogadores[i].client.sendall(dados)

                    i+=1
                    if i== 2:
                        input("Digite para continuar")
                        rodada = 'aposta'

        
        elif rodada == 'continue':
            i=0
            while i<2:
                dados = enviarDados('continue', jogadores, banca, i)
                jogadores[i].client.sendall(dados)
                i+=1
                if i==2:
                    time.sleep("Contabilizando valores, e iniciando nova rodada")

            

        elif rodada == 'end':
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
    
def enviarDados(tipo, jogadores, banca, i):
    if banca[0].mao != []:
        return  pickle.dumps([tipo, jogadores[i].saldo,jogadores[i].aposta,[banca[0].mao[0], 'back'],jogadores[i].mao,jogadores[0].nome, jogadores[0].vitorias, jogadores[1].nome, jogadores[1].vitorias, banca[0].vitorias])           
    else:
        return  pickle.dumps([tipo, jogadores[i].saldo,jogadores[i].aposta,['back', 'back'],jogadores[i].mao,jogadores[0].nome, jogadores[0].vitorias, jogadores[1].nome, jogadores[1].vitorias, banca[0].vitorias])           

def verificarGanhador(jogadores, banca):

    banc = int(somaCartas(banca[0].mao))
    bjBanc = 0
    jog1 = int(somaCartas(jogadores[0].mao))
    bjJog1 = 0
    jog2 = int(somaCartas(jogadores[1].mao))
    bjJog2 = 0
    print('\nPontuação final:')
    print('Banca: {}'.format(banc))
    print('{}: {}'.format(jogadores[0].nome,jog1))
    print('{}: {}'.format(jogadores[1].nome,jog2))
    print(jogadores[1].mao[1][0])

    if banc == 21 and len(banca[0].mao) == 2:
         if banca[0].mao[0][0] == ('A' or 'J'):
            if banca[0].mao[1][0] == ('A' or 'J'):
                bjBanc += 1 
    if jog1 == 21 and len(jogadores[0].mao) == 2:
        if (jogadores[0].mao[0])[0] ==( 'A' or 'J'):
            if jogadores[0].mao[1][0] == ('A' or 'J'):
                bjJog1 += 1 
    if jog2 == 21 and len(jogadores[1].mao) == 2:
        if jogadores[1].mao[0][0] == ('A' or 'J'):
            if jogadores[1].mao[1][0] == ('A' or 'J'):
                bjJog2 += 1 
   
    print('\n\nAqui chegou  {}  {}  {}'.format(bjBanc,bjJog1,bjJog2))
    
    if bjBanc > 0 and bjJog1 == 0 and bjJog2 == 0:
        banca[0].vitorias +=1
        print('Teste 1')
        return pickle.dumps(['end', 'Banca', 'A banca venceu com um BlackJack!!'])
    
    elif bjBanc == 0 and bjJog1 > 0 and bjJog2 == 0:
        jogadores[0].vitorias += 1
        jogadores[0].saldo +=(jogadores[0].aposta*2)
        print('Teste 2')
        return pickle.dumps(['end', 'Jogador1', 'O jogador {} venceu com um BlackJack!!'.format(jogadores[0].nome)])
    
    elif bjBanc == 0 and bjJog1 == 0 and bjJog2 > 0:
        jogadores[1].vitorias +=1
        jogadores[1].saldo +=(jogadores[1].aposta*2)
        print('Teste 3')
        return pickle.dumps(['end', 'Jogador2', 'O jogador {} venceu com um BlackJack!!'.format(jogadores[1].nome)])

    elif bjBanc > 0 and bjJog1 == 0 and bjJog2 > 0:
        jogadores[1].saldo += jogadores[1].aposta

        print('Teste 4')
        return pickle.dumps(['end', 'Empate', 'A banca e o jogador {} empataram com um BlackJack!!'.format(jogadores[1].nome)])

    elif bjBanc > 0 and bjJog1 > 0 and bjJog2 == 0:
        jogadores[0].saldo += jogadores[0].aposta
        print('Teste 5')
        return pickle.dumps(['end', 'Empate', 'A banca e o jogador {} empataram com um BlackJack!!'.format(jogadores[0].nome)])

    elif bjBanc == 0 and bjJog1 > 0 and bjJog2 > 0:
        jogadores[1].saldo += jogadores[1].aposta
        jogadores[0].saldo += jogadores[0].aposta
        print('Teste 6')
        return pickle.dumps(['end', 'Empate', 'O jogador {} e o jogador {} empataram com um BlackJack!!'.format(jogadores[0].nome,jogadores[1].nome)])
    
    elif bjBanc > 0 and bjJog1 > 0 and bjJog2 > 0:
        jogadores[1].saldo += jogadores[1].aposta
        jogadores[0].saldo += jogadores[0].aposta
        print('Teste 7')
        return pickle.dumps(['end', 'Empate', 'Todos os jogares empataram com um BlackJack'.format(jogadores[1].nome)])

    
    if jog1 > 21:
        if jog2 > banc and jog2 <= 21:
            jogadores[1].vitorias +=1
            jogadores[1].saldo +=(jogadores[1].aposta*2)

            print('Teste 8')
            return pickle.dumps(['end', 'Jogador2', 'Jogador {} ganhou a rodada com {}'.format(jogadores[1].nome, jog2)]) 
        elif banc > 21 and jog2 <=21:
            jogadores[1].vitorias +=1
            jogadores[1].saldo +=(jogadores[1].aposta*2)
            print('Teste 12a')
            return pickle.dumps(['end', 'Jogador2', 'Jogador {} ganhou a rodada com {}'.format(jogadores[1].nome, jog2)])     
        elif banc > jog2 and banc <=21:
            banca[0].vitorias +=1
            print('Teste 9')
            return pickle.dumps(['end', 'Banca', 'A banca ganhou a rodada com {}'.format(banc)]) 

        elif jog2 > 21:
            banca[0].vitorias +=1
            print('Teste 10')
            return pickle.dumps(['end', 'Banca', 'A banca ganhou a rodada pois ambos jogadores estouraram']) 

        elif jog2 == banc and jog2 <= 21:
            jogadores[1].saldo += jogadores[1].aposta

            print('Teste 11')
            return pickle.dumps(['end', 'Empate', 'A banca e o jogador {} fizeram a mesma quantidade de pontos'.format(jogadores[1].nome)])

    elif jog2 > 21:
        if jog1 > banc and jog1 <= 21:
            jogadores[0].vitorias +=1
            jogadores[0].saldo +=(jogadores[0].aposta*2)
            print('Teste 12')
            return pickle.dumps(['end', 'Jogador1', 'Jogador {} ganhou a rodada com {}'.format(jogadores[0].nome, jog1)]) 
        elif banc > 21 and jog1 <=21:
            jogadores[0].vitorias +=1
            jogadores[0].saldo +=(jogadores[0].aposta*2)
            print('Teste 12a')
            return pickle.dumps(['end', 'Jogador1', 'Jogador {} ganhou a rodada com {}'.format(jogadores[0].nome, jog1)]) 
        

        elif banc > jog1 and banc <=21:
            banca[0].vitorias +=1
            print('Teste 13')
            return pickle.dumps(['end', 'Banca', 'A banca ganhou a rodada com {}'.format(banc)]) 

        elif jog1 > 21:
            banca[0].vitorias +=1
            print('Teste 14')
            return pickle.dumps(['end', 'Banca', 'A banca ganhou a rodada pois ambos jogadores estouraram']) 

        elif jog1 == banc and jog1 <= 21:
            jogadores[0].saldo += jogadores[0].aposta
            print('Teste 15')
            return pickle.dumps(['end', 'Empate', 'A banca e o jogador {} fizeram a mesma quantidade de pontos'.format(jogadores[0].nome)])
    elif banc > 21:
        if jog1 > jog2:
            jogadores[0].saldo += jogadores[0].aposta*2
            jogadores[0].vitorias +=1
            print('Teste 16')
            return pickle.dumps(['end', 'Jogador1', 'O jogador {} ganhou.'.format(jogadores[0].nome)])

        elif jog2 > jog1:
            jogadores[1].saldo += jogadores[1].aposta
            jogadores[1].vitorias +=1

            print('Teste 17')
            return pickle.dumps(['end', 'Jogador2', 'O jogador {} ganhou.'.format(jogadores[1].nome)])

    elif jog1 == jog2:
        if jog1 >= banc:
            jogadores[0].saldo += jogadores[0].aposta
            jogadores[1].saldo += jogadores[1].aposta
            print('Teste 18')
            return pickle.dumps(['end', 'Empate', 'Ambos jogadores pontuaram igual e marcaram mais pontos que a banca'])
        elif banc > jog1:
            print('Teste 19')
            return pickle.dumps(['end','Banca', 'A banca ganhou'])
    
    elif jog1 > jog2 and jog1 > banc:
        jogadores[0].vitorias +=1
        jogadores[0].saldo += (jogadores[0].aposta*2)
        print('Teste 20')
        return pickle.dumps(['end', 'Jogador1', 'O jogador {} ganhou com {} pontos'.format(jogadores[0].nome, jog1)])
    elif jog2 > jog1 and jog2 > banc:
        jogadores[1].vitorias +=1
        jogadores[1].saldo += (jogadores[1].aposta*2)
        print('Teste 21')
        return pickle.dumps(['end', 'Jogador2', 'O jogador {} ganhou com {} pontos'.format(jogadores[1].nome, jog2)])
    elif banc > jog1 and banc > jog2:
        print('Teste 22')
        return pickle.dumps(['end', 'Banca', 'A banca ganhou com {} pontos'.format(banc)])

    else:
         print('Teste 23')
         return pickle.dumps(['end', 'INDECISO', 'NAO ENCONTROU NENHUM IF'])
    print('FIM D OVERIFICADOR')


init()



