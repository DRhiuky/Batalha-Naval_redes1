# Protocolo de Comunicação

## Formato das mensagens
As mensagens trocadas entre cliente e servidor seguem o formato de texto simples UTF-8.

### Tipos de mensagens
1. **Conexão inicial**:
   - Cliente: Envia uma mensagem para identificar a conexão.
   - Exemplo: `"PLAYER_NAME: Jogador1"`

2. **Jogada**:
   - Cliente: Envia uma coordenada de ataque.
   - Exemplo: `"MOVE: A1"`

3. **Resposta do servidor**:
   - Servidor: Envia o resultado da jogada ou mensagens de status.
   - Exemplo: `"RESULT: Hit!"` ou `"RESULT: Miss!"`

4. **Poderes**:
   - Cliente: Solicita ativação de um poder especial.
   - Exemplo: `"POWER: Sonar A"`

5. **Encerramento da conexão**:
   - Cliente: `"QUIT"`
   - Servidor: `"GAME_OVER: Vitória do Jogador1"`
