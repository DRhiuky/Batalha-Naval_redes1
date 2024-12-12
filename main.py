from tabuleiro import Tabuleiro
from turnos import executar_turno, atualizar_temporarios
from poderes import atualizar_temporarios, inicializar_poderes
from utils import posicionar_navios

import os

def limpar_terminal():
    """
    Limpa o terminal de acordo com o sistema operacional.
    """
    os.system('cls' if os.name == 'nt' else 'clear')


# Lista de navios com suas quantidades (1 de cada tipo para testes)
tipos_navios = [
    ("Cruzador de Mísseis", 5, 5, 1),
    ("Porta-Aviões", 4, 4, 1),
    ("Contratorpedeiro", 3, 3, 1),
    ("Couraçado", 2, 2, 1),
    ("Submarino", 1, 1, 1)
]

# Configurar tabuleiros para dois jogadores
tabuleiro_jogador1 = Tabuleiro()
tabuleiro_jogador2 = Tabuleiro()

# Posicionar navios para cada jogador
print("\nJogador 1, posicione seus navios:")
posicionar_navios(tabuleiro_jogador1, tipos_navios)

print("\nJogador 2, posicione seus navios:")
posicionar_navios(tabuleiro_jogador2, tipos_navios)

# Inicializar poderes com base nos navios posicionados
poderes_jogador1 = inicializar_poderes(tabuleiro_jogador1.navios, 1)
poderes_jogador2 = inicializar_poderes(tabuleiro_jogador2.navios, 2)

# Inicializa os turnos temporários para efeitos dos poderes
turnos_temporarios = {
    "reconhecimento": [],
    "nevoeiro": [],
    "decoy": []
}

# Loop principal do jogo
jogador_atual = 1
while True:
    # Limpa o terminal
    limpar_terminal()

    # Atualiza os efeitos temporários
    atualizar_temporarios(turnos_temporarios)

    # Executa o turno do jogador atual
    if jogador_atual == 1:
        print("\nJogador 1, seu turno!")
        status = executar_turno(
            jogador=1,
            tabuleiro_proprio=tabuleiro_jogador1,
            tabuleiro_oponente=tabuleiro_jogador2,
            poderes_disponiveis=poderes_jogador1,
            turnos_temporarios=turnos_temporarios
        )
        if status == "desistir":
            print("Jogador 2 vence!")
            break
        # Verificar condição de vitória
        if all(navio.afundado() for navio in tabuleiro_jogador2.navios):
            print("Jogador 1 venceu! Todos os navios do oponente foram destruídos.")
            break
        jogador_atual = 2
    else:
        print("\nJogador 2, seu turno!")
        status = executar_turno(
            jogador=2,
            tabuleiro_proprio=tabuleiro_jogador2,
            tabuleiro_oponente=tabuleiro_jogador1,
            poderes_disponiveis=poderes_jogador2,
            turnos_temporarios=turnos_temporarios
        )
        if status == "desistir":
            print("Jogador 1 vence!")
            break
        # Verificar condição de vitória
        if all(navio.afundado() for navio in tabuleiro_jogador1.navios):
            print("Jogador 2 venceu! Todos os navios do oponente foram destruídos.")
            break
        jogador_atual = 1

print("\nFim do jogo!")

