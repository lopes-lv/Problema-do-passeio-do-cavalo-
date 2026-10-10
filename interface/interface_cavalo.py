"""
Passeio do Cavalo -- Visualizador (interface grafica em Tkinter)

Anima, num tabuleiro 8x8, o mesmo algoritmo que roda em cavalo_V1.py,
cavalo_V2.py e CAVALO_V3.py -- esta interface IMPORTA e chama a função
passeio() de cada um desses arquivos diretamente (veja _build_frames() logo
abaixo). Ou seja: qualquer alteração na lógica de movimentação feita nesses
três arquivos passa a valer aqui automaticamente, sem precisar tocar neste
arquivo.

Requisitos: apenas a biblioteca padrao do Python (tkinter).
Para executar:  python interface_cavalo.py
"""

import tkinter as tk
from tkinter import ttk

from core import cavalo_core
from algoritmos import cavalo_V1
from algoritmos import cavalo_V2
from algoritmos import CAVALO_V3 as cavalo_V3

COLORS = {
    "paper": "#eef1e9",
    "surface": "#ffffff",
    "surface2": "#f7f8f3",
    "ink": "#1b201c",
    "ink_dim": "#5b625a",
    "line": "#d8ddd0",
    "board_light": "#eef0e2",
    "board_dark": "#5f8768",
    "visited_light": "#dbe6f5",
    "visited_dark": "#4a6f7a",
    "accent": "#3860a8",
    "accent_soft": "#dbe6f5",
    "good": "#2f7d4d",
    "good_soft": "#dcefe1",
    "bad": "#b23a30",
    "bad_soft": "#f6dfdc",
    "warn": "#a8701c",
    "warn_soft": "#f3e6d0",
}

VERSION_INFO = {
    1: {
        "badge": "SEM BUSCA REAL",
        "title": "Sequência fixa pré-programada",
        "desc": ("Aplica, em ordem inversa, uma lista fixa de 8 deslocamentos de "
                 "cavalo a partir da posição atual -- sem verificar se uma casa já "
                 "foi visitada. Se um passo cair fora do tabuleiro, ele é ignorado "
                 "e a posição não muda. Não é um algoritmo de busca: é um script "
                 "determinístico de tentativa única."),
        "extra_lbl": "Passos inválidos",
        "defaults": (1, 3),
    },
    2: {
        "badge": "BUSCA ESTOCÁSTICA",
        "title": "Passeio aleatório com rejeição",
        "desc": ("A cada uma das até 10 iterações, sorteia um movimento entre os "
                 "que respeitam os limites do tabuleiro e só o aceita se a casa "
                 "ainda não tiver sido visitada -- senão, sorteia de novo. Não há "
                 "exploração sistemática nem retrocesso real: é tentativa-e-erro "
                 "(rejection sampling) puro."),
        "extra_lbl": "Sorteios rejeitados",
        "defaults": (4, 4),
    },
    3: {
        "badge": "BACKTRACKING + HEURÍSTICA",
        "title": "Busca em profundidade com a Regra de Warnsdorff",
        "desc": ("Em cada casa, ordena os movimentos possíveis pelo número de "
                 "saídas futuras (menor primeiro) e tenta o mais restrito antes -- "
                 "a heurística de Warnsdorff. Quando não há saída, retrocede "
                 "(backtracking) e tenta a próxima opção. Como a 64ª casa "
                 "precisa ser, de novo, a casa inicial, o algoritmo busca "
                 "especificamente um passeio FECHADO (um ciclo)."),
        "extra_lbl": "Retrocessos",
        "defaults": (1, 1),
    },
}


# --------------------------------------------------------------------------
# Adaptador -- chama diretamente a função passeio() de cada script original
# (cavalo_V1.py, cavalo_V2.py, CAVALO_V3.py) e converte os eventos que ela
# produz em "frames" prontos para a interface desenhar. Nenhuma lógica de
# movimentação vive aqui: ela inteira está nos três arquivos importados.
# --------------------------------------------------------------------------

def _build_frames(eventos):
    frames = []
    for evento in eventos:
        frame = dict(evento)
        frame["pos"] = cavalo_core.native_to_pos(evento.get("native"))
        if "removed_native" in evento:
            frame["removed"] = cavalo_core.native_to_pos(evento["removed_native"])
        frames.append(frame)
    return frames


def simulate_v1(start_c, start_l):
    return _build_frames(cavalo_V1.passeio(start_c, start_l))


