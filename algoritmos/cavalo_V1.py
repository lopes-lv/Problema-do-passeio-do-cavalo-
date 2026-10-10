"""
Passeio do Cavalo -- Versão 1

Sequência fixa de 8 deslocamentos (na ordem inversa da lista MOVIMENTO),
aplicada a partir da posição atual -- sem verificar se uma casa já foi
visitada. Não é um algoritmo de busca: é um script determinístico de
tentativa única.

#falta adicionar para ele nao volta para as casas que ja foi
# e resolver bug de as vezes ele nao voltar para a casa inicial

A função passeio() é usada tanto pelo modo texto (abaixo) quanto pela
interface gráfica (interface_cavalo.py) -- qualquer alteração na lógica de
movimentação feita aqui vale para os dois.
"""

from core.cavalo_core import MOVIMENTO


def passeio(coluna_inicial, linha_inicial):
    """Gera os eventos do passeio, um por vez.

    Cada evento é um dicionário com 'type' e 'label', e (quando aplicável)
    'native' com a coordenada (coluna, linha) em 1..8.
    """
    arm = [coluna_inicial, linha_inicial]
    movimento1 = MOVIMENTO[::-1]

    cur_c, cur_l = coluna_inicial, linha_inicial
    lista = []

    yield {"type": "start", "native": (cur_c, cur_l),
           "label": f"Início em ({cur_c},{cur_l})"}

    for i in range(8):
        moviexecut = movimento1[i]
        novoC = moviexecut[0] + cur_c
        novoL = moviexecut[1] + cur_l

        if 0 < novoC and 0 < novoL and 8 >= novoC and 8 >= novoL:
            cur_c, cur_l = novoC, novoL
            lista.append([novoC, novoL])
            yield {"type": "move", "index": i, "native": (cur_c, cur_l),
                   "label": f"Passo {i + 1}: desloc {moviexecut} → ({cur_c},{cur_l})"}
            if arm in lista:
                yield {"type": "success", "native": (cur_c, cur_l),
                       "label": "Casa inicial revisitada -- sequência interrompida."}
                return
        else:
            yield {"type": "invalid", "index": i, "native": (novoC, novoL),
                   "label": f"Passo {i + 1}: desloc {moviexecut} cairia em "
                            f"({novoC},{novoL}), fora do tabuleiro -- ignorado"}

    yield {"type": "fail", "native": (cur_c, cur_l),
           "label": "Sequência fixa de 8 passos concluída sem retornar à casa inicial."}


def _run_como_script():
    coluna_inicial = 1  # int(input('em qual coluna vai começar: '))
    linha_inicial = 3   # int(input('em qual linha vai começar: '))

    lista, fase, erro = [], [], []
    for evento in passeio(coluna_inicial, linha_inicial):
        if evento["type"] in ("move", "invalid"):
            erro.append(list(evento["native"]))
        if evento["type"] == "move":
            lista.append(list(evento["native"]))
            fase.append(f"fase{evento['index']}")

    print(lista)
    print(fase)
    print(erro)


if __name__ == "__main__":
    _run_como_script()
