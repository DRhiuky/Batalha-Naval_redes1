nome: Luiz Augusto Bello Marques dos Anjos
matricula: 202010242

---

# Documentação do Protocolo de Comunicação e Funcionamento do Software


### Visão Geral
Este protocolo define a comunicação entre o cliente e o servidor do jogo de Batalha Naval. A interação ocorre através de sockets TCP, permitindo troca confiável de mensagens e controle do estado do jogo. O protocolo inclui eventos, estados e mensagens trocadas durante as fases do jogo: conexão, posicionamento de navios, turnos de ataque, e finalização do jogo.

---

### Estrutura das Mensagens
1. Mensagens do Servidor para o Cliente:
   - Mensagens iniciam com uma descrição textual clara e delimitada por quebras de linha (`\n`).
   - Exemplos:
     - `Bem-vindo ao Batalha Naval! Aguardando outros jogadores...\n`
     - `Posicione seus navios...\n`
     - `Você venceu!\n`
     - `Oponente atacou B12: ACERTOU!\n`

2. Mensagens do Cliente para o Servidor:
   - Formatos:
     - Comando simples (`ready`, `sair`).
     - Ataques: coordenadas no formato `<letra> <número>` (ex.: `A 12`).
     - Dados do posicionamento: `<nome do navio>:<lista de coordenadas>` (ex.: `Cruzador:[(0,0),(0,1),(0,2)]`).

---

### Eventos e Estados

#### Conexão
- Evento: O cliente se conecta ao servidor.
- Mensagens:
  - Servidor → Cliente:
    - `Bem-vindo ao Batalha Naval! Aguardando outros jogadores...\n`
    - `Aguardando outro jogador conectar...\n`
    - `Todos os jogadores conectados. Iniciando fase de posicionamento.\n`

#### Posicionamento de Navios
- Evento: Cada jogador posiciona seus navios no tabuleiro, escolhendo um navio da lista disponível, informando a coordenada inicial e a orientação (`h` para horizontal ou `v` para vertical).
- Lista de Navios Disponíveis:
  - Cruzador de Mísseis (tamanho: 5)
  - Porta-Aviões (tamanho: 4)
  - Contratorpedeiro (tamanho: 3)
  - Couraçado (tamanho: 2)
  - Submarino (tamanho: 1)

  O jogador escolhe o navio desejado pela ordem na lista, define a posição inicial no formato `A 1` e a orientação.

- Mensagens:
  - Servidor → Cliente:
    - `Posicione seus navios...\n`
    - Exemplo de instrução: "Escolha um navio para posicionar. Informe a coordenada inicial (ex.: 'A 1') e a orientação ('h' ou 'v')."
  - Cliente → Servidor:
    - `<nome do navio>:<lista de coordenadas>`
    - Ex.: `Cruzador:[(0,0),(0,1),(0,2)]`

#### Turnos de Jogo
- Evento: Jogadores alternam turnos para realizar ataques.
- Mensagens:
  - Servidor → Cliente:
    - `Seu tabuleiro: <estado do tabuleiro próprio>`
    - `Tabuleiro do adversário (público): <estado do tabuleiro público>`
    - `Sua vez! Informe sua jogada (ex: A12) ou 'sair' para encerrar: `
    - `Você venceu!\n`
    - `O oponente saiu. Você venceu!\n`
  - Cliente → Servidor:
    - `<letra> <número>`: Indica a coordenada atacada.
    - `sair`: Finaliza o jogo.

#### Finalização do Jogo
- Evento: O jogo é encerrado por vitória, derrota ou desistência.
- Mensagens:
  - Servidor → Cliente:
    - `Você venceu!\n`
    - `Você perdeu. Todos os seus navios foram afundados.\n`
    - `O oponente saiu. Você venceu!\n`

---

## Documentação do Funcionamento do Software

### Propósito
Este software implementa o jogo Batalha Naval de forma distribuída para o trabalho realizado na disciplina de redes I do curso de Ciência da Computação da UESC ministrada pelo docente Jorge Lima de Oliveira Filho, utilizando o modelo cliente-servidor. O software oferece uma experiência multiplayer para dois jogadores, com comunicação pela rede e regras clássicas do jogo. O objetivo do trabalho foi promover aprendizado sobre desenvolvimento de sistemas distribuídos e uso de sockets TCP.

---

