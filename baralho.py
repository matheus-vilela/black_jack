import random

def criar_baralho():
    cartas = ["A", "2", "3", "4", "5", "6",
              "7", "8", "9", "10", "Q", "J",
              "K"]
    nipes = ["♣", "♦", "♥", "♠"]

    baralho = []
    for nipe in nipes:
        for carta in cartas:
            baralho.append("{}{}".format(carta, nipe))
    return baralho

def embaralhar(baralho):
    baralho = random.shuffle(baralho)

def pegarCarta(baralho):
    embaralhar(baralho)
    return baralho.pop(0)

def imprimirCartas(cartas):
    lista = [cartaMedia(carta) for carta in cartas]
    for card in zip(*lista):
            print('   '.join(card))

def cartaMedia(carta):
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
    print('╔════════════════════════════════════════╗')
    print('  {} - vitorias: {}'.format(dados[5], dados[6]))
    print('  {} - vitorias: {}'.format(dados[7], dados[8]))
    print('  Banca - vitorias: {}'.format(dados[9]))
    print('╔════════════════════════════════════════╗')
    print('  Total em fichas {} - Aposta atual: {}   '.format(dados[1], dados[2]))
    print('╚════════════════════════════════════════╝')   
