# Laby com Pygame

Bem-vindo ao Laby, um jogo de labirinto feito com a linguagem Python utilizando a biblioteca Pygame. O Laby gera, a cada jogada, labirintos aleatórios feitos com o algoritmo de Prim (para mais informações, visite: https://pt.wikipedia.org/wiki/Algoritmo_de_Prim). 

O objetivo do jogo é escapar desses labirintos antes do tempo acabar. 
As teclas de movimento do jogador são WASD ou setas (← → ↑ ↓).

## Tecnologias utilizadas
Python V.: 3.11.1 || Pygame V.: 2.4.0

OBS.: É obrigatória a instalação manual do Python na versão citada acima para ser possível a criação do ambiente virtual e instalação das dependências do projeto.

- Windows 8+

https://www.python.org/ftp/python/3.11.1/python-3.11.1-amd64.exe

- macOS 10.9+

https://www.python.org/ftp/python/3.11.1/python-3.11.1-macos11.pkg

## Configurando o ambiente virtual
* No seu terminal, navegue até a pasta raiz do projeto e execute o seguinte comando para criar um ambiente virtual:

  <code>python -m venv nome_da_virtualenv</code> (exemplo: venv)

* Rode o comando de acordo com seu sistema para ativar seu ambiente virtual:

  <code>.\nome_da_virtualenv\Scripts\activate</code> (Windows)

  <code>source nome_da_virtualenv/bin/activate</code> (Linux ou macOS)

## Instalando as dependências
* Com o ambiente virtual **ativado**, instale as dependências do Laby com o seguinte comando:

  <code>pip install -r requirements.txt</code>

## Como executar o Laby?
* Execute o arquivo principal do jogo conforme abaixo:

  <code>python laby.py</code>
