---
estado: em andamento
proximo_passo: Revisar e commitar as mudanças pendentes no git (renomeação dos arquivos de versão + reorganização em camadas)
bloqueios:
---
# Passeio_do_cavalo

**Objetivo:** implementação e evolução de algoritmos em Python para o Problema do Passeio do Cavalo (8x8), com foco em ciclos fechados, mais uma interface gráfica em Tkinter.

## Tarefas
- [ ] Revisar e commitar as mudanças pendentes no git (renomeação de `cavalo_V.1.py`/`cavalo_V.2.py` para `cavalo_V1.py`/`cavalo_V2.py`, atualizações em `CAVALO_V3.py`/`README.md` e a reorganização em camadas abaixo)
- [x] Reorganizar o projeto em camadas: `core/` (utilidades compartilhadas), `algoritmos/` (as três versões) e `interface/` (visualizador Tkinter); imports, `CLAUDE.md` e `README.md` atualizados e testados

## Notas
Três versões implementadas (básica, estocástica, com heurística de Warnsdorff) mais `interface/interface_cavalo.py` (Tkinter) que anima qualquer uma das três. Estrutura em camadas: `core/cavalo_core.py`, `algoritmos/{cavalo_V1,cavalo_V2,CAVALO_V3}.py`, `interface/interface_cavalo.py`. Execução agora é via módulo, a partir da raiz: `python -m algoritmos.cavalo_V1` / `python -m interface.interface_cavalo`.
