from utils import entrada_para_coordenadas

def poder_bombardeio(poder, tabuleiro_oponente, turnos_temporarios):
    """
    Executa o poder de bombardeio, que ataca uma área 3x3 no tabuleiro oponente.
    """
    entrada = input("Informe o centro do bombardeio (ex: 'C 10'): ")
    x, y = entrada_para_coordenadas(entrada)
    for i in range(-1, 2):
        for j in range(-1, 2):
            tabuleiro_oponente.atacar(x + i, y + j)
    print("Bombardeio executado!")

def poder_reconhecimento(poder, tabuleiro_oponente, turnos_temporarios):
    """
    Executa o poder de reconhecimento, que revela uma área 3x3 no tabuleiro oponente por 3 turnos.
    """
    entrada = input("Informe o centro da área para reconhecimento (ex: 'E 8'): ")
    x, y = entrada_para_coordenadas(entrada)
    if "reconhecimento" not in turnos_temporarios:
        turnos_temporarios["reconhecimento"] = []
    area = [(x + i, y + j) for i in range(-1, 2) for j in range(-1, 2)]
    turnos_temporarios["reconhecimento"].append({"jogador": poder["jogador"], "area": area, "turnos": 3})
    print("Reconhecimento ativado!")

def poder_nevoeiro(poder, tabuleiro_proprio, turnos_temporarios):
    """
    Executa o poder de nevoeiro, que esconde uma área 4x4 no próprio tabuleiro por 3 turnos.
    """
    entrada = input("Informe o centro do nevoeiro (ex: 'G 4'): ")
    x, y = entrada_para_coordenadas(entrada)
    if "nevoeiro" not in turnos_temporarios:
        turnos_temporarios["nevoeiro"] = []
    area = [(x + i, y + j) for i in range(-2, 2) for j in range(-2, 2)]
    turnos_temporarios["nevoeiro"].append({"jogador": poder["jogador"], "area": area, "turnos": 3})
    print("Nevoeiro ativado!")

def poder_decoy(poder, tabuleiro_proprio, turnos_temporarios):
    """
    Executa o poder de decoy, que cria um navio falso por 5 turnos.
    """
    entrada = input("Informe o centro do decoy (ex: 'B 7'): ")
    x, y = entrada_para_coordenadas(entrada)
    if "decoy" not in turnos_temporarios:
        turnos_temporarios["decoy"] = []
    tabuleiro_proprio.matriz[x][y] = "D"  # D para Decoy
    turnos_temporarios["decoy"].append({"jogador": poder["jogador"], "posicao": (x, y), "turnos": 5})
    print("Decoy criado!")

def poder_sonar(poder, tabuleiro_oponente):
    """
    Executa o poder de sonar, que revela navios em uma linha ou coluna.
    """
    direcao = input("Escolha uma linha (A-X) ou coluna (1-24) para o sonar: ")
    if direcao.isdigit():
        coluna = int(direcao) - 1
        for x in range(tabuleiro_oponente.tamanho):
            print(tabuleiro_oponente.matriz[x][coluna])
    else:
        linha = ord(direcao.upper()) - ord("A")
        print(tabuleiro_oponente.matriz[linha])
    print("Sonar ativado!")

# Mapeamento de poderes para suas funções correspondentes
POWERS = {
    "bombardeio": poder_bombardeio,
    "reconhecimento": poder_reconhecimento,
    "nevoeiro": poder_nevoeiro,
    "decoy": poder_decoy,
    "sonar": poder_sonar,
}

def usar_poder(poder, tabuleiro_proprio, tabuleiro_oponente, turnos_temporarios):
    """
    Chama a função correspondente ao poder especificado.
    """
    func = POWERS.get(poder["tipo"])
    if not func:
        print(f"Poder desconhecido: {poder['tipo']}")
        return
    if poder["tipo"] in ["nevoeiro", "decoy"]:
        func(poder, tabuleiro_proprio, turnos_temporarios)
    elif poder["tipo"] in ["bombardeio", "reconhecimento", "sonar"]:
        func(poder, tabuleiro_oponente, turnos_temporarios)
    else:
        print("Tipo de poder não implementado.")
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
