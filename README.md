## Projeto Python de um jogo ---REDACTED---
### Autores: Bruno Machado Ferreira, Ernani Mendes da Fonseca Neto, Fábio Gomes de Souza e Ryan Henrique Nantes

## Descrição:
O jogo, feito com base na biblioteca Pygame, consiste de uma janela com os elementos gráficos nela.

### Gameplay
O personagem até o momento(30/08/2023) dispõe de 2 armas: Uma pistola de tiro único e uma escopeta que espalha projéteis.
Use WASD para movimentar o personagem e o botão esquerdo do mouse para disparar sua arma.
A mira é travada na posição do seu cursor.
Inimigos vermelhos apenas passam na tela, sem atacar.
Inimigos laranjas vão perseguir você sem parar. Não deixe que acumulem ao seu redor.
Objetivos surgirão pelo mapa e te dão recompensas de XP e Itens.

## Código
Esta versão do código foi modularizada para melhor organização e manutenção.
Segue abaixo uma explicação de cada pasta de módulos e seus conteúdos:

### Armas
- Contém as classes de armas, suas manipulações e o funcionamento dos projéteis
- As classes WeaponClass e ProjectileClass são usados e referenciadas em todos os módulos de armas. MUITO CUIDADO NAS ALTERAÇÕES!

### NTT
- Contém um único módulo que engloba todas as entidades(Player, Monstros e Objetivos)
- Faz uso de alguns módulos das armas.

### XP
- Contém um único módulo que engloba a quantia e a barra de XP