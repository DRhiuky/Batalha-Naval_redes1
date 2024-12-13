import socket
import threading

HOST = "0.0.0.0"
PORT = 12345
MAX_PLAYERS = 2

players = []  # Lista para armazenar informações dos jogadores
lock = threading.Lock()

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
            conn.sendall(b"Navio posicionado com sucesso.\n")
            # Você pode armazenar ou processar os dados do navio aqui, se necessário
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

    # Loop dos turnos
    while True:
        if "turn" in players[player_id] and players[player_id]["turn"]:
            conn.sendall(b"Sua vez! Informe sua jogada (ex: A14) ou 'sair' para encerrar: ")
            data = conn.recv(1024).decode("utf-8").strip()
            if data.lower() == "sair":
                print(f"Jogador {player_id} saiu.")
                conn.sendall("Você saiu do jogo.\n".encode("utf-8"))
                conn.close()
                return
            with lock:
                players[1 - player_id]["conn"].sendall(f"Oponente jogou: {data}\n".encode("utf-8"))
                players[player_id]["turn"] = False
                players[1 - player_id]["turn"] = True
        else:
            if not players[player_id].get("waiting", False):
                conn.sendall(b"Aguardando sua vez...\n")
                players[player_id]["waiting"] = True

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
                    "turn": player_id == 0  # O jogador 0 começa jogando
                })
            threading.Thread(target=handle_player, args=(conn, addr, player_id)).start()


if __name__ == "__main__":
    start_server()