### Motivação da Escolha do Protocolo de Transporte
Optou-se pelo uso do protocolo TCP devido às seguintes razões:
1. Confiabilidade: O TCP garante entrega de mensagens na ordem correta, essencial para sincronização entre jogadores.
2. Controle de Conexão: O protocolo permite rastrear quando um cliente se conecta ou desconecta, essencial para gerenciar eventos como desistência.
3. Robustez: Em um jogo com interação contínua, como Batalha Naval, falhas na entrega de mensagens poderiam comprometer a experiência.

---

### Requisitos Mínimos
1. Hardware:
   - Computador com capacidade para rodar Python 3.8 ou superior.
   - Rede local ou internet com suporte a conexões TCP.

2. Software:
   - Python 3.8 ou superior.
   - Dependências padrão do Python (sem bibliotecas externas adicionais).

3. Configuração de Rede:
   - O servidor deve estar acessível por um endereço IP público ou privado na rede local.
   
   3.1. Servidor em Rede Remota:
     1. Certifique-se de que o computador que irá rodar o servidor tem um endereço IP acessível na rede (pública ou local). Use o comando `ipconfig` (Windows) ou `ifconfig` (Linux/Mac) para verificar o IP.
     2. Caso o servidor esteja em uma rede doméstica e precise ser acessado por clientes fora dessa rede, configure o redirecionamento de portas (port forwarding) no roteador para a porta utilizada pelo servidor (padrão: 12345) apontando para o IP interno do servidor.
     3. Garanta que o firewall do servidor permita conexões na porta 12345. Em sistemas como Windows, Linux (iptables/ufw), ou Mac, adicione uma exceção para essa porta.
   
   - Conexão dos Clientes:
     1. Configure os clientes para usar o endereço IP do servidor em vez de `127.0.0.1` (localhost). Por exemplo:
        - Se o IP do servidor for `192.168.0.100` na rede local, configure `SERVER_HOST = "192.168.0.100"` no cliente.
        - Se o IP público do servidor for `203.0.113.25`, configure `SERVER_HOST = "203.0.113.25"` no cliente.
     2. Certifique-se de que o cliente também tem acesso à internet ou à mesma rede local onde o servidor está rodando.

   - Teste de Conectividade:
     Antes de iniciar o jogo, teste a conexão entre o cliente e o servidor:
     - Use o comando `ping <IP do servidor>` para verificar se o servidor está alcançável.
     - Use o comando `telnet <IP do servidor> 12345` para verificar se a porta está acessível.

   - Os clientes devem ter permissão para realizar conexões TCP na porta definida (padrão: 12345).

4. Arquivos do Software:
   - Servidor: `server.py`
   - Cliente: `client.py`
   - Lógica do Jogo:
     - `tabuleiro.py`
     - `navio.py`
     - `turnos.py`
     - `poderes.py` (não implementado na versão final)
     - `utils.py`

---

### Fluxo do Jogo
1. Início:
   - O servidor é iniciado e aguarda conexões de dois clientes.
   - Após a conexão, os jogadores posicionam seus navios.

2. Turnos:
   - Jogadores alternam turnos para atacar e receber atualizações dos tabuleiros.
   - O jogo termina quando todos os navios de um jogador são afundados ou um jogador desiste.

3. Finalização:
   - O vencedor é anunciado ao final do jogo.

---

Nota: Apesar de planejados, poderes especiais não foram implementados na versão final devido à complexidade lógica e limitações do ambiente de terminal. O foco foi dado à estabilidade e funcionalidade básica do jogo.

---

### Arquivo: servidor.py

Descrição e funcionalidade:

O arquivo `servidor.py` implementa o lado servidor de um jogo distribuído de Batalha Naval utilizando o modelo cliente-servidor. Ele é responsável por gerenciar as conexões de dois clientes (jogadores), coordenar a troca de mensagens entre eles e implementar a lógica do jogo. A comunicação é feita via sockets TCP.

Componentes principais:

1. Constantes e variáveis globais:
   - `HOST`: Define o endereço IP no qual o servidor irá escutar (`0.0.0.0` para aceitar conexões de qualquer IP).
   - `PORT`: Porta utilizada para as conexões (padrão: 12345).
   - `MAX_PLAYERS`: Número máximo de jogadores (padrão: 2).
   - `players`: Lista que armazena informações sobre os jogadores conectados, incluindo o socket, tabuleiros e estado de prontidão.
   - `lock`: Trava para sincronização entre threads.