def simulate_v2(start_c, start_l):
    return _build_frames(cavalo_V2.passeio(start_c, start_l))


def simulate_v3(start_col1, start_row1):
    return _build_frames(cavalo_V3.passeio(start_col1, start_row1))


SIMULATORS = {1: simulate_v1, 2: simulate_v2, 3: simulate_v3}
LOGGABLE = {"start", "move", "backtrack", "success", "fail"}


# --------------------------------------------------------------------------
# Interface grafica
# --------------------------------------------------------------------------

class KnightTourApp:
    CELL = 50
    MARGIN_L = 28
    MARGIN_T = 22

    def __init__(self, root):
        self.root = root
        root.title("Passeio do Cavalo -- Visualizador")
        root.configure(bg=COLORS["paper"])
        root.resizable(True, True)
        root.minsize(760, 660)
        root.columnconfigure(0, weight=1)
        root.rowconfigure(1, weight=1)

        self.fullscreen = False
        root.bind("<F11>", self._toggle_fullscreen)
        root.bind("<Escape>", self._exit_fullscreen)

        self.style = ttk.Style()
        try:
            self.style.theme_use("clam")
        except tk.TclError:
            pass
        self._style_widgets()

        self.current_version = 3
        self.frames = []
        self.idx = 0
        self.playing = False
        self.after_id = None
        self.speed_ms = tk.IntVar(value=150)
        self.state = {"visited_order": [], "knight_pos": None,
                      "move_count": 0, "back_count": 0, "rej_count": 0}
        self.log_lines = []

        self._build_header()
        self._build_main()
        self._build_log()

        self.cell_items = {}
        self.order_items = {}
        self._build_board()

        self.select_version(3)

    # ---- estilos -------------------------------------------------------

    def _style_widgets(self):
        s = self.style
        s.configure("TFrame", background=COLORS["paper"])
        s.configure("Card.TFrame", background=COLORS["surface"])
        s.configure("TLabel", background=COLORS["paper"], foreground=COLORS["ink"])
        s.configure("Card.TLabel", background=COLORS["surface"], foreground=COLORS["ink"])
        s.configure("Dim.TLabel", background=COLORS["surface"], foreground=COLORS["ink_dim"])
        s.configure("Badge.TLabel", background=COLORS["accent_soft"], foreground=COLORS["accent"],
                    font=("Consolas", 9, "bold"), padding=(6, 2))
        s.configure("Title.TLabel", background=COLORS["surface"], foreground=COLORS["ink"],
                    font=("Georgia", 13, "bold"))
        s.configure("Header.TLabel", background=COLORS["paper"], foreground=COLORS["ink"],
                    font=("Georgia", 20, "bold"))
        s.configure("Sub.TLabel", background=COLORS["paper"], foreground=COLORS["ink_dim"],
                    font=("Segoe UI", 10))
        s.configure("TNotebook", background=COLORS["paper"], borderwidth=0)
        s.configure("TNotebook.Tab", background=COLORS["surface2"], foreground=COLORS["ink_dim"],
                    padding=(14, 8), font=("Segoe UI", 10, "bold"))
        s.map("TNotebook.Tab",
              background=[("selected", COLORS["accent"])],
              foreground=[("selected", "#ffffff")])
        s.configure("TButton", background=COLORS["surface2"], foreground=COLORS["ink"],
                    font=("Segoe UI", 9, "bold"), padding=(8, 6))
        s.map("TButton", background=[("active", COLORS["accent_soft"])])
        s.configure("Primary.TButton", background=COLORS["accent"], foreground="#ffffff",
                    font=("Segoe UI", 9, "bold"), padding=(8, 6))
        s.map("Primary.TButton", background=[("active", COLORS["accent"])])
        s.configure("TEntry", fieldbackground=COLORS["surface2"], foreground=COLORS["ink"])
        s.configure("Horizontal.TScale", background=COLORS["surface"])

    # ---- construcao da UI -----------------------------------------------

    def _build_header(self):
        header = ttk.Frame(self.root, padding=(18, 16, 18, 6))
        header.grid(row=0, column=0, sticky="ew")
        ttk.Label(header, text="♞ Passeio do Cavalo", style="Header.TLabel").pack(anchor="w")
        ttk.Label(header,
                  text="Mesma lógica de cavalo_V.1.py, cavalo_V.2.py e CAVALO_V3.py, "
                       "animada num tabuleiro.  (F11: tela cheia · Esc: sair)",
                  style="Sub.TLabel").pack(anchor="w")

    def _build_main(self):
        main = ttk.Frame(self.root, padding=(18, 0))
        main.grid(row=1, column=0, sticky="")

        left = ttk.Frame(main, width=330)
        left.grid(row=0, column=0, sticky="n", padx=(0, 16))
        right = ttk.Frame(main)
        right.grid(row=0, column=1, sticky="n")

        # tabs (versoes) ---------------------------------------------------
        self.notebook = ttk.Notebook(left)
        self.notebook.add(ttk.Frame(self.notebook), text="Versão 1")
        self.notebook.add(ttk.Frame(self.notebook), text="Versão 2")
        self.notebook.add(ttk.Frame(self.notebook), text="Versão 3")
        self.notebook.select(2)
        self.notebook.pack(fill="x", pady=(0, 10))
        self.notebook.bind("<<NotebookTabChanged>>", self._on_tab_changed)

        # descricao ----------------------------------------------------------
        desc_card = ttk.Frame(left, style="Card.TFrame", padding=14)
        desc_card.pack(fill="x", pady=(0, 10))
        self.badge_lbl = ttk.Label(desc_card, style="Badge.TLabel", text="")
        self.badge_lbl.pack(anchor="w")
        self.title_lbl = ttk.Label(desc_card, style="Title.TLabel", text="", wraplength=290)
        self.title_lbl.pack(anchor="w", pady=(6, 4))
        self.desc_lbl = ttk.Label(desc_card, style="Dim.TLabel", text="", wraplength=290,
                                   justify="left")
        self.desc_lbl.pack(anchor="w")

        # posicao inicial ------------------------------------------------
        pos_card = ttk.Frame(left, style="Card.TFrame", padding=14)
        pos_card.pack(fill="x", pady=(0, 10))
        row = ttk.Frame(pos_card, style="Card.TFrame")
        row.pack(fill="x")
        col_box = ttk.Frame(row, style="Card.TFrame")
        col_box.pack(side="left", expand=True, fill="x", padx=(0, 6))
        ttk.Label(col_box, text="COLUNA (1-8)", style="Dim.TLabel",
                  font=("Segoe UI", 8, "bold")).pack(anchor="w")
        self.in_col = tk.Spinbox(col_box, from_=1, to=8, width=6,
                                  font=("Consolas", 12), justify="center")
        self.in_col.pack(fill="x")
        lin_box = ttk.Frame(row, style="Card.TFrame")
        lin_box.pack(side="left", expand=True, fill="x", padx=(6, 0))
        ttk.Label(lin_box, text="LINHA (1-8)", style="Dim.TLabel",
                  font=("Segoe UI", 8, "bold")).pack(anchor="w")
        self.in_lin = tk.Spinbox(lin_box, from_=1, to=8, width=6,
                                  font=("Consolas", 12), justify="center")
        self.in_lin.pack(fill="x")
        ttk.Button(pos_card, text="Gerar nova simulação", style="Primary.TButton",
                   command=self.run_simulation).pack(fill="x", pady=(10, 0))

        # transporte ------------------------------------------------------
        trans_card = ttk.Frame(left, style="Card.TFrame", padding=14)
        trans_card.pack(fill="x", pady=(0, 10))
        trow = ttk.Frame(trans_card, style="Card.TFrame")
        trow.pack(fill="x")
        ttk.Button(trow, text="⏮ Início", command=self.jump_to_start).pack(
            side="left", expand=True, fill="x", padx=2)
        ttk.Button(trow, text="◀", width=3, command=self.step_back).pack(
            side="left", padx=2)
        self.play_btn = ttk.Button(trow, text="▶ Play", style="Primary.TButton",
                                    command=self.toggle_play)
        self.play_btn.pack(side="left", expand=True, fill="x", padx=2)
        ttk.Button(trow, text="Fim ⏭", command=self.jump_to_end).pack(
            side="left", expand=True, fill="x", padx=2)

        speed_row = ttk.Frame(trans_card, style="Card.TFrame")
        speed_row.pack(fill="x", pady=(10, 0))
        ttk.Label(speed_row, text="VELOCIDADE", style="Dim.TLabel",
                  font=("Segoe UI", 8, "bold")).pack(side="left")
        self.speed_scale = ttk.Scale(speed_row, from_=30, to=500, orient="horizontal",
                                      variable=self.speed_ms, command=self._on_speed_change)
        self.speed_scale.pack(side="left", expand=True, fill="x", padx=8)
        self.speed_lbl = ttk.Label(speed_row, style="Dim.TLabel", text="150 ms",
                                    font=("Consolas", 9))
        self.speed_lbl.pack(side="left")

        self.status_lbl = tk.Label(trans_card, text="Pronto.", font=("Consolas", 10),
                                    bg=COLORS["surface2"], fg=COLORS["ink"], anchor="w",
                                    padx=8, pady=8, wraplength=290, justify="left")
        self.status_lbl.pack(fill="x", pady=(10, 0))

        # estatisticas ------------------------------------------------------
        stats_card = ttk.Frame(left, style="Card.TFrame", padding=14)
        stats_card.pack(fill="x")
        grid = ttk.Frame(stats_card, style="Card.TFrame")
        grid.pack(fill="x")
        self.stat_visited = self._build_stat(grid, "Casas visitadas", 0, 0)
        self.stat_step = self._build_stat(grid, "Passo da simulação", 0, 1)
        self.stat_extra = self._build_stat(grid, "Retrocessos", 1, 0)
        self.stat_moves = self._build_stat(grid, "Movimentos aceitos", 1, 1)
        grid.columnconfigure(0, weight=1)
        grid.columnconfigure(1, weight=1)

        # tabuleiro ---------------------------------------------------------
        board_card = ttk.Frame(right, style="Card.TFrame", padding=14)
        board_card.pack()
        w = self.MARGIN_L + 8 * self.CELL
        h = self.MARGIN_T + 8 * self.CELL
        self.canvas = tk.Canvas(board_card, width=w, height=h,
                                 bg=COLORS["surface"], highlightthickness=0)
        self.canvas.pack()

    def _build_stat(self, parent, label, r, c):
        box = tk.Frame(parent, bg=COLORS["surface2"], padx=10, pady=8)
        box.grid(row=r, column=c, sticky="nsew", padx=3, pady=3)
        num = tk.Label(box, text="0", font=("Consolas", 15), bg=COLORS["surface2"],
                        fg=COLORS["ink"])
        num.pack(anchor="w")
        tk.Label(box, text=label.upper(), font=("Segoe UI", 7, "bold"),
                 bg=COLORS["surface2"], fg=COLORS["ink_dim"]).pack(anchor="w")
        return num

    def _build_log(self):
        log_card = ttk.Frame(self.root, style="Card.TFrame", padding=14)
        log_card.grid(row=2, column=0, sticky="ew", padx=18, pady=(10, 18))
        ttk.Label(log_card, text="Registro de movimentos", style="Title.TLabel").pack(anchor="w")
        text_frame = ttk.Frame(log_card, style="Card.TFrame")
        text_frame.pack(fill="both", pady=(8, 0))
        self.log_text = tk.Text(text_frame, height=8, font=("Consolas", 9),
                                 bg=COLORS["surface2"], fg=COLORS["ink_dim"],
                                 relief="flat", wrap="none", state="disabled")
        scroll = ttk.Scrollbar(text_frame, orient="vertical", command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scroll.set)
        self.log_text.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

    def _build_board(self):
        for r in range(8):
            for c in range(8):
                x0 = self.MARGIN_L + c * self.CELL
                y0 = self.MARGIN_T + r * self.CELL
                x1, y1 = x0 + self.CELL, y0 + self.CELL
                base = COLORS["board_light"] if (r + c) % 2 == 0 else COLORS["board_dark"]
                rect = self.canvas.create_rectangle(x0, y0, x1, y1, fill=base,
                                                      outline=COLORS["line"], width=1)
                order_txt = self.canvas.create_text(x1 - 6, y1 - 6, anchor="se", text="",
                                                      font=("Consolas", 8), fill=COLORS["ink_dim"])
                self.cell_items[(c, r)] = rect
                self.order_items[(c, r)] = order_txt
        for c in range(8):
            x = self.MARGIN_L + c * self.CELL + self.CELL / 2
            self.canvas.create_text(x, self.MARGIN_T / 2, text=str(c + 1),
                                     font=("Consolas", 9), fill=COLORS["ink_dim"])
        for r in range(8):
            y = self.MARGIN_T + r * self.CELL + self.CELL / 2
            self.canvas.create_text(self.MARGIN_L / 2, y, text=str(r + 1),
                                     font=("Consolas", 9), fill=COLORS["ink_dim"])
        self.knight_item = self.canvas.create_text(0, 0, text="♞",
                                                     font=("Segoe UI Symbol", 26),
                                                     fill=COLORS["ink"])

    # ---- selecao de versao / geracao de simulacao -----------------------

    def _on_tab_changed(self, _event=None):
        self.current_version = self.notebook.index(self.notebook.select()) + 1
        info = VERSION_INFO[self.current_version]
        self.badge_lbl.configure(text=info["badge"])
        self.title_lbl.configure(text=info["title"])
        self.desc_lbl.configure(text=info["desc"])
        c, l = info["defaults"]
        self.in_col.delete(0, "end"); self.in_col.insert(0, str(c))
        self.in_lin.delete(0, "end"); self.in_lin.insert(0, str(l))
        self.run_simulation()

    def run_simulation(self):
        self.pause()
        try:
            col = max(1, min(8, int(self.in_col.get())))
        except ValueError:
            col = VERSION_INFO[self.current_version]["defaults"][0]
        try:
            lin = max(1, min(8, int(self.in_lin.get())))
        except ValueError:
            lin = VERSION_INFO[self.current_version]["defaults"][1]
        self.in_col.delete(0, "end"); self.in_col.insert(0, str(col))
        self.in_lin.delete(0, "end"); self.in_lin.insert(0, str(lin))

        self.frames = SIMULATORS[self.current_version](col, lin)
        self.jump_to_start()

    def select_version(self, v):
        self.notebook.select(v - 1)
        self._on_tab_changed()

    # ---- tela cheia ---------------------------------------------------------

    def _toggle_fullscreen(self, _event=None):
        self.fullscreen = not self.fullscreen
        self.root.attributes("-fullscreen", self.fullscreen)

    def _exit_fullscreen(self, _event=None):
        if self.fullscreen:
            self.fullscreen = False
            self.root.attributes("-fullscreen", False)

    # ---- player -----------------------------------------------------------

    def apply_forward(self, f):
        t = f["type"]
        if t == "start":
            self.state["visited_order"] = [f["pos"]]
            self.state["knight_pos"] = f["pos"]
        elif t == "move":
            self.state["visited_order"].append(f["pos"])
            self.state["knight_pos"] = f["pos"]
            self.state["move_count"] += 1
        elif t == "backtrack":
            self.state["visited_order"].pop()
            self.state["knight_pos"] = f["pos"]
            self.state["back_count"] += 1
        elif t == "rejected":
            self.state["rej_count"] += 1
        if t in LOGGABLE:
            self.log_lines.append(f)

    def undo_frame(self, f):
        t = f["type"]
        if t == "move":
            self.state["visited_order"].pop()
            self.state["knight_pos"] = (self.state["visited_order"][-1]
                                         if self.state["visited_order"] else self.state["knight_pos"])
            self.state["move_count"] -= 1
        elif t == "backtrack":
            self.state["visited_order"].append(f["removed"])
            self.state["knight_pos"] = f["removed"]
            self.state["back_count"] -= 1
        elif t == "rejected":
            self.state["rej_count"] -= 1
        if t in LOGGABLE and self.log_lines:
            self.log_lines.pop()

    def step_forward(self):
        if self.idx >= len(self.frames) - 1:
            self.pause()
            return False
        self.idx += 1
        self.apply_forward(self.frames[self.idx])
        self.refresh()
        return True

    def step_back(self):
        if self.idx <= 0:
            return False
        self.pause()
        self.undo_frame(self.frames[self.idx])
        self.idx -= 1
        self.refresh()
        return True

    def jump_to_start(self):
        self.pause()
        self.idx = 0
        self.log_lines = []
        first = self.frames[0]
        self.state = {"visited_order": [first["pos"]], "knight_pos": first["pos"],
                      "move_count": 0, "back_count": 0, "rej_count": 0}
        self.log_lines.append(first)
        self.refresh()

    def jump_to_end(self):
        self.pause()
        while self.idx < len(self.frames) - 1:
            self.idx += 1
            self.apply_forward(self.frames[self.idx])
        self.refresh()

    def toggle_play(self):
        if self.playing:
            self.pause()
        else:
            self.play()

    def play(self):
        if self.idx >= len(self.frames) - 1:
            return
        self.playing = True
        self.play_btn.configure(text="⏸ Pausar")
        self._schedule_tick()

    def _schedule_tick(self):
        if not self.playing:
            return
        went = self.step_forward()
        if went and self.idx < len(self.frames) - 1:
            self.after_id = self.root.after(int(self.speed_ms.get()), self._schedule_tick)
        else:
            self.pause()

    def pause(self):
        self.playing = False
        self.play_btn.configure(text="▶ Play")
        if self.after_id is not None:
            self.root.after_cancel(self.after_id)
            self.after_id = None

    def _on_speed_change(self, _value=None):
        self.speed_lbl.configure(text=f"{int(self.speed_ms.get())} ms")

    # ---- render -----------------------------------------------------------

    def refresh(self):
        self._render_board()
        self._render_stats()
        self._render_status()
        self._render_log()

    def _cell_base_color(self, c, r):
        return COLORS["board_light"] if (r + c) % 2 == 0 else COLORS["board_dark"]

    def _render_board(self):
        for (c, r), rect in self.cell_items.items():
            self.canvas.itemconfig(rect, fill=self._cell_base_color(c, r),
                                    outline=COLORS["line"], width=1)
            self.canvas.itemconfig(self.order_items[(c, r)], text="")

        order = self.state["visited_order"]
        for i, (c, r) in enumerate(order):
            base_dark = (r + c) % 2 == 1
            fill = COLORS["visited_dark"] if base_dark else COLORS["visited_light"]
            self.canvas.itemconfig(self.cell_items[(c, r)], fill=fill)
            self.canvas.itemconfig(self.order_items[(c, r)], text=str(i + 1))
            if i == len(order) - 1:
                self.canvas.itemconfig(self.cell_items[(c, r)], outline=COLORS["accent"], width=3)

        f = self.frames[self.idx] if self.frames else None
        if f:
            if f["type"] in ("try", "rejected") and f.get("pos"):
                c, r = f["pos"]
                color = COLORS["warn_soft"] if f["type"] == "try" else COLORS["bad_soft"]
                self.canvas.itemconfig(self.cell_items[(c, r)], fill=color)
            if f["type"] == "backtrack" and f.get("removed"):
                c, r = f["removed"]
                self.canvas.itemconfig(self.cell_items[(c, r)], fill=COLORS["bad_soft"])

        if self.state["knight_pos"] is not None:
            c, r = self.state["knight_pos"]
            x = self.MARGIN_L + c * self.CELL + self.CELL / 2
            y = self.MARGIN_T + r * self.CELL + self.CELL / 2
            self.canvas.coords(self.knight_item, x, y)
        self.canvas.tag_raise(self.knight_item)

    def _render_stats(self):
        info = VERSION_INFO[self.current_version]
        casas_distintas = len(set(self.state["visited_order"]))
        self.stat_visited.configure(text=f"{casas_distintas}/64")
        total = len(self.frames)
        self.stat_step.configure(text=f"{self.idx + 1}/{total}" if total else "0/0")
        self.stat_moves.configure(text=str(self.state["move_count"]))
        if self.current_version == 3:
            extra = self.state["back_count"]
        elif self.current_version == 2:
            extra = self.state["rej_count"]
        else:
            extra = sum(1 for f in self.frames[:self.idx + 1] if f["type"] == "invalid")
        self.stat_extra.configure(text=str(extra))
        self.stat_extra.master.winfo_children()[1].configure(text=info["extra_lbl"].upper())

    def _render_status(self):
        f = self.frames[self.idx] if self.frames else None
        if not f:
            self.status_lbl.configure(text="Pronto.", bg=COLORS["surface2"], fg=COLORS["ink"])
            return
        if f["type"] == "success":
            self.status_lbl.configure(text=f["label"], bg=COLORS["good_soft"], fg=COLORS["good"])
        elif f["type"] == "fail":
            self.status_lbl.configure(text=f["label"], bg=COLORS["bad_soft"], fg=COLORS["bad"])
        else:
            self.status_lbl.configure(text=f["label"], bg=COLORS["surface2"], fg=COLORS["ink"])

    def _render_log(self):
        self.log_text.configure(state="normal")
        self.log_text.delete("1.0", "end")
        for n, f in enumerate(self.log_lines, start=1):
            native = f.get("native")
            coord = f"({native[0]},{native[1]})" if native else "--"
            self.log_text.insert("end", f"{n:>3}  {coord:<9}  {f['label']}\n")
        self.log_text.see("end")
        self.log_text.configure(state="disabled")


def main():
    root = tk.Tk()
    KnightTourApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
