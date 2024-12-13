import socket
import threading
from tabuleiro import Tabuleiro
from navio import Navio
from utils import entrada_para_coordenadas

HOST = "0.0.0.0"
PORT = 12345
MAX_PLAYERS = 2

players = []  # Lista para armazenar informações dos jogadores
lock = threading.Lock()

def handle_turns():
    """
    Gerencia a fase de turnos do jogo.
    """
    while True:
        for player_id in range(MAX_PLAYERS):
            opponent_id = 1 - player_id
            player = players[player_id]
            opponent = players[opponent_id]
            conn = player["conn"]

            try:
                # Atualiza e envia o estado dos tabuleiros
                conn.sendall(b"\nSeu tabuleiro (completo):\n")
                conn.sendall(player["tabuleiro"].exibir_completo().encode("utf-8"))
                conn.sendall(b"\nTabuleiro do adversario (publico):\n")
                conn.sendall(opponent["tabuleiro_publico"].exibir_publico().encode("utf-8"))

                # Solicita a jogada
                conn.sendall(b"Sua vez! Informe sua jogada (ex: A14) ou 'sair' para encerrar: ")
                data = conn.recv(1024).decode("utf-8").strip()

                if data.lower() == "sair":
                    print(f"Jogador {player_id} saiu.")
                    conn.sendall(b"Voce saiu do jogo.\n")
                    opponent["conn"].sendall(b"O oponente saiu. Voce venceu!\n")
                    return

                # Processa o ataque
                x, y = entrada_para_coordenadas(data)
                resultado = opponent["tabuleiro"].atacar(x, y)

                # Atualiza o estado público do tabuleiro do adversário
                opponent["tabuleiro_publico"].atualizar_com_ataque(x, y, resultado)

                # Envia mensagens sobre o resultado do ataque
                if resultado == "acerto":
                    conn.sendall("ACERTOU! Você atingiu um navio.\n".encode("utf-8"))
                    opponent["conn"].sendall(f"Oponente atacou {data}: ACERTOU!\n".encode("utf-8"))
                elif resultado == "afundado":
                    conn.sendall(b"ACERTOU! Voce afundou um navio.\n")
                    opponent["conn"].sendall(f"Oponente atacou {data}: ACERTOU e AFUNDOU um navio!\n".encode("utf-8"))
                else:  # "agua"
                    conn.sendall(b"AGUA! Voce nao atingiu nada.\n")
                    opponent["conn"].sendall(f"Oponente atacou {data}: ÁGUA!\n".encode("utf-8"))

                # Verifica a condição de vitória
                if opponent["tabuleiro"].todos_afundados():
                    conn.sendall("Parabéns! Você venceu.\n".encode("utf-8"))
                    opponent["conn"].sendall(b"Voce perdeu. Todos os seus navios foram afundados.\n")
                    return

            except Exception as e:
                print(f"Erro ao processar turno do jogador {player_id}: {e}")
                conn.sendall(b"Erro ao processar sua jogada. Tente novamente.\n")



def handle_player(conn, addr, player_id):
    """
    Lida com a conexão de um jogador.
    """
    global players

    print(f"Jogador {player_id} conectado: {addr}")
    conn.sendall(b"Bem-vindo ao Batalha Naval! Aguardando outros jogadores...\n")

    if len(players) < MAX_PLAYERS:
        conn.sendall(b"Aguardando outro jogador conectar...\n")

    # Aguarda todos os jogadores
    while len(players) < MAX_PLAYERS:
        pass

    conn.sendall(b"Todos os jogadores conectados. Iniciando fase de posicionamento.\n")
    conn.sendall(b"Posicione seus navios...\n")

    # Fase de posicionamento
    while True:
        data = conn.recv(1024).decode("utf-8").strip()
        if "ready" in data:  # Aceitar strings que contenham "ready"
            with lock:
                players[player_id]["ready"] = True
            conn.sendall(b"Aguardando oponente...\n")
            break
        elif ":" in data:  # Mensagem de posicionamento de navios
            print(f"Recebido do jogador {player_id}: {data}")
            navio_info = data.split(":")
            if len(navio_info) == 2:
                try:
                    navio_nome = navio_info[0]
                    posicoes = eval(navio_info[1])
                    players[player_id]["tabuleiro"].posicionar_navio(
                        Navio(navio_nome, len(posicoes), len(players[player_id]["tabuleiro"].navios) + 1), posicoes
                    )
                    conn.sendall(b"Navio posicionado com sucesso.\n")
                except Exception as e:
                    print(f"Erro ao processar navio do jogador {player_id}: {e}")
                    conn.sendall(b"Erro ao posicionar navio. Verifique a entrada e tente novamente.\n")
            else:
                conn.sendall(b"Formato invalido para posicionamento. Tente novamente.\n")
        elif data:  # Mensagem inválida
            print(f"Mensagem não reconhecida de {addr}: {data}")
            conn.sendall("Entrada inválida. Digite 'ready' após posicionar os navios.\n".encode("utf-8"))

    # Aguarda o outro jogador finalizar o posicionamento
    while not all(player["ready"] for player in players):
        pass

    if player_id == 0:
        conn.sendall("Você começará jogando.\n".encode("utf-8"))
    else:
        conn.sendall("Seu oponente começará jogando.\n".encode("utf-8"))

    # Após o posicionamento, inicia a fase de turnos
    if player_id == 0:  # Apenas o primeiro jogador gerencia a fase de turnos
        handle_turns()


def start_server():
    """
    Inicia o servidor.
    """
    global players

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen(MAX_PLAYERS)
        print(f"Servidor rodando em {HOST}:{PORT}")

        while True:
            conn, addr = server_socket.accept()
            with lock:
                if len(players) >= MAX_PLAYERS:
                    conn.sendall("ERRO: O jogo já está cheio. Tente novamente mais tarde.\n".encode("utf-8"))
                    conn.close()
                    continue

                player_id = len(players)
                players.append({
                    "id": player_id,
                    "conn": conn,
                    "addr": addr,
                    "ready": False,
                    "turn": player_id == 0,  # O jogador 0 começa jogando
                    "tabuleiro": Tabuleiro(),
                    "tabuleiro_publico": Tabuleiro()
                })
            threading.Thread(target=handle_player, args=(conn, addr, player_id)).start()

if __name__ == "__main__":
    start_server()
