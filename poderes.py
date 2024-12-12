from utils import entrada_para_coordenadas

def usar_poder(poder, tabuleiro_proprio, tabuleiro_oponente, turnos_temporarios):
    """
    Executa o poder selecionado.
    """
    if poder["tipo"] == "bombardeio":
        entrada = input("Informe o centro do bombardeio (ex: 'C 10'): ")
        x, y = entrada_para_coordenadas(entrada)
        for i in range(-1, 2):
            for j in range(-1, 2):
                tabuleiro_oponente.atacar(x + i, y + j)
        print("Bombardeio executado!")

    elif poder["tipo"] == "reconhecimento":
        entrada = input("Informe o centro da área para reconhecimento (ex: 'E 8'): ")
        x, y = entrada_para_coordenadas(entrada)
        area = [(x + i, y + j) for i in range(-1, 2) for j in range(-1, 2)]
        turnos_temporarios["reconhecimento"].append({"jogador": poder["jogador"], "area": area, "turnos": 3})
        print("Reconhecimento ativado!")

    elif poder["tipo"] == "nevoeiro":
        entrada = input("Informe o centro do nevoeiro (ex: 'G 4'): ")
        x, y = entrada_para_coordenadas(entrada)
        area = [(x + i, y + j) for i in range(-2, 2) for j in range(-2, 2)]
        turnos_temporarios["nevoeiro"].append({"jogador": poder["jogador"], "area": area, "turnos": 3})
        print("Nevoeiro ativado!")

    elif poder["tipo"] == "decoy":
        entrada = input("Informe o centro do decoy (ex: 'B 7'): ")
        x, y = entrada_para_coordenadas(entrada)
        tabuleiro_proprio.matriz[x][y] = "D"  # D para Decoy
        turnos_temporarios["decoy"].append({"jogador": poder["jogador"], "posicao": (x, y), "turnos": 5})
        print("Decoy criado!")

    elif poder["tipo"] == "sonar":
        direcao = input("Escolha uma linha (A-X) ou coluna (1-24) para o sonar: ")
        if direcao.isdigit():
            coluna = int(direcao) - 1
            for x in range(tabuleiro_oponente.tamanho):
                print(tabuleiro_oponente.matriz[x][coluna])
        else:
            linha = ord(direcao.upper()) - ord("A")
            print(tabuleiro_oponente.matriz[linha])

    poder["usos"] -= 1

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

def inicializar_poderes(navios, jogador_id):
    """
    Inicializa os poderes com a quantidade de usos igual ao número de navios do tipo correspondente.
    """
    tipos_poderes = {
        "Cruzador de Mísseis": "bombardeio",
        "Porta-Aviões": "reconhecimento",
        "Contratorpedeiro": "nevoeiro",
        "Couraçado": "decoy",
        "Submarino": "sonar",
    }

    poderes = []
    for navio in navios:
        if navio.nome in tipos_poderes:
            poder = {
                "nome": navio.nome,
                "tipo": tipos_poderes[navio.nome],
                "usos": sum(1 for n in navios if n.nome == navio.nome),
                "jogador": jogador_id,
            }
            if poder not in poderes:  # Evita duplicatas para o mesmo tipo de poder
                poderes.append(poder)

    return poderes
