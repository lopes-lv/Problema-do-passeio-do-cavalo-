"""
Passeio do Cavalo -- Versão 3

Busca em profundidade (DFS) com retrocesso (backtracking), guiada pela
Regra de Warnsdorff: em cada casa, ordena os movimentos possíveis pelo
número de saídas futuras (menor primeiro) e tenta o mais restrito antes.

Importante: como "casas_visitadas" começa vazia (a casa inicial não entra
nela) e a condição de vitória é `len(casas_visitadas) == 64`, o algoritmo
está, na verdade, procurando um PASSEIO FECHADO -- a 64ª casa visitada tem
de ser, de novo, a casa inicial (alcançada por um movimento de cavalo
válido a partir da 63ª). É um problema mais difícil que o passeio aberto.

A função passeio() é usada tanto pelo modo texto (abaixo) quanto pela
interface gráfica (interface_cavalo.py) -- qualquer alteração na lógica de
movimentação feita aqui vale para os dois.
"""

import time

from core.cavalo_core import MOVIMENTO

# Protege contra buscas muito longas: um passeio fechado pode exigir muito
# mais retrocesso do que um passeio aberto, dependendo da casa inicial.
MAX_EVENTOS = 40000


def passeio(coluna_inicial, linha_inicial):
    pos_atual = [coluna_inicial - 1, linha_inicial - 1]
    casas_visitadas = []
    movimentos_feitos = [0]
    contador_eventos = [0]
    abortado = [False]

    yield {"type": "start", "native": (coluna_inicial, linha_inicial),
           "label": f"Início em ({coluna_inicial},{linha_inicial})"}

    def numero_movi(pos1, pos2, movimento):
        movimentos_posiveis = []
        for i in range(8):
            novoC = pos1 + movimento[i][0]
            novoL = pos2 + movimento[i][1]
            if novoC >= 0 and novoC < 8 and novoL >= 0 and novoL < 8:
                if [novoC, novoL] not in casas_visitadas:
                    movimentos_posiveis.append([movimento[i][0], movimento[i][1]])
        return len(movimentos_posiveis)

    def validar_movimento(movimento):
        movimentos_possiveis = []
        for i in range(8):
            novoC = pos_atual[0] + movimento[i][0]
            novoL = pos_atual[1] + movimento[i][1]
            if novoC >= 0 and novoC < 8 and novoL >= 0 and novoL < 8:
                if [novoC, novoL] not in casas_visitadas:
                    movimentos_possiveis.append([movimento[i][0], movimento[i][1]])
        movimentos_possiveis.sort(
            key=lambda m: numero_movi(pos_atual[0] + m[0], pos_atual[1] + m[1], movimento))
        return movimentos_possiveis

    def movimentar(movimento_fazer):
        movimentos_feitos[0] += 1
        novoc = movimento_fazer[0]
        novol = movimento_fazer[1]
        nova_pos = [pos_atual[0] + novoc, pos_atual[1] + novol]
        casas_visitadas.append(nova_pos)
        pos_atual[0] = nova_pos[0]
        pos_atual[1] = nova_pos[1]
        contador_eventos[0] += 1
        yield {"type": "move", "native": (pos_atual[0] + 1, pos_atual[1] + 1),
               "label": f"Movimento {movimentos_feitos[0]} → "
                        f"({pos_atual[0] + 1},{pos_atual[1] + 1}), "
                        f"{len(casas_visitadas)}/64 casas"}
        if contador_eventos[0] > MAX_EVENTOS:
            abortado[0] = True

    def executar(movimento_possiveis):
        if abortado[0]:
            return False
        if len(movimento_possiveis) == 0:
            return False
        for i in range(len(movimento_possiveis)):
            pos_anterior = [pos_atual[0], pos_atual[1]]
            yield from movimentar(movimento_possiveis[i])
            if abortado[0]:
                return False
            if len(casas_visitadas) == 64:
                return True
            sucesso = yield from executar(validar_movimento(MOVIMENTO))
            if sucesso:
                return True
            else:
                removida = casas_visitadas.pop()
                pos_atual[0], pos_atual[1] = pos_anterior[0], pos_anterior[1]
                contador_eventos[0] += 1
                yield {"type": "backtrack", "native": (pos_atual[0] + 1, pos_atual[1] + 1),
                       "removed_native": (removida[0] + 1, removida[1] + 1),
                       "label": f"Sem saída em ({removida[0] + 1},{removida[1] + 1}) "
                                f"-- retrocede para ({pos_atual[0] + 1},{pos_atual[1] + 1})"}
                if contador_eventos[0] > MAX_EVENTOS:
                    abortado[0] = True
                    return False
        return False

    sucesso = yield from executar(validar_movimento(MOVIMENTO))

    if sucesso:
        yield {"type": "success", "native": (pos_atual[0] + 1, pos_atual[1] + 1),
               "label": f"Passeio fechado completo! 64 casas visitadas em "
                        f"{movimentos_feitos[0]} movimentos."}
    elif abortado[0]:
        yield {"type": "fail", "native": (pos_atual[0] + 1, pos_atual[1] + 1),
               "label": "Simulação interrompida: limite de passos de segurança atingido."}
    else:
        yield {"type": "fail", "native": (pos_atual[0] + 1, pos_atual[1] + 1),
               "label": "Não foi possível encontrar um passeio fechado a partir desta casa."}


def mostrar_posição(posicaoC, posicaoL):
    cavalo = "♞"
    for l in range(0, 8):
        print("\n")
        for c in range(0, 8):
            if c == posicaoC and l == posicaoL:
                print(f"  {cavalo} ", end="")
            else:
                print(" ⬜ ", end="")
    print("\n======================================\n")
    return


def _run_como_script():
    initC = int(input("Digite onde o cavalo vai começar \nComeçando pela coluna e depois a linha:\n")) - 1
    initL = int(input()) - 1

    if initC > 7 or initC < 0 or initL > 7 or initL < 0:
        print("Os valores não são aceitaveis \nDigite apenas numeros entre 1 a 8")

    pos_atual = [initC, initL]
    print(f"pos atual {pos_atual}")
    mostrar_posição(pos_atual[0], pos_atual[1])

    inicio = time.time()
    casas_visitadas = []
    movimentos_feitos = 0
    for evento in passeio(initC + 1, initL + 1):
        if evento["type"] == "move":
            movimentos_feitos += 1
            nc, nl = evento["native"][0] - 1, evento["native"][1] - 1
            casas_visitadas.append([nc, nl])
            mostrar_posição(nc, nl)
        elif evento["type"] == "backtrack":
            if casas_visitadas:
                casas_visitadas.pop()
    fim = time.time()

    print(f"A quantidade de movimentos feitos foi: {movimentos_feitos}\n"
          f"O tempo de duração foi de: {fim - inicio}")
    print(casas_visitadas)


if __name__ == "__main__":
    _run_como_script()
