import os
import tkinter as tk
from tkinter import ttk
from datetime import datetime

# ====== Dados (FAQ) ======
def _data_dir():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "DATA"))

def _faq_path():
    return os.path.join(_data_dir(), "faq.csv")

def _load_faq():
    """
    Lê DATA/faq.csv no formato: pergunta;resposta
    Se não existir, usa um FAQ padrão.
    """
    path = _faq_path()
    faqs = []
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    if ";" in line:
                        q, a = line.split(";", 1)
                        faqs.append((q.strip(), a.strip()))
        except Exception:
            pass
    if not faqs:
        faqs = [
            ("Como a média é calculada?",
             "A média = (Prova1 + Prova2 + Trabalho) / 3. Se for 7.00 ou mais: Aprovado; senão: Reprovado."),
            ("Onde vejo minhas faltas?",
             "Na tela do aluno clique em “Atualizar”. O total aparece abaixo da tabela (Faltas: N)."),
            ("Minhas notas não apareceram",
             "As notas são lançadas pelo professor da sua matéria. Se estiver faltando, fale com o professor."),
            ("Quem altera minha senha?",
             "A alteração de senha é feita pela Direção (perfil Diretor no sistema)."),
        ]
    return faqs

# ====== UI do Chat ======
BGC_APP   = "#0f172a"  # fundo dark (slate-900)
BGC_ME    = "#1e293b"  # bolha do aluno
BGC_BOT   = "#14b8a6"  # bolha do bot (teal-500)
FG_LIGHT  = "#e2e8f0"  # texto claro
FG_DARK   = "#0f172a"  # texto escuro
BGC_PANEL = "#111827"  # painel inferior
BGC_BTN   = "#0ea5e9"  # botões de perguntas

def _add_bubble(chat_frame, text, who="bot"):
    """
    Adiciona uma 'bolha' de conversa (Label dentro de um Frame alinhado à esquerda/direita).
    who: "bot" ou "me"
    """
    wrapper = tk.Frame(chat_frame, bg=BGC_APP)
    wrapper.pack(fill="x", padx=6, pady=2, anchor="e" if who=="me" else "w")

    # avatar + bubble
    line = tk.Frame(wrapper, bg=BGC_APP)
    line.pack(anchor="e" if who=="me" else "w")

    # avatar
    avatar_txt = "🤖" if who == "bot" else "🧑"
    av = tk.Label(line, text=avatar_txt, bg=BGC_APP, fg=FG_LIGHT, font=("Segoe UI Emoji", 14))
    if who == "me":
        # usuário: avatar à direita
        msg_side = tk.RIGHT
    else:
        msg_side = tk.LEFT
    if who == "me":
        av.pack(side=tk.RIGHT, padx=(8,2))
    else:
        av.pack(side=tk.LEFT, padx=(2,8))

    # bolha
    if who == "bot":
        bg = BGC_BOT
        fg = FG_DARK
        anchor = "w"
        padx = (0, 40)
    else:
        bg = BGC_ME
        fg = FG_LIGHT
        anchor = "e"
        padx = (40, 0)

    bubble = tk.Label(
        line, text=text, bg=bg, fg=fg, justify="left", wraplength=460,
        font=("Segoe UI", 10), padx=10, pady=8
    )
    if who == "me":
        bubble.pack(side=tk.RIGHT, padx=padx)
    else:
        bubble.pack(side=tk.LEFT, padx=padx)

    # timestamp
    ts = tk.Label(wrapper,
        text=datetime.now().strftime("%H:%M"),
        bg=BGC_APP, fg="#94a3b8", font=("Segoe UI", 8))
    ts.pack(anchor="e" if who=="me" else "w", padx=12)

