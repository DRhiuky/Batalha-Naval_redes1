import socket
import threading

# Configurações do cliente
HOST = "127.0.0.1"
PORT = 12345

def escutar_servidor(client):
    """Thread para escutar mensagens do servidor."""
    while True:
        try:
            response = client.recv(1024).decode("utf-8")
            if not response:
                print("[ERRO] Conexão encerrada pelo servidor.")
                break
            print(f"\n[SERVIDOR] {response}\n")
        except ConnectionResetError:
            print("\n[ERRO] Conexão encerrada pelo servidor.")
            break

def menu_principal():
    """Menu principal para conexão ao servidor."""
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        print("\n=== Menu Principal ===")
        print("1 - Conectar e Jogar")
        print("2 - Sair")
        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            if conectar(client):
                threading.Thread(target=escutar_servidor, args=(client,), daemon=True).start()
                menu_jogo(client)
        elif escolha == "2":
            print("Saindo...")
            client.close()
            break
        else:
            print("Opção inválida!")

def conectar(client):
    """Conecta ao servidor e trata possíveis erros."""
    try:
        client.connect((HOST, PORT))
        print(f"[CONECTADO] Conectado ao servidor em {HOST}:{PORT}")
        return True
    except Exception as e:
        print(f"[ERRO] Não foi possível conectar ao servidor: {e}")
        return False

def menu_jogo(client):
    """Menu dentro do jogo com opções de enviar READY e interagir."""
    print("[AGUARDANDO INÍCIO] Esperando todos os jogadores...")
    
    # Enviar comando READY ao servidor
    try:
        client.send("READY".encode("utf-8"))
        print("[STATUS] Você ficou pronto. Aguardando início do jogo...")
    except Exception as e:
        print(f"[ERRO] Não foi possível enviar o comando READY: {e}")
        return
    
    while True:
        print("\n=== Menu do Jogo ===")
        print("1 - Fazer jogada")
        print("2 - Usar poder especial")
        print("3 - Desistir e voltar ao menu principal")
        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            jogada = input("Digite a coordenada para atacar (ex.: A1): ").upper()
            try:
                client.send(f"MOVE: {jogada}".encode("utf-8"))
            except Exception as e:
                print(f"[ERRO] Não foi possível enviar a jogada: {e}")
        elif escolha == "2":
            poder = input("Digite o poder (Sonar, Decoy ou Nevoeiro): ").capitalize()
            try:
                client.send(f"POWER: {poder}".encode("utf-8"))
            except Exception as e:
                print(f"[ERRO] Não foi possível enviar o comando do poder: {e}")
        elif escolha == "3":
            try:
                client.send("QUIT".encode("utf-8"))
                print("[STATUS] Você desistiu. Voltando ao menu principal...")
            except Exception as e:
                print(f"[ERRO] Não foi possível enviar o comando de saída: {e}")
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    try:
        print("[INFO] Iniciando o cliente...")
        menu_principal()
    except KeyboardInterrupt:
        print("\n[INFO] Cliente encerrado pelo usuário.")
    except Exception as e:
        print(f"[ERRO] Um erro inesperado ocorreu: {e}")
