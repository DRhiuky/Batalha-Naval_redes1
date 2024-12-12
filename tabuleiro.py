import random

class Tabuleiro:
    def __init__(self, tamanho=24):
        self.tamanho = tamanho
        self.matriz = [[0 for _ in range(tamanho)] for _ in range(tamanho)]
        self.navios = []  # Lista de navios posicionados no tabuleiro
        
    def gerar_posicao_aleatoria(self, tamanho):
        """Gera uma posição aleatória válida para um navio."""
        orientacao = random.choice(["H", "V"])  # Escolhe entre horizontal (H) e vertical (V)
        if orientacao == "H":  # Horizontal
            x = random.randint(0, self.tamanho - 1)  # Linha fixa
            y = random.randint(0, self.tamanho - tamanho)  # Coluna inicial
            return [(x, y + i) for i in range(tamanho)]
        else:  # Vertical
            x = random.randint(0, self.tamanho - tamanho)  # Linha inicial
            y = random.randint(0, self.tamanho - 1)  # Coluna fixa
            return [(x + i, y) for i in range(tamanho)]
    
    def exibir(self):
        letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        print("   " + " ".join(f"{i:2}" for i in range(1, self.tamanho + 1)))
        for idx, linha in enumerate(self.matriz):
            print(f"{letras[idx]:2} " + " ".join(str(cell) for cell in linha))
    
    def validar_posicao(self, x, y):
        return 0 <= x < self.tamanho and 0 <= y < self.tamanho
    
    def verificar_disponibilidade(self, posicoes):
        """Verifica se as posições estão livres."""
        return all(self.validar_posicao(x, y) and self.matriz[x][y] == 0 for x, y in posicoes)
    
    def posicionar_navio(self, navio, posicoes):
        """Posiciona o navio no tabuleiro."""
        if self.verificar_disponibilidade(posicoes):
            for x, y in posicoes:
                self.matriz[x][y] = navio.numero
            navio.posicionar(posicoes)
            self.navios.append(navio)
        else:
            raise ValueError("As posições estão ocupadas ou fora dos limites.")
    
    def atacar(self, x, y):
        """Processa um ataque no tabuleiro."""
        if not self.validar_posicao(x, y):
            return "Coordenadas inválidas!"
        
        for navio in self.navios:
            if (x, y) in navio.posicoes:
                acertou = navio.atacar((x, y))
                self.matriz[x][y] = "X"  # Marca o ataque no tabuleiro
                if navio.afundado():
                    return f"{navio.nome.upper()} AFUNDADO!"
                elif acertou:
                    return "ACERTO!"
        
        self.matriz[x][y] = "*"  # Marca um tiro na água
        return "ÁGUA!"
