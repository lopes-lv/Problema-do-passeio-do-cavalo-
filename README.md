# ♞ O Problema do Passeio do Cavalo: Busca por Ciclos Fechados

Este repositório contém a implementação e evolução de algoritmos em Python para resolver o clássico **Problema do Passeio do Cavalo** (*Knight's Tour*) num tabuleiro de xadrez 8x8. 

O projeto destaca-se pela procura de **Ciclos Fechados**, explorando desde a movimentação básica e estocástica até algoritmos de procura exaustiva com heurísticas avançadas.

## 📖 Sobre o Projeto e o Conceito

O Passeio do Cavalo é um desafio matemático onde o objetivo é mover a peça do cavalo por todas as 64 casas de um tabuleiro sem repetir nenhuma. 

O foco principal deste trabalho é a exploração de **Ciclos**:
* **Ciclos Curtos:** Onde o cavalo retorna à casa inicial após alguns movimentos.
* **Ciclo Hamiltoniano (Passeio Fechado):** O objetivo final, onde o cavalo visita todas as 64 casas e termina exatamente a um movimento de distância da origem, permitindo o fecho perfeito do percurso.

## 🚀 Histórico de Versões e Evolução

O desenvolvimento foi dividido em três etapas principais, cada uma introduzindo novos conceitos de programação e otimização:

### 1. Versão Inicial (`cavalo_V.1.py`)
* **Lógica:** Implementação básica da movimentação do cavalo.
* **Características:** Coordenadas fixas no código e execução de uma sequência simples de até 8 movimentos.
* **Estado:** Versão experimental; serviu para validar a matemática dos saltos em "L" e identificar a necessidade de um sistema de memória para evitar repetições.

### 2. Versão Estocástica (`cavalo_V.2.py`)
* **Lógica:** Introdução de aleatoriedade e interação com o utilizador.
* **Características:** * O utilizador define o ponto de partida.
    * Utiliza a biblioteca `random` para escolher o próximo movimento válido.
    * Implementa uma lista de "casas feitas" para garantir que o cavalo não pise na mesma casa duas vezes.
* **Objetivo:** Tenta encontrar um ciclo de retorno à origem num limite de 10 iterações através de tentativas aleatórias.

### 3. Versão Avançada com Heurística (`CAVALO_V3.py`)
* **Lógica:** Recursividade (*Backtracking*) e Heurística de Warnsdorff.
* **Características:**
    * **Procura Exaustiva:** Tenta completar o passeio total de 64 casas.
    * **Otimização:** Implementa a **Regra de Warnsdorff**, que ordena os movimentos possíveis priorizando as casas com menos movimentos subsequentes, aumentando drasticamente a eficiência.
    * **Interface:** Visualização em tempo real do tabuleiro no terminal utilizando o caractere "♞".
    * **Telemetria:** Medição do tempo de execução e contagem total de movimentos tentados.

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3.x
* **Módulos Nativos:** `random` (V2) e `time` (V3).

## 💻 Como Executar

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/tour-do-cavalo.git