2. Funções principais:
   - `handle_turns`: Gerencia a fase de turnos do jogo. Essa função alterna entre os jogadores, solicita jogadas, processa ataques, atualiza os tabuleiros e verifica as condições de vitória. Ela também trata mensagens de saída do jogo.
   - `handle_player`: Gerencia a conexão de um jogador, incluindo a fase de posicionamento de navios. Recebe mensagens do cliente para posicionar navios no tabuleiro e confirma a prontidão do jogador. Após o posicionamento de ambos os jogadores, inicia a fase de turnos.
   - `start_server`: Inicia o servidor, configura o socket TCP e aguarda conexões dos jogadores. Para cada conexão aceita, uma nova thread é criada para tratar o jogador por meio da função `handle_player`.

3. Fluxo geral do servidor:
   - Aceita conexões até atingir o limite de jogadores (`MAX_PLAYERS`).
   - Coordena a fase de posicionamento, recebendo e validando as posições dos navios de cada jogador.
   - Inicia a fase de turnos, onde os jogadores alternam jogadas.
   - Envia mensagens de vitória, derrota ou saída conforme necessário.
   - Encerra a conexão ao final do jogo ou em caso de saída de um jogador.

4. Mensagens trocadas:
   - Durante o posicionamento: "Posicione seus navios", "Navio posicionado com sucesso", "Erro ao posicionar navio".
   - Durante os turnos: "Sua vez!", "ACERTOU!", "ÁGUA!", "Você venceu", "Você perdeu".
   - Mensagens de sincronização e status: "Aguardando outro jogador conectar", "Você começará jogando", "Seu oponente saiu".

5. Tratamento de exceções:
   - Todas as etapas críticas, como leitura de mensagens e processamento de jogadas, possuem tratamento de exceções para evitar falhas inesperadas no servidor.

6. Encerramento:
   - O servidor encerra a conexão de um jogador em caso de saída voluntária ou erro de comunicação.
   - A saída de um jogador encerra automaticamente o jogo e informa o outro jogador sobre o resultado.

Requisitos mínimos:
   - Python 3.8 ou superior.
   - O módulo `socket` para comunicação de rede.
   - O módulo `threading` para gerenciar conexões simultâneas.

Objetivo:
Este script é o núcleo do servidor para o jogo de Batalha Naval e deve ser executado antes de iniciar os clientes. Ele centraliza toda a lógica do jogo e comunicação entre os jogadores.

---

### Arquivo: cliente.py 

Descrição e funcionalidade:

O arquivo `cliente.py` implementa o lado cliente do jogo distribuído de Batalha Naval. Ele é responsável por conectar-se ao servidor, interagir com o usuário para posicionar navios, realizar ataques durante o jogo, e exibir o estado atualizado dos tabuleiros.

Componentes principais:

1. Constantes:
   - `SERVER_HOST`: Define o endereço IP do servidor ao qual o cliente irá se conectar (padrão: `127.0.0.1`).
   - `SERVER_PORT`: Define a porta utilizada para a conexão (padrão: 12345).

2. Funções principais:
   - `limpar_terminal`: Limpa o terminal para melhorar a visualização durante o jogo. Funciona tanto em sistemas Windows quanto Unix.
   - `connect_to_server`: Realiza a conexão ao servidor, coordena as interações com o jogador e gerencia a exibição e envio de informações.

3. Fluxo do cliente:
   - Estabelece uma conexão com o servidor utilizando sockets TCP.
   - Recebe instruções do servidor para posicionar navios no tabuleiro.
     - Solicita ao jogador as coordenadas e a orientação de cada navio.
     - Valida as posições antes de enviá-las ao servidor.
   - Durante os turnos, alterna entre:
     - Exibir os tabuleiros (próprio e público do oponente).
     - Solicitar e enviar uma jogada ao servidor.
   - Finaliza o jogo ao receber mensagens de término do servidor ou em caso de saída do oponente.

4. Mensagens trocadas:
   - Durante o posicionamento: "Posicione seus navios", "Todos os navios foram posicionados".
   - Durante os turnos: "Sua vez!", "Aguardando sua vez".
   - Mensagens finais: "Você venceu", "Você perdeu", "O oponente saiu".

5. Tratamento de erros:
   - Durante a conexão: Exibe uma mensagem de erro se não for possível conectar ao servidor.
   - Durante o posicionamento: Lida com entradas inválidas do usuário, como coordenadas fora do tabuleiro ou orientações inválidas.
   - Durante o jogo: Exibe mensagens apropriadas em caso de saída do oponente ou erro no envio/recebimento de dados.

