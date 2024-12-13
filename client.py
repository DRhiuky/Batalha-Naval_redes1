import socket
import os
from tabuleiro import Tabuleiro
from navio import Navio
from utils import entrada_para_coordenadas

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 12345

def limpar_terminal():
    """
    Limpa o terminal do cliente.
    """
    os.system("cls" if os.name == "nt" else "clear")

def connect_to_server():
    """
    Conecta ao servidor e gerencia a comunicação.
    """
    tabuleiro = Tabuleiro()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            client_socket.connect((SERVER_HOST, SERVER_PORT))
            print("Conectado ao servidor.")

            while True:
                data = client_socket.recv(4096).decode("utf-8")
                if not data:
                    break

                if "Posicione seus navios" in data:
                    # Fase de posicionamento
                    print("\nFase de posicionamento:")
                    tipos_navios = [
                        ("Cruzador de Mísseis", 5, 1, 5),
                        ("Porta-Aviões", 4, 0, 4),
                        ("Contratorpedeiro", 3, 0, 3),
                        ("Couraçado", 2, 0, 2),
                        ("Submarino", 1, 0, 1),
                    ]

                    navios_disponiveis = [
                        (nome, tamanho, numero)
                        for nome, tamanho, quantidade, numero in tipos_navios
                        for _ in range(quantidade)
                    ]

                    while navios_disponiveis:
                        limpar_terminal()
                        print("\nTabuleiro atual:")
                        tabuleiro.exibir()

                        print("\nNavios disponíveis:")
                        for i, (nome, tamanho, _) in enumerate(navios_disponiveis):
                            print(f"{i + 1}. {nome} (Tamanho: {tamanho})")

                        try:
                            escolha = int(input("\nEscolha um navio pelo número: ")) - 1
                            if escolha < 0 or escolha >= len(navios_disponiveis):
                                print("Escolha inválida.")
                                continue

                            nome, tamanho, numero = navios_disponiveis[escolha]
                            entrada = input(f"Informe a posição inicial para o {nome} (ex: 'A 1'): ")
                            orientacao = input("Informe a orientação ('h' para horizontal, 'v' para vertical): ").lower()
                            x, y = entrada_para_coordenadas(entrada)

                            if orientacao == "h":
                                posicoes = [(x, y + i) for i in range(tamanho)]
                            elif orientacao == "v":
                                posicoes = [(x + i, y) for i in range(tamanho)]
                            else:
                                print("Orientação inválida. Use 'h' ou 'v'.")
                                continue

                            if tabuleiro.verificar_disponibilidade(posicoes):
                                navio = Navio(nome, tamanho, numero)
                                tabuleiro.posicionar_navio(navio, posicoes)
                                print(f"{nome} posicionado com sucesso!")
                                client_socket.sendall(f"{nome}:{posicoes}\n".encode("utf-8"))
                                navios_disponiveis.pop(escolha)

                            if not navios_disponiveis:
                                print("Todos os navios foram posicionados. Informando o servidor...")
                                client_socket.sendall("ready".encode("utf-8"))
                                break

                        except (ValueError, IndexError) as e:
                            print(f"Erro: {e}. Tente novamente.")

                elif "Seu tabuleiro" in data:
                    # Exibição de tabuleiros durante os turnos
                    limpar_terminal()
                    partes = data.split("Tabuleiro do adversário (público):")
                    if len(partes) == 2:
                        print("Seu tabuleiro:")
                        print(partes[0])  # Mostra o tabuleiro completo do jogador
                        print("\nTabuleiro do adversário (público):")
                        print(partes[1])  # Mostra apenas os ataques no tabuleiro público

                elif "Sua vez!" in data:
                    # Jogada do jogador
                    print(data)
                    jogada = input("\nInforme sua jogada (ex: A 14): ")
                    client_socket.sendall(jogada.encode("utf-8"))
                elif "Aguardando sua vez" in data:
                    # Mensagem de espera
                    print(data)
                elif "Você saiu" in data or "Você venceu" in data or "Você perdeu" in data:
                    # Finalização do jogo
                    print(data)
                    break

        except ConnectionRefusedError:
            print("Erro: Não foi possível conectar ao servidor. Verifique se ele está ativo.")

if __name__ == "__main__":
    connect_to_server()
