class Tabuleiro:
    def __init__(self, tamanho=24):
        self.tamanho = tamanho
        self.matriz = [[0 for _ in range(tamanho)] for _ in range(tamanho)]
        self.navios = []  # Lista de navios posicionados no tabuleiro

    def exibir(self):
        """Exibe o tabuleiro no terminal."""
        letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        print("   " + " ".join(f"{i:2}" for i in range(1, self.tamanho + 1)))
        for idx, linha in enumerate(self.matriz):
            print(f"{letras[idx]:2} " + " ".join(str(cell) for cell in linha))
            
    def formatar_para_envio(self):
        """
        Formata o tabuleiro em uma string legível para envio ao jogador.
        """
        letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        linhas = ["   " + " ".join(f"{i:2}" for i in range(1, self.tamanho + 1))]
        for idx, linha in enumerate(self.matriz):
            linhas.append(f"{letras[idx]:2} " + " ".join(str(cell) for cell in linha))
        return "\n".join(linhas)


    def validar_posicao(self, x, y):
        """Valida se uma posição está dentro dos limites do tabuleiro."""
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

    def atualizar_com_ataque(self, x, y, resultado):
        """
        Atualiza o tabuleiro com o resultado do ataque.
        """
        if resultado in ["acerto", "afundado"]:
            self.matriz[x][y] = "X"
        elif resultado == "agua":
            self.matriz[x][y] = "*"


    def atualizar_com_ataque(self, x, y, resultado):
        """
        Atualiza o tabuleiro com o resultado do ataque.
        """
        if resultado in ["acerto", "afundado"]:
            self.matriz[x][y] = "X"
        elif resultado == "agua":
            self.matriz[x][y] = "*"

    def atacar(self, x, y):
        """
        Processa o ataque no tabuleiro.
        Retorna "acerto", "afundado" ou "agua".
        """
        for navio in self.navios:
            if (x, y) in navio.posicoes:
                acertou = navio.atacar((x, y))
                self.matriz[x][y] = "X"  # Marca o acerto no tabuleiro
                if navio.afundado():
                    return "afundado"
                elif acertou:
                    return "acerto"
        self.matriz[x][y] = "*"  # Marca água no tabuleiro
        return "agua"

    def todos_afundados(self):
        """Verifica se todos os navios foram afundados."""
        return all(navio.afundado() for navio in self.navios)

    def get_publico(self):
        """
        Retorna o estado público do tabuleiro, exibindo apenas acertos (X) e tiros na água (*).
        """
        letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        linhas = ["   " + " ".join(f"{i:2}" for i in range(1, self.tamanho + 1))]
        for idx, linha in enumerate(self.matriz):
            linhas.append(f"{letras[idx]:2} " + " ".join(
                "X" if cell == "X" else "*" if cell == "*" else "~"  # "~" representa células não atacadas
                for cell in linha))
        return "\n".join(linhas)


    def get_completo(self):
        """Retorna o estado completo do tabuleiro, exibindo todas as células."""
        return "\n".join(
            " ".join(str(cell) for cell in row) for row in self.matriz
        )

    def exibir_publico(self):
        """Exibe o estado público do tabuleiro, onde apenas acertos (X) e erros (*) são visíveis."""
        letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        linhas = ["   " + " ".join(f"{i:2}" for i in range(1, self.tamanho + 1))]
        for idx, linha in enumerate(self.matriz):
            linhas.append(f"{letras[idx]:2} " + " ".join(
                str(cell) if cell in ["X", "*"] else "~"  # "~" representa células não atacadas
                for cell in linha
            ))
        return "\n".join(linhas)
    
    def exibir_completo(self):
        """Exibe o estado completo do tabuleiro, com navios, acertos e erros."""
        letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        linhas = ["   " + " ".join(f"{i:2}" for i in range(1, self.tamanho + 1))]
        for idx, linha in enumerate(self.matriz):
            linhas.append(f"{letras[idx]:2} " + " ".join(str(cell) for cell in linha))
        return "\n".join(linhas)