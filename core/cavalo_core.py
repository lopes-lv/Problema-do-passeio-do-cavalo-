"""
Utilidades compartilhadas entre os scripts do Passeio do Cavalo
(cavalo_V1.py, cavalo_V2.py, CAVALO_V3.py) e a interface gráfica
(interface_cavalo.py).
"""

MOVIMENTO = [[2, -1], [2, 1], [-2, 1], [-2, -1], [1, 2], [1, -2], [-1, 2], [-1, -2]]


def native_to_pos(native):
    """Converte coordenadas (coluna, linha) 1..8, como usadas nos scripts,
    para (col, lin) 0..7, usadas pelo tabuleiro da interface gráfica.

    Retorna None quando a coordenada está fora do tabuleiro (usado pelos
    passos inválidos da Versão 1).
    """
    if native is None:
        return None
    c, l = native
    if 1 <= c <= 8 and 1 <= l <= 8:
        return (c - 1, l - 1)
    return None
