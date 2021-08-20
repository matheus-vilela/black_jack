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

def cartaGrande(carta):
    visual = [
            '  ╔════════════╗',
            f'  ║ {carta:<5}      ║',
            '  ║            ║',
            '  ║            ║',
            f'  ║     {carta[1]:^3}    ║',
            '  ║            ║',
            '  ║            ║',
            '  ║            ║',
            f'  ║      {carta:>5} ║',
            '  ╚════════════╝'
    ]

    return visual

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

def cartaMediaBack():
    visual = [
     '╔══════╗',
     '║░░░░░░║',
     '║░░░░░░║',
     '║░░░░░░║',
     '╚══════╝'
    ],

    return visual

def cartaPequena(carta):
    for nipe in carta:
        visual = [
            '╔════╗',
            f'║ {carta[0]:<2} ║',
            f'║ {nipe:>2} ║',
            '╚════╝'     ]

    return visual
