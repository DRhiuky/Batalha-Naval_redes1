class Tabuleiro:
    def __init__(self):
        # Criar tabuleiro vazio (24x24)
        self.tamanho = 24
        self.matriz = [[None for _ in range(self.tamanho)] for _ in range(self.tamanho)]

    def coordenada_valida(self, coord):
        """Verifica se a coordenada está dentro do tabuleiro."""
        if len(coord) < 2 or not coord[1:].isdigit():
            return False
        
        linha = coord[0].upper()
        coluna = int(coord[1:])
        return linha in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[:self.tamanho] and 1 <= coluna <= self.tamanho

    def traduzir_coordenada(self, coord):
        """Converte coordenada (ex.: 'A1') para índices da matriz."""
        linha = ord(coord[0].upper()) - ord('A')
        coluna = int(coord[1:]) - 1
        return linha, coluna

    def verificar_jogada(self, coord):
        """Valida a jogada e retorna o estado da célula."""
        if not self.coordenada_valida(coord):
            return "CoordInválida"

        linha, coluna = self.traduzir_coordenada(coord)
        if self.matriz[linha][coluna] is None:
            return "Água"
        elif self.matriz[linha][coluna] == "Navio":
            return "Acerto"
        elif self.matriz[linha][coluna] in ["Água", "Acerto"]:
            return "JáAtacada"
        return "Erro"

    def registrar_jogada(self, coord):
        """Registra o resultado da jogada no tabuleiro."""
        linha, coluna = self.traduzir_coordenada(coord)
        estado = self.verificar_jogada(coord)

        if estado == "Água":
            self.matriz[linha][coluna] = "Água"
        elif estado == "Acerto":
            self.matriz[linha][coluna] = "Acerto"
        return estado