Requisitos mínimos:
   - Python 3.8 ou superior.
   - O módulo `socket` para comunicação de rede.
   - O módulo `os` para limpeza do terminal.
   - Arquivos auxiliares: `tabuleiro.py`, `navio.py`, `utils.py`.

Objetivo:
Este script representa o cliente no jogo de Batalha Naval e deve ser executado por cada jogador. Ele permite que o jogador interaja com o servidor para posicionar navios, realizar ataques e acompanhar o progresso do jogo.

---

### Arquivo: tabuleiro.py 

Descrição e funcionalidade:

O arquivo `tabuleiro.py` implementa a classe `Tabuleiro`, responsável por gerenciar o estado e as operações relacionadas ao tabuleiro de cada jogador no jogo de Batalha Naval. Ele controla a disposição dos navios, valida jogadas, atualiza o tabuleiro conforme ataques e fornece representações tanto públicas quanto completas do estado do jogo.

Componentes principais:

1. Atributos da Classe `Tabuleiro`:
   - `tamanho`: Define o tamanho do tabuleiro (padrão: 24x24).
   - `matriz`: Matriz bidimensional que representa o tabuleiro. Inicialmente, todas as células têm o valor `0`.
   - `navios`: Lista que armazena os objetos `Navio` posicionados no tabuleiro.

2. Métodos da Classe `Tabuleiro`:
   - `__init__`: Inicializa um tabuleiro vazio.
   - `exibir`: Mostra o estado atual do tabuleiro no terminal, útil para debug e visualização local.
   - `formatar_para_envio`: Retorna uma string formatada do tabuleiro para envio ao cliente ou exibição.
   - `validar_posicao`: Verifica se uma posição (x, y) está dentro dos limites do tabuleiro.
   - `verificar_disponibilidade`: Confirma se as células necessárias para posicionar um navio estão livres e válidas.
   - `posicionar_navio`: Posiciona um navio no tabuleiro, atualizando a matriz com o tamanho do navio e armazenando o navio na lista `navios`.
   - `atualizar_com_ataque`: Atualiza a matriz com o resultado de um ataque, marcando `X` para acerto e `*` para erro.
   - `atacar`: Processa uma jogada no tabuleiro. Retorna os resultados:
     - `"acerto"`: Indica que um navio foi atingido.
     - `"afundado"`: Indica que um navio foi completamente destruído.
     - `"agua"`: Indica que o ataque não acertou nenhum navio.
   - `todos_afundados`: Verifica se todos os navios no tabuleiro foram afundados.
   - `get_publico`: Retorna uma string com o estado público do tabuleiro, mostrando apenas ataques acertados (X) e erros (*), ocultando os navios não atingidos.
   - `get_completo`: Retorna uma string com o estado completo do tabuleiro, incluindo a posição dos navios e ataques.
   - `exibir_publico`: Exibe no terminal o estado público do tabuleiro.
   - `exibir_completo`: Exibe no terminal o estado completo do tabuleiro.

3. Estado do Tabuleiro:
   - Estado inicial: Todas as células são `0`.
   - Após o posicionamento: As células correspondentes aos navios contêm o tamanho do navio.
   - Durante o jogo: As células podem ser atualizadas para `X` (acerto) ou `*` (erro).

4. Interface com Outras Classes:
   - Interage com a classe `Navio` para controlar as posições e o estado de cada navio no tabuleiro.

Requisitos mínimos:
   - Python 3.8 ou superior.
   - Arquivos auxiliares: `navio.py` (para criar objetos de navios).

Objetivo:
Esta classe é fundamental para o funcionamento do jogo, sendo responsável por organizar e exibir o estado do tabuleiro durante todas as fases do jogo: posicionamento, turnos de ataque e verificação de vitória.

---

### Arquivo: navio.py 

Descrição e funcionalidade:

O arquivo `navio.py` implementa a classe `Navio`, que representa cada navio do jogo de Batalha Naval. Ele controla as propriedades, posições e estado de cada navio durante o jogo, incluindo se foi atingido ou afundado.

Componentes principais:

1. Atributos da Classe `Navio`:
   - `nome`: Nome do navio (ex.: "Cruzador de Mísseis", "Submarino").
   - `tamanho`: Tamanho do navio em células.
   - `numero`: Número identificador do navio, usado para representação no tabuleiro.
   - `posicoes`: Lista de tuplas `(x, y)` que indicam as posições ocupadas pelo navio no tabuleiro.
   - `atingido`: Lista booleana que indica quais partes do navio foram atingidas.

