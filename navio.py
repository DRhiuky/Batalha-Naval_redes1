class Navio:
    def __init__(self, nome, tamanho, numero):
        self.nome = nome
        self.tamanho = tamanho
        self.numero = numero  # Número que representa o navio no tabuleiro
        self.posicoes = []  # Lista de tuplas (x, y) indicando as posições ocupadas
        self.atingido = [False] * tamanho  # Lista para registrar as partes atingidas do navio
    
    def posicionar(self, posicoes):
        """Posiciona o navio no tabuleiro."""
        if len(posicoes) != self.tamanho:
            raise ValueError(f"O número de posições ({len(posicoes)}) não corresponde ao tamanho do navio ({self.tamanho}).")
        self.posicoes = posicoes
    
    def atacar(self, posicao):
        """Marca uma parte do navio como atingida, se a posição for válida."""
        if posicao in self.posicoes:
            index = self.posicoes.index(posicao)
            self.atingido[index] = True
            return True
        return False
    
    def afundado(self):
        """Verifica se todas as partes do navio foram atingidas."""
        return all(self.atingido)
