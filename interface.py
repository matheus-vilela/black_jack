

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
    print('╚════════════════════════════════════════╝\n')   