2. Métodos da Classe `Navio`:
   - `__init__`: Inicializa o navio com suas propriedades básicas (nome, tamanho, número) e define suas posições como vazias e suas partes como não atingidas.
   - `posicionar`: Associa uma lista de posições `(x, y)` ao navio. Valida se o número de posições corresponde ao tamanho do navio.
   - `atacar`: Marca uma parte do navio como atingida se a posição estiver na lista de posições. Retorna `True` se acertou, `False` caso contrário.
   - `afundado`: Verifica se todas as partes do navio foram atingidas. Retorna `True` se o navio foi completamente destruído, `False` caso contrário.

3. Estado do Navio:
   - Inicial: Todas as partes do navio são marcadas como não atingidas.
   - Durante o jogo: As partes atingidas são marcadas como `True` na lista `atingido`.
   - Após ser afundado: Todas as posições na lista `atingido` são `True`.

4. Interface com Outras Classes:
   - Interage com a classe `Tabuleiro` para posicionar o navio e processar ataques.
   - Pode ser usada para verificar o estado do jogo (ex.: condição de vitória quando todos os navios forem afundados).

Requisitos mínimos:
   - Python 3.8 ou superior.

Objetivo:
Esta classe abstrai a lógica e o comportamento de um navio no jogo, permitindo que o estado de cada navio seja rastreado de forma independente. Ela é essencial para gerenciar a interação entre ataques e o estado do tabuleiro.

---

### Arquivo: turnos.py

Descrição e funcionalidade:

O arquivo `turnos.py` contém as funções responsáveis por gerenciar os turnos dos jogadores no jogo de Batalha Naval. Ele organiza as ações que podem ser realizadas por cada jogador durante seu turno, como ataques e uso de poderes, além de lidar com efeitos temporários aplicados ao tabuleiro.

Componentes principais:

1. Função `executar_turno`:
   - Responsável por executar o turno de um jogador.
   - Oferece ao jogador três opções: atacar, usar um poder ou desistir.
   - Lida com a entrada do jogador e processa as ações escolhidas.
   - Atualiza os tabuleiros (do jogador e do oponente) com base nos ataques e poderes usados.
   - Retorna o status do jogo após o turno:
     - `"continuar"`: O jogo segue normalmente.
     - `"desistir"`: O jogador desistiu, e o oponente vence.

2. Função `atualizar_temporarios`:
   - Gerencia os efeitos temporários que estão ativos no jogo.
   - Reduz o número de turnos restantes para cada efeito ativo.
   - Remove efeitos expirados do controle de estado.

3. Função `aplicar_efeitos_temporários`:
   - Aplica os efeitos temporários ao tabuleiro do oponente ou ao jogador.
   - Exemplo: "Nevoeiro" que oculta áreas do tabuleiro oponente por um número limitado de turnos.

4. Estrutura de gerenciamento de turnos temporários:
   - `turnos_temporarios`: Um dicionário que armazena os efeitos temporários aplicados, suas áreas de impacto e o número de turnos restantes.
   - Utilizado para aplicar e atualizar efeitos que afetam a visibilidade ou o comportamento do jogo.

5. Integração com outras partes do jogo:
   - Chama funções da classe `Tabuleiro` para atualizar o estado dos tabuleiros após ações.
   - Usa a função `usar_poder` do módulo `poderes` para processar habilidades especiais.
   - Converte entradas do jogador (ex.: "A 14") em coordenadas usando a função `entrada_para_coordenadas` do módulo `utils`.

Requisitos mínimos:
   - Python 3.8 ou superior.
   - Dependências:
     - `poderes.py`: Para o uso de habilidades especiais.
     - `utils.py`: Para conversão de entradas e utilitários de suporte.
     - Classe `Tabuleiro`: Para interação com os tabuleiros do jogo.

Objetivo:
O arquivo centraliza a lógica de execução de turnos e aplicação de efeitos temporários, permitindo uma experiência de jogo organizada e flexível. Ele garante que os jogadores alternem turnos, com suporte para ações avançadas como uso de poderes e gerenciamento de efeitos temporários.

---

### Arquivo: utils.py

Descrição e funcionalidade:

O arquivo `utils.py` contém funções auxiliares que facilitam o funcionamento do jogo de Batalha Naval. Ele centraliza conversões e interações essenciais para a lógica do jogo, como transformar entradas do usuário em coordenadas e gerenciar o posicionamento manual de navios.