def abrir_chat(parent, aluno_nome: str):
    """
    Abre a janela do chat estilo IA (somente perguntas pré-definidas).
    """
    faqs = _load_faq()

    # ===== janela =====
    win = tk.Toplevel(parent)
    win.title("Assistente • Ajuda")
    win.geometry("760x520")
    win.minsize(640, 420)
    win.configure(bg=BGC_APP)

    # cabeçalho
    header = tk.Frame(win, bg=BGC_APP)
    header.pack(fill="x", padx=12, pady=(12, 4))
    tk.Label(header, text="Assistente do Aluno", bg=BGC_APP, fg=FG_LIGHT,
             font=("Segoe UI Semibold", 12)).pack(side="left")
    tk.Label(header, text="(clique em uma pergunta abaixo)", bg=BGC_APP, fg="#94a3b8",
             font=("Segoe UI", 9)).pack(side="left", padx=8)

    # ===== área de chat rolável =====
    body = tk.Frame(win, bg=BGC_APP)
    body.pack(fill="both", expand=True, padx=12, pady=(0, 8))

    canvas = tk.Canvas(body, bg=BGC_APP, highlightthickness=0)
    scrollbar = ttk.Scrollbar(body, orient="vertical", command=canvas.yview)
    chat_frame = tk.Frame(canvas, bg=BGC_APP)

    chat_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    canvas.create_window((0,0), window=chat_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # mensagem inicial
    _add_bubble(chat_frame, f"Olá, {aluno_nome}! Sou sua assistente. "
                            f"Escolha uma pergunta abaixo e eu respondo 😉", who="bot")

    # ===== painel de ações (filtro + botões de perguntas) =====
    panel = tk.Frame(win, bg=BGC_PANEL)
    panel.pack(fill="x", padx=0, pady=0)

    # filtro
    filt_wrap = tk.Frame(panel, bg=BGC_PANEL)
    filt_wrap.pack(fill="x", pady=(8, 0), padx=12)
    tk.Label(filt_wrap, text="Perguntas sugeridas",
             bg=BGC_PANEL, fg=FG_LIGHT, font=("Segoe UI", 10)).pack(side="left")
    filtro = tk.StringVar()
    ent = ttk.Entry(filt_wrap, textvariable=filtro, width=36)
    ent.pack(side="right")

    # grade de botões (rolável horizontal)
    btn_wrap = tk.Frame(panel, bg=BGC_PANEL)
    btn_wrap.pack(fill="x", padx=12, pady=(8, 10))

    btn_canvas = tk.Canvas(btn_wrap, height=120, bg=BGC_PANEL, highlightthickness=0)
    btn_scroll_x = ttk.Scrollbar(btn_wrap, orient="horizontal", command=btn_canvas.xview)
    btn_inner = tk.Frame(btn_canvas, bg=BGC_PANEL)

    btn_inner.bind(
        "<Configure>",
        lambda e: btn_canvas.configure(scrollregion=btn_canvas.bbox("all"))
    )
    btn_canvas.create_window((0,0), window=btn_inner, anchor="nw")
    btn_canvas.configure(xscrollcommand=btn_scroll_x.set)

    btn_canvas.pack(side="top", fill="x", expand=True)
    btn_scroll_x.pack(side="bottom", fill="x")

    # estilo para botões "pill"
    def make_qbtn(parent, text, cmd):
        b = tk.Button(
            parent, text=text, command=cmd,
            bg=BGC_BTN, fg="white", activebackground="#0284c7", activeforeground="white",
            relief="flat", padx=12, pady=8, wraplength=200, justify="left",
            font=("Segoe UI", 9)
        )
        return b

    # constrói botões (2 colunas por linha, mas dentro de um fluxo horizontal)
    buttons = []

    def rebuild_buttons():
        for w in buttons:
            w.destroy()
        buttons.clear()

        term = filtro.get().strip().lower()
        filtered = [(q, a) for (q, a) in faqs if not term or term in q.lower()]
        if not filtered:
            lbl = tk.Label(btn_inner, text="Nenhuma pergunta encontrada.",
                           bg=BGC_PANEL, fg="#cbd5e1", font=("Segoe UI", 10))
            lbl.grid(row=0, column=0, padx=6, pady=6)
            buttons.append(lbl)
            return

        col = 0
        row = 0
        for q, a in filtered:
            def on_click(qq=q, aa=a):
                # adiciona a pergunta como se fosse do usuário
                _add_bubble(chat_frame, qq, who="me")
                # pequena “pausa” para dar sensação de resposta
                chat_frame.after(150, lambda: _add_bubble(chat_frame, aa, who="bot"))
                # rola pro fim
                chat_frame.after(50, lambda: canvas.yview_moveto(1.0))

            btn = make_qbtn(btn_inner, "• " + q, on_click)
            btn.grid(row=row, column=col, padx=6, pady=6, sticky="w")
            buttons.append(btn)

            col += 1
            if col >= 2:  # 2 colunas
                col = 0
                row += 1

    filtro.trace_add("write", lambda *_: rebuild_buttons())
    rebuild_buttons()

    # rolar para o fim sempre que algo novo entrar
    def _auto_scroll(_event=None):
        canvas.yview_moveto(1.0)
    chat_frame.bind("<Map>", _auto_scroll)