## Inicio do jogo

- Conectar banca
- Conectar jogador 1 passando como parametro: Nome e Cidade
- Conectar jogador 2 passando como parametro: Nome e Cidade

- Servidor cria base de dados: [
  - Nome: Jogador1
  - Cidade: AAAAAAA
  - Cash: 980
  - Aposta: 20
  - Pontuacao: 0
  - Vitorias: 0
  - Mao: [A♠,A♠]
  - MaoCrupie: A♠
  - Jogando: Jogador2

  - Nome: Jogador2
  - Cidade: AAAAAAA
  - Cash: 980
  - Aposta: 20
  - Pontuacao: 0
  - Vitorias: 0
  - Mao: []
  - MaoCrupie: A♠
  - Jogando: Jogador1

  - Nome: Banca
  - Pontuacao: 0
  - Vitorias: 0
  - Mao: [A♠, K♠]
]
  
- Começar rodada de apostas
  - Jogador1 aposta
  - Jogador2 aposta

- Dealer distribui as cartas, salvando na variavel "Mao" e "MaoDealer" do objeto 
  do jogador, e o servidor envia para o jogador equivalente as cartas dele, e a 
  carta à mostra do Dealer.