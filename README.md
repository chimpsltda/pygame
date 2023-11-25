## Projeto Python de um jogo ---REDACTED---
### Autores: Bruno Machado Ferreira, Ernani Mendes da Fonseca Neto, Fábio Gomes de Souza e Ryan Henrique Nantes

## Descrição:
O jogo, feito com base na biblioteca Pygame, é um arcade 2D sobre matar slimes e conquistar os objetivos.
Bibliotecas:
- `paho-mqtt 1.6.1`
- `pygame 2.5.2`
- `Python 3.11.6`

### Gameplay
O personagem até o momento(22/11/2023) dispõe de 2 armas: Uma pistola de tiro único e uma escopeta que espalha projéteis. Use WASD para movimentar o personagem e o botão esquerdo do mouse para disparar sua arma.
- A mira é travada na posição do seu cursor.
- Inimigos vermelhos apenas passam na tela, sem atacar. Inimigos laranjas vão perseguir você sem parar.
- Objetivos surgirão pelo mapa e te dão recompensas de XP e Itens.(Possivelmente removido)

## Código
Esta versão do código foi modularizada para melhor organização e manutenção.
Segue abaixo uma explicação de cada módulo e suas funções:

### Drops
- Pedaços de código que configuram itens deixados por inimigos mortos.

### Entities
- Configura todas as entidades(Jogador, Monstros e Objetivos)
- Faz uso de alguns módulos das armas para interagir com projéteis.
- Configura as sprites mostradas em diferentes movimentos.

### GameData
- Guarda informações do funciomanento do jogo como velocidade de entidades e do jogador, cores e tamanho da tela.

### InventoryClass
- Armazena a matriz 3x5 que é o inventário do jogador.
- Itens obtidos serão adicionados em posições livres na matriz

### Jogador
- Armazena configurações do jogador(HP, dano das armas, hitbox)
- Controla o movimento do jogador ao apertar as teclas WASD

### main
- Arquivo principal. Deve ser executado para rodar o jogo.
- Apenas chama e usa as funções dos outros módulos.

### Menu(WIP)
- É a primeira tela apresentada ao rodar o jogo.
- Botões interativos e texturizados serão adicionados

### multi(WIP)
- Módulo responsável por conectar o jogo a um servidor MQTT(teoricamente)
- MQTT é muito difícil de implementar...

###  particulas
- Configura efeitos visuais

### WeaponClass
- Contém as classes de armas, suas manipulações e o funcionamento dos projéteis
- MUITO CUIDADO NAS ALTERAÇÕES! Este módulo é usado em grande parte do jogo.

### xpClass
- Configura e controla o XP deixado por inimigos mortos
- Permite que o jogador melhore atributos ao subir de nível(Ainda não funciona)
- Exibe a barra de XP