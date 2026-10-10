"""
Passeio do Cavalo -- Versão 2

Passeio aleatório: a cada uma das até 10 iterações, sorteia um movimento
válido (dentro dos limites do tabuleiro) e só o aceita se a casa ainda não
tiver sido visitada -- senão, sorteia de novo. Sem exploração sistemática
nem retrocesso real: é tentativa-e-erro (rejection sampling) puro.

A função passeio() é usada tanto pelo modo texto (abaixo) quanto pela
interface gráfica (interface_cavalo.py) -- qualquer alteração na lógica de
movimentação feita aqui vale para os dois.
"""

import random

from core.cavalo_core import MOVIMENTO

# Protege contra a recursão infinita que o algoritmo original pode sofrer
# quando "movimentar" reencontra repetidamente casas já visitadas.
MAX_TENTATIVAS = 60


def passeio(coluna_inicial, linha_inicial):
    arm = [coluna_inicial, linha_inicial]
    onde = [[coluna_inicial, linha_inicial]]
    feito = []
    lista = []
    preso = [False]
    iteracao_atual = [0]

    yield {"type": "start", "native": (coluna_inicial, linha_inicial),
           "label": f"Início em ({coluna_inicial},{linha_inicial})"}

    def validar(dados):
        for i in range(8):
            moviexecut = dados[i]
            posiC = onde[0][0]
            posiL = onde[0][1]
            novoC = moviexecut[0] + posiC
            novoL = moviexecut[1] + posiL
            if 0 < novoC and 0 < novoL and 8 >= novoC and 8 >= novoL:
                novoC = novoC - posiC
                novoL = novoL - posiL
                lista.append([novoC, novoL])
        return

    def movimentar(dados, tentativas=0):
        if tentativas >= MAX_TENTATIVAS:
            preso[0] = True
            yield {"type": "fail", "native": (onde[0][0], onde[0][1]),
                   "label": "Preso em sorteios repetidos (limite de tentativas atingido "
                            "-- reflete o risco de recursão infinita do código original)."}
            return
        escolha = random.choice(dados)
        posiC = onde[0][0]
        posiL = onde[0][1]
        novoC = escolha[0] + posiC
        novoL = escolha[1] + posiL
        if 0 < novoC and 0 < novoL and 8 >= novoC and 8 >= novoL:
            if [novoC, novoL] not in feito:
                feito.append([novoC, novoL])
                onde.clear()
                onde.append([novoC, novoL])
                lista.clear()
                yield {"type": "move", "native": (novoC, novoL),
                       "label": f"Iteração {iteracao_atual[0]}: movimento aceito "
                                f"→ ({novoC},{novoL})"}
            else:
                yield {"type": "rejected", "native": (novoC, novoL),
                       "label": f"Iteração {iteracao_atual[0]}: sorteou ({novoC},{novoL}), "
                                f"já visitada -- sorteando de novo"}
                yield from movimentar(dados, tentativas + 1)
        return

    for i in range(10):
        iteracao_atual[0] = i + 1
        validar(MOVIMENTO)
        yield from movimentar(lista)
        if preso[0]:
            break
        if arm in onde:
            yield {"type": "success", "native": (onde[0][0], onde[0][1]),
                   "label": "Cavalo voltou para a posição inicial!"}
            break
    else:
        yield {"type": "fail", "native": (onde[0][0], onde[0][1]),
               "label": "Limite de 10 iterações atingido -- cavalo não conseguiu voltar."}


def _run_como_script():
    coluna_inicial = int(input('em qual coluna vai começar: '))
    linha_inicial = int(input('em qual linha vai começar: '))
    print("PRIMEIRA CASA E A COLUNA E A SEGUNDA A LINHA")
    print(f"posiçao inicial: {coluna_inicial, linha_inicial}")

    feito = []
    voltou = False
    for evento in passeio(coluna_inicial, linha_inicial):
        if evento["type"] == "move":
            feito.append(list(evento["native"]))
        elif evento["type"] == "success":
            voltou = True

    if voltou:
        print("CAVALO VOLTOU PARA POSIÇAO INICIAL")
    else:
        print("CAVALO NAO CONSEGUIU VOLTAR")
    print(f"movimentos feitos:{feito}")

    repetiu = False
    for i in range(len(feito)):
        for j in range(i + 1, len(feito)):
            if feito[i] == feito[j]:
                print(f"Listas iguais encontradas nos índices {i} e {j}: {feito[i]}")
                repetiu = True
    if not repetiu:
        print("NAO REPETIU MOVIMENTO")


if __name__ == "__main__":
    _run_como_script()