Componentes principais:

1. Função `entrada_para_coordenadas`:
   - Converte uma entrada de texto no formato 'A 14' em coordenadas numéricas (linha, coluna) para uso interno no tabuleiro.
   - Valida a entrada e gera um erro se o formato for inválido.
   - Exemplo:
     - Entrada: `'A 14'`
     - Saída: `(0, 13)` (Linha 0, Coluna 13 no índice zero)

2. Função `posicionar_navios`:
   - Gerencia o posicionamento manual de navios no tabuleiro.
   - Exibe o estado atual do tabuleiro e a lista de navios disponíveis.
   - Permite ao jogador selecionar um navio, informar a posição inicial e escolher a orientação (horizontal ou vertical).
   - Valida as posições e orientações fornecidas antes de posicionar o navio no tabuleiro.
   - Remove o navio da lista de disponíveis após o posicionamento bem-sucedido.
   - Exemplo de interação:
     - Lista os navios disponíveis com suas dimensões.
     - Solicita ao jogador uma entrada como `'A 14'` para posicionamento inicial.
     - Orientação ('h' ou 'v') define como o navio será colocado.

Requisitos mínimos:
   - Python 3.8 ou superior.
   - Dependência:
     - `navio.py`: Para criar instâncias de navios e gerenciar seus atributos.

Objetivo:
O arquivo serve como um módulo de utilidades que auxilia na interação com os tabuleiros e na entrada do jogador. Ele abstrai e simplifica tarefas comuns, como conversão de entradas e validação de posições.

---

### Arquivo: poderes.py

Descrição e funcionalidade:

O arquivo `poderes.py` foi planejado para implementar funcionalidades adicionais ao jogo de Batalha Naval, utilizando poderes especiais que afetam a dinâmica do tabuleiro, adicionando uma camada estratégica ao jogo. Ele define diferentes poderes que os jogadores podem usar durante seus turnos e gerencia os efeitos temporários que esses poderes podem causar.

Componentes principais:

1. Poderes disponíveis e suas funções:
   - `poder_bombardeio`:
     - Ataca uma área 3x3 no tabuleiro do oponente, causando dano em todas as casas.
   - `poder_reconhecimento`:
     - Revela temporariamente uma área 3x3 no tabuleiro do oponente por 3 turnos.
   - `poder_nevoeiro`:
     - Esconde uma área 4x4 no próprio tabuleiro por 3 turnos, dificultando a visibilidade do oponente.
   - `poder_decoy`:
     - Cria um navio falso (decoy) em uma posição específica no próprio tabuleiro, visível ao oponente, por 5 turnos.
   - `poder_sonar`:
     - Revela todos os navios presentes em uma linha ou coluna específica do tabuleiro do oponente.

2. Função `usar_poder`:
   - Chama a função correspondente ao tipo de poder escolhido.
   - Garante a contagem de usos restantes do poder.
   - Valida se o tipo de poder é suportado.

3. Gerenciamento de efeitos temporários:
   - `atualizar_temporarios`:
     - Reduz a duração dos efeitos temporários a cada turno e remove os efeitos expirados.
   - `aplicar_efeitos_temporarios`:
     - Aplica os efeitos ativos, como esconder áreas ou revelar informações no tabuleiro.

4. Inicialização de poderes:
   - `inicializar_poderes`:
     - Cria a lista de poderes disponíveis para cada jogador, com a quantidade de usos baseada na quantidade de navios disponíveis no início do jogo.


Requisitos mínimos:
   - Python 3.8 ou superior.
   - Dependências:
     - `utils.py`: Para conversão de entradas e gerenciamento de posições no tabuleiro.
     - Classes `Tabuleiro` e `Navio`: Para manipulação do estado dos tabuleiros e navios.

Objetivo:
Os poderes introduzem mecânicas avançadas ao jogo, incentivando estratégias e aumentando a interação entre os jogadores. Eles ampliam a complexidade e tornam a experiência mais envolvente.

Justificativa da não implementação:
Devido à complexidade e ao tempo necessário para implementar uma lógica consistente e equilibrada, que funcionasse bem em um ambiente de terminal, os poderes não foram integrados na versão final do jogo. Apesar de seu potencial para enriquecer o gameplay, a prioridade foi dada à implementação e estabilização das mecânicas básicas de Batalha Naval.