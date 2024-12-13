from poderes import usar_poder
from utils import entrada_para_coordenadas

def executar_turno(jogador, tabuleiro_proprio, tabuleiro_oponente, poderes_disponiveis, turnos_temporarios):
    """
    Executa o turno de um jogador.
    Permite atacar, usar um poder ou desistir.
    """
    # Aplica os efeitos temporários antes do turno
    aplicar_efeitos_temporarios(turnos_temporarios, tabuleiro_oponente, jogador)

    print(f"\nTurno do jogador {jogador}:")
    print("1. Atacar")
    print("2. Usar poder")
    print("3. Desistir")

    try:
        escolha = int(input("Escolha uma ação (1-3): "))
        if escolha == 1:
            # Realizar ataque
            entrada = input("Informe a posição para atacar (ex: 'A 14'): ")
            try:
                x, y = entrada_para_coordenadas(entrada)
                resultado = tabuleiro_oponente.atacar(x, y)
                print(f"Resultado do ataque: {resultado}")
            except ValueError as e:
                print(f"Erro: {e}")
        elif escolha == 2:
            # Usar poder
            if not poderes_disponiveis:
                print("Nenhum poder disponível!")
                return "continuar"
            print("\nPoderes disponíveis:")
            for i, poder in enumerate(poderes_disponiveis):
                print(f"{i + 1}. {poder['nome']} (Usos restantes: {poder['usos']})")
            try:
                escolha_poder = int(input("Escolha um poder pelo número: ")) - 1
                if escolha_poder < 0 or escolha_poder >= len(poderes_disponiveis):
                    print("Escolha inválida.")
                    return "continuar"
                poder = poderes_disponiveis[escolha_poder]
                usar_poder(poder, tabuleiro_proprio, tabuleiro_oponente, turnos_temporarios)
                if poder["usos"] == 0:
                    poderes_disponiveis.pop(escolha_poder)  # Remove poder esgotado
            except ValueError:
                print("Entrada inválida.")
        elif escolha == 3:
            print(f"Jogador {jogador} desistiu! O oponente vence.")
            return "desistir"
        else:
            print("Escolha inválida. Perdeu o turno.")
    except ValueError:
        print("Entrada inválida. Perdeu o turno.")

    # Reimprime os tabuleiros após o turno
    print("\nTabuleiro do jogador:")
    tabuleiro_proprio.exibir()
    print("\nTabuleiro do oponente:")
    tabuleiro_oponente.exibir()

    return "continuar"


def atualizar_temporarios(turnos_temporarios):
    """
    Atualiza os efeitos temporários, reduzindo os turnos restantes e removendo os expirados.
    """
    for chave in list(turnos_temporarios.keys()):
        temporarios = turnos_temporarios[chave]
        for efeito in list(temporarios):
            efeito["turnos"] -= 1
            if efeito["turnos"] <= 0:
                temporarios.remove(efeito)
        if not temporarios:
            turnos_temporarios.pop(chave)

def aplicar_efeitos_temporarios(turnos_temporarios, tabuleiro_oponente, jogador):
    """
    Aplica os efeitos temporários ao jogador ou ao tabuleiro oponente.
    """
    for efeito in turnos_temporarios.get("nevoeiro", []):
        if efeito["jogador"] != jogador:
            for x, y in efeito["area"]:
                if tabuleiro_oponente.validar_posicao(x, y):
                    tabuleiro_oponente.matriz[x][y] = "?"
            print(f"Nevoeiro ativo na área: {efeito['area']}")
