import socket
import pickle
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


class Server():

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET,  socket.SOCK_STREAM)
        self.host = '127.0.0.1'
        self.port = 8081
        self.buffer = 1024

servers = []

def game():

    servers.append(Server())
    server = servers[0]
    server.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 3)

    os.system('cls' if os.name == 'nt' else 'clear')
    print ("Iniciando servidor BLACKJACK \nHost: %s  Porta: %s" % (server.host, server.port))
    server.sock.bind((server.host, server.port))
    server.sock.listen(3)

    jogadores = []
    banca = []
  
    i=0
    while i < 2: 
        print ('Aguardando jogador{} se conectar... '.format(i+1))
        client, address = server.sock.accept() 
        data = client.recv(server.buffer) 
        jogador = data.decode('utf-8').split('-')
        jogadores.append(Jogador(jogador[0], jogador[1], client, address))
        print("Jogador{} se conectou.\nNome: {}\nCidade: {}".format(i, jogador[0], jogador[1]))
        i+=1
        j=0
        while i >= 2:
            if j == 0:
                deck = baralho.criar_baralho()
                banca.append(Banca())
                banca[j].mao.append(baralho.pegarCarta(deck))
                banca[j].mao.append(baralho.pegarCarta(deck))
                while j < 2:
                    jogadores[j].mao.append(baralho.pegarCarta(deck))
                    jogadores[j].mao.append(baralho.pegarCarta(deck))
                    j+=1

            count = input("Aperte para continuar")
            if i != 2:
                jogadores[i-2].mao.append(baralho.pegarCarta(deck))
            stringCartas = pickle.dumps([[banca[0].mao[0], 'back'],jogadores[i-2].mao])
            jogadores[i-2].client.sendall(stringCartas)
            i+=1
            if i == 4:
                i = 2
    



game()



