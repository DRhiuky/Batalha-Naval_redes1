from navio import Navio

def entrada_para_coordenadas(entrada):
    """
    Converte uma entrada como 'A 14' em coordenadas (linha, coluna).
    """
    try:
        linha, coluna = entrada.split()
        x = ord(linha.upper()) - ord('A')  # Converte a letra em índice numérico (A=0, B=1, ...)
        y = int(coluna) - 1  # Ajusta a coluna para índice zero
        return x, y
    except (ValueError, IndexError):
        raise ValueError("Entrada inválida. Use o formato 'A 14'.")


def posicionar_navios(tabuleiro, tipos_navios):
    """
    Função auxiliar para posicionar navios manualmente no tabuleiro de um jogador.
    """
    navios_disponiveis = []
    for nome, tamanho, numero, quantidade in tipos_navios:
        for _ in range(quantidade):
            navios_disponiveis.append(Navio(nome, tamanho, numero))

    while navios_disponiveis:
        print("\nTabuleiro atual:")
        tabuleiro.exibir()
        print("\nNavios disponíveis:")
        for i, navio in enumerate(navios_disponiveis):
            print(f"{i + 1}. {navio.nome} (Tamanho: {navio.tamanho})")
        try:
            escolha = int(input("\nEscolha um navio pelo número: ")) - 1
            if escolha < 0 or escolha >= len(navios_disponiveis):
                print("Escolha inválida.")
                continue
            navio = navios_disponiveis[escolha]
            entrada = input(f"Posicione o {navio.nome} (ex: 'A 14'): ")
            orientacao = input("Escolha a orientação (h para horizontal, v para vertical): ").lower()
            if orientacao not in ["h", "v"]:
                print("Orientação inválida.")
                continue
            x, y = entrada_para_coordenadas(entrada)
            if orientacao == "h":
                posicoes = [(x, y + i) for i in range(navio.tamanho)]
            else:
                posicoes = [(x + i, y) for i in range(navio.tamanho)]
            if tabuleiro.verificar_disponibilidade(posicoes):
                tabuleiro.posicionar_navio(navio, posicoes)
                navios_disponiveis.pop(escolha)
            else:
                print("Posição inválida ou fora dos limites.")
        except ValueError as e:
            print(f"Erro: {e}")
        except IndexError:
            print("Posição fora dos limites.")


