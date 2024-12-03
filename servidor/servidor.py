import socket
import threading
import random
import time
from game_logic import Tabuleiro

# Configurações do servidor
HOST = "0.0.0.0"
PORT = 12345
TURN_TIMEOUT = 60  # Tempo limite de 60 segundos por turno

# Estado do jogo
jogadores = {}
turno_atual = None
jogo_iniciado = False
lock = threading.Lock()

def iniciar_jogo():
    """Inicia o jogo se ambos os jogadores estiverem prontos e define o primeiro turno aleatoriamente."""
    global jogo_iniciado, turno_atual
    with lock:
        if len(jogadores) == 2 and all(j["pronto"] for j in jogadores.values()) and not jogo_iniciado:
            jogo_iniciado = True
            turno_atual = random.choice(["player1", "player2"])  # Seleciona aleatoriamente o primeiro jogador
            print("[JOGO INICIADO] Ambos os jogadores estão prontos!")
            print(f"[TURNO INICIAL] O primeiro turno é do {turno_atual}.")
            for jogador_id, jogador in jogadores.items():
                if jogador_id == turno_atual:
                    jogador["socket"].send(f"GAME_STARTED: O jogo começou! Você é {jogador_id}. É o seu turno.".encode("utf-8"))
                else:
                    jogador["socket"].send(f"GAME_STARTED: O jogo começou! Você é {jogador_id}. Aguarde o seu turno.".encode("utf-8"))
            threading.Thread(target=gerenciar_turno, daemon=True).start()

def alternar_turno():
    """Alterna o turno entre os jogadores e notifica ambos."""
    global turno_atual
    turno_atual = "player1" if turno_atual == "player2" else "player2"
    print(f"[TURNO] É a vez de {turno_atual}.")
    for jogador_id, jogador in jogadores.items():
        if jogador_id == turno_atual:
            jogador["socket"].send("TURN: É o seu turno!".encode("utf-8"))
        else:
            jogador["socket"].send("WAIT: Aguarde seu turno.".encode("utf-8"))

def gerenciar_turno():
    """Controla o tempo do turno e alterna se o jogador ultrapassar o limite."""
    global jogo_iniciado, turno_atual
    while jogo_iniciado:
        time.sleep(TURN_TIMEOUT)
        if jogo_iniciado:  # Verifica se o jogo ainda está ativo
            print(f"[TIMEOUT] O jogador {turno_atual} não jogou no tempo limite.")
            alternar_turno()

def handle_client(client_socket, address):
    global jogadores, turno_atual, jogo_iniciado
    print(f"[NOVO CLIENTE] Conexão de {address} estabelecida.")

    with lock:
        if len(jogadores) >= 2:
            print(f"[DEBUG] Conexão rejeitada: {address} (Jogo cheio)")
            client_socket.send("CONNECTION_DENIED: O jogo já está cheio.".encode("utf-8"))
            client_socket.close()
            return

        jogador_id = f"player{len(jogadores) + 1}"
        jogadores[jogador_id] = {
            "socket": client_socket,
            "endereco": address,
            "tabuleiro": Tabuleiro(),
            "pronto": False
        }
        client_socket.send(f"CONNECTED: Você é {jogador_id}. Aguardando outro jogador...".encode("utf-8"))
        print(f"[DEBUG] {jogador_id} foi adicionado ao jogo.")

    while True:
        try:
            data = client_socket.recv(1024).decode("utf-8")
            if not data:
                break

            print(f"[{address}] {data}")
            response = "Comando inválido."

            if data == "READY":
                with lock:
                    jogadores[jogador_id]["pronto"] = True
                    print(f"[DEBUG] {jogador_id} está pronto.")
                response = f"STATUS: Você está pronto como {jogador_id}."
                client_socket.send(response.encode("utf-8"))
                iniciar_jogo()

            elif data.startswith("MOVE:") and jogo_iniciado:
                if jogador_id != turno_atual:
                    response = "STATUS: Não é seu turno!"
                else:
                    coordenada = data.split(":")[1].strip()
                    estado = jogadores[turno_atual]["tabuleiro"].registrar_jogada(coordenada)
                    if estado == "CoordInválida":
                        response = "RESULT: Coordenada inválida!"
                    elif estado == "JáAtacada":
                        response = "RESULT: Essa casa já foi atacada!"
                    elif estado == "Água":
                        response = "RESULT: Água!"
                        alternar_turno()
                    elif estado == "Acerto":
                        response = "RESULT: Acertou um navio!"
                        alternar_turno()
                    else:
                        response = "RESULT: Erro inesperado."

            elif data == "QUIT":
                response = "Você desistiu do jogo. Voltando ao menu principal."
                break

            client_socket.send(response.encode("utf-8"))
        except ConnectionResetError:
            break

    print(f"[CLIENTE DESCONECTADO] {address} desconectou.")
    with lock:
        if jogador_id in jogadores:
            del jogadores[jogador_id]
    client_socket.close()

def start_server():
    """Inicializa o servidor e gerencia conexões."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"[SERVIDOR INICIADO] Aguardando conexões em {HOST}:{PORT}...")

    while True:
        client_socket, address = server.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, address))
        client_thread.start()

if __name__ == "__main__":
    start_server()
