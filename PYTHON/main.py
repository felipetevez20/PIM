import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date

from escola_wrapper import (
    login, cadastrar_usuario, atribuir_materia_professor,
    listar_alunos, salvar_notas3, registrar_falta,
    obter_materia_professor, obter_notas3, contar_faltas
)

from estilo import apply_theme, header_bar, card, style_tree_status
from chatbot import abrir_chat

APP_W, APP_H = 900, 560
PAGE_W, PAGE_H = 860, 500


def centralizar_janela(root, w, h):
    root.update_idletasks()
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    x = (sw - w) // 2
    y = (sh - h) // 2
    root.geometry(f"{w}x{h}+{x}+{y}")


def criar_pagina(parent):
    page = ttk.Frame(parent)
    page.pack(fill="both", expand=True, padx=20, pady=20)
    return page


class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sistema Escolar")

        apply_theme(self.root)
        self.root.resizable(False, False)
        centralizar_janela(self.root, APP_W, APP_H)

        self.container = ttk.Frame(self.root)
        self.container.pack(fill="both", expand=True)

        self.usuario_logado = None
        self.tipo_usuario = None

        self.mostrar_login()
        self.root.bind("<Return>", self._enter_atual)

    def limpar_tela(self):
        for w in self.container.winfo_children():
            w.destroy()

    def mostrar_login(self):
        self.usuario_logado = None
        self.tipo_usuario = None
        self.limpar_tela()
        LoginScreen(self)

    def mostrar_aluno(self, nome):
        self.usuario_logado = nome
        self.tipo_usuario = "aluno"
        self.limpar_tela()
        AlunoScreen(self, nome)

    def mostrar_professor(self, nome):
        self.usuario_logado = nome
        self.tipo_usuario = "professor"
        self.limpar_tela()
        ProfessorScreen(self, nome)

    def mostrar_diretor(self):
        self.usuario_logado = "diretor"
        self.tipo_usuario = "diretor"
        self.limpar_tela()
        DiretorScreen(self)

    def _enter_atual(self, _event):
        telas = self.container.winfo_children()
        if telas and hasattr(telas[0], "on_enter"):
            telas[0].on_enter()

    def run(self):
        self.root.mainloop()

#TeladeLogin
class LoginScreen:
    def __init__(self, app: App):
        self.app = app

        page = criar_pagina(app.container)
        header_bar(page, "Sistema Escolar", "Faça login para continuar", icon="🔐")

        frm = card(page)
        frm.pack(pady=8)

        self.usuario = tk.StringVar()
        self.senha = tk.StringVar()

        r = 0
        ttk.Label(frm, text="Usuário:").grid(row=r, column=0, sticky="e", padx=6, pady=8)
        ttk.Entry(frm, textvariable=self.usuario, width=28).grid(row=r, column=1, padx=6, pady=8)

        r += 1
        ttk.Label(frm, text="Senha:").grid(row=r, column=0, sticky="e", padx=6, pady=8)
        ttk.Entry(frm, textvariable=self.senha, show="*", width=28).grid(row=r, column=1, padx=6, pady=8)

        r += 1
        ttk.Button(
            frm,
            text="Entrar",
            style="Accent.TButton",
            command=self.entrar
        ).grid(row=r, column=0, columnspan=2, pady=10)

    def entrar(self):
        usuario = self.usuario.get().strip()
        senha = self.senha.get().strip()

        ok, tipo = login(usuario, senha)
        if not ok:
            messagebox.showerror("Login", "Usuário ou senha inválidos.")
            return

        if tipo == "diretor":
            self.app.mostrar_diretor()
        elif tipo == "professor":
            self.app.mostrar_professor(usuario)
        elif tipo == "aluno":
            self.app.mostrar_aluno(usuario)

    def on_enter(self):
        self.entrar()

#TelaDiretor
class DiretorScreen:
    def __init__(self, app: App):
        self.app = app
        page = criar_pagina(app.container)

        _, right = header_bar(
            page,
            "Diretor",
            "Gerencie usuários e matérias",
            icon="🧭"
        )
        ttk.Button(
            right,
            text="Logout",
            style="Secondary.TButton",
            command=self.app.mostrar_login
        ).pack()

        nb = ttk.Notebook(page)
        nb.pack(fill="both", expand=True, pady=6)

        tab_cadastro = ttk.Frame(nb)
        nb.add(tab_cadastro, text="Cadastrar Usuário")

        card_cadastro = card(tab_cadastro)
        card_cadastro.pack(padx=8, pady=12, fill="x")

        self.nome = tk.StringVar()
        self.tipo = tk.StringVar(value="aluno")
        self.senha = tk.StringVar()

        r = 0
        ttk.Label(card_cadastro, text="Nome:").grid(row=r, column=0, sticky="e", padx=6, pady=8)
        ttk.Entry(card_cadastro, textvariable=self.nome, width=28).grid(row=r, column=1, padx=6, pady=8)

        r += 1
        ttk.Label(card_cadastro, text="Tipo:").grid(row=r, column=0, sticky="e", padx=6, pady=8)
        ttk.Combobox(
            card_cadastro,
            textvariable=self.tipo,
            values=["aluno", "professor", "diretor"],
            state="readonly",
            width=25
        ).grid(row=r, column=1, padx=6, pady=8)

        r += 1
        ttk.Label(card_cadastro, text="Senha:").grid(row=r, column=0, sticky="e", padx=6, pady=8)
        ttk.Entry(card_cadastro, textvariable=self.senha, show="*", width=28).grid(row=r, column=1, padx=6, pady=8)

        ttk.Button(
            card_cadastro,
            text="Cadastrar",
            style="Accent.TButton",
            command=self.cadastrar_usuario_novo
        ).grid(row=r+1, column=0, columnspan=2, pady=10)

        tab_materia = ttk.Frame(nb)
        nb.add(tab_materia, text="Atribuir Matéria")

        card_materia = card(tab_materia)
        card_materia.pack(padx=8, pady=12, fill="x")

        self.prof = tk.StringVar()
        self.materia = tk.StringVar()

        r = 0
        ttk.Label(card_materia, text="Professor (nome exato):").grid(
            row=r, column=0, sticky="e", padx=6, pady=8
        )
        ttk.Entry(card_materia, textvariable=self.prof, width=32).grid(
            row=r, column=1, padx=6, pady=8
        )

        r += 1
        ttk.Label(card_materia, text="Matéria:").grid(row=r, column=0, sticky="e", padx=6, pady=8)
        ttk.Entry(card_materia, textvariable=self.materia, width=32).grid(
            row=r, column=1, padx=6, pady=8
        )

        ttk.Button(
            card_materia,
            text="Atribuir",
            style="Accent.TButton",
            command=self.atribuir_materia
        ).grid(row=r+1, column=0, columnspan=2, pady=10)

    def cadastrar_usuario_novo(self):
        nome = self.nome.get().strip()
        tipo = self.tipo.get().strip()
        senha = self.senha.get().strip()

        if not nome or not senha:
            messagebox.showwarning("Campos", "Preencha nome e senha.")
            return

        ok = cadastrar_usuario(nome, tipo, senha)
        if ok:
            messagebox.showinfo("OK", f"Usuário {nome} ({tipo}) cadastrado.")
            self.nome.set("")
            self.senha.set("")
        else:
            messagebox.showerror("Erro", "Não foi possível cadastrar (usuário já existe?).")

    def atribuir_materia(self):
        professor = self.prof.get().strip()
        materia = self.materia.get().strip()

        if not professor or not materia:
            messagebox.showwarning("Campos", "Preencha professor e matéria.")
            return

        ok = atribuir_materia_professor(professor, materia)
        if ok:
            messagebox.showinfo("OK", f"Matéria '{materia}' atribuída ao professor '{professor}'.")
            self.materia.set("")
        else:
            messagebox.showerror("Erro", "Professor não encontrado ou não é 'professor'.")

#TelaProfessor
class ProfessorScreen:
    def __init__(self, app: App, professor_nome: str):
        self.app = app
        self.professor = professor_nome
        self.materia = obter_materia_professor(professor_nome) or ""

        page = criar_pagina(app.container)

        _, right = header_bar(
            page,
            f"Professor: {professor_nome}",
            f"Matéria: {self.materia or '— sem atribuição —'}",
            icon="🧑‍🏫"
        )
        ttk.Button(
            right,
            text="Logout",
            style="Secondary.TButton",
            command=self.app.mostrar_login
        ).pack()

        main = ttk.Frame(page)
        main.pack(pady=6)
        main.columnconfigure(1, weight=1)

        left = card(main)
        left.grid(row=0, column=0, padx=(0, 8), sticky="n")

        ttk.Label(left, text="Alunos").grid(row=0, column=0, sticky="w", padx=2, pady=(0, 4))

        self.filtro = tk.StringVar()
        ttk.Entry(left, textvariable=self.filtro, width=28).grid(row=1, column=0, padx=2, pady=(0, 6))

        self.lista_alunos = tk.Listbox(left, height=16, width=28, exportselection=False)
        self.lista_alunos.grid(row=2, column=0, padx=2, pady=(0, 6))

        ttk.Button(
            left,
            text="Atualizar lista",
            style="Secondary.TButton",
            command=self.carregar_lista
        ).grid(row=3, column=0, sticky="e")

        right = card(main)
        right.grid(row=0, column=1, padx=(8, 0), sticky="n")
        right.columnconfigure(1, weight=1)

        self.aluno_sel = tk.StringVar(value="(nenhum)")
        self.p1 = tk.StringVar()
        self.p2 = tk.StringVar()
        self.trabalho = tk.StringVar()

        r = 0
        ttk.Label(right, text="Aluno selecionado:").grid(row=r, column=0, sticky="e", padx=6, pady=8)
        ttk.Label(
            right,
            textvariable=self.aluno_sel,
            font=("Segoe UI Semibold", 11)
        ).grid(row=r, column=1, sticky="w")

        vcmd = (app.root.register(self.validar_nota), "%P")

        r += 1
        ttk.Label(right, text="Prova 1:").grid(row=r, column=0, sticky="e", padx=6, pady=6)
        ttk.Entry(
            right,
            textvariable=self.p1,
            width=12,
            validate="key",
            validatecommand=vcmd
        ).grid(row=r, column=1, sticky="w")

        r += 1
        ttk.Label(right, text="Prova 2:").grid(row=r, column=0, sticky="e", padx=6, pady=6)
        ttk.Entry(
            right,
            textvariable=self.p2,
            width=12,
            validate="key",
            validatecommand=vcmd
        ).grid(row=r, column=1, sticky="w")

        r += 1
        ttk.Label(right, text="Trabalho:").grid(row=r, column=0, sticky="e", padx=6, pady=6)
        ttk.Entry(
            right,
            textvariable=self.trabalho,
            width=12,
            validate="key",
            validatecommand=vcmd
        ).grid(row=r, column=1, sticky="w")

        r += 1
        botoes = ttk.Frame(right, style="Card.TFrame")
        botoes.grid(row=r, column=0, columnspan=2, pady=10, sticky="e")

        ttk.Button(
            botoes,
            text="Salvar Notas",
            style="Accent.TButton",
            command=self.salvar_notas
        ).pack(side="left", padx=6)

        ttk.Button(
            botoes,
            text="Registrar Falta (hoje)",
            style="Secondary.TButton",
            command=self.registrar_falta_hoje
        ).pack(side="left", padx=6)

        self.lista_alunos.bind("<<ListboxSelect>>", self.quando_selecionar)
        self.filtro.trace_add("write", lambda *_: self.carregar_lista())

        self.carregar_lista()

    def validar_nota(self, texto):
        if texto.strip() == "":
            return True
        try:
            valor = float(texto.replace(",", "."))
            return 0 <= valor <= 10
        except Exception:
            return False

    def converter_nota(self, s):
        try:
            valor = float(s.replace(",", "."))
            if 0 <= valor <= 10:
                return valor
        except Exception:
            return None

    def carregar_lista(self):
        alunos = listar_alunos()
        termo = self.filtro.get().strip().lower()
        self.lista_alunos.delete(0, "end")
        for a in alunos:
            if not termo or termo in a.lower():
                self.lista_alunos.insert("end", a)

    def aluno_selecionado(self):
        sel = self.lista_alunos.curselection()
        return self.lista_alunos.get(sel[0]) if sel else ""

    def quando_selecionar(self, _evt=None):
        aluno = self.aluno_selecionado()
        self.aluno_sel.set(aluno if aluno else "(nenhum)")

    def salvar_notas(self):
        aluno = self.aluno_selecionado()
        if not aluno:
            messagebox.showwarning("Seleção", "Selecione um aluno.")
            return

        if not self.materia:
            messagebox.showwarning("Matéria", "Professor sem matéria atribuída.")
            return

        v1 = self.converter_nota(self.p1.get())
        v2 = self.converter_nota(self.p2.get())
        vtr = self.converter_nota(self.trabalho.get())

        if None in (v1, v2, vtr):
            messagebox.showwarning("Notas", "Digite notas entre 0 e 10.")
            return

        ok = salvar_notas3(aluno, self.materia, v1, v2, vtr)
        messagebox.showinfo("Notas", "Notas registradas!" if ok else "Falhou.")

        if ok:
            self.p1.set("")
            self.p2.set("")
            self.trabalho.set("")

    def registrar_falta_hoje(self):
        aluno = self.aluno_selecionado()
        if not aluno:
            messagebox.showwarning("Seleção", "Selecione um aluno.")
            return

        if not self.materia:
            messagebox.showwarning("Matéria", "Professor sem matéria atribuída.")
            return

        data_hoje = date.today().strftime("%Y%m%d")
        ok = registrar_falta(aluno, self.materia, data_hoje)
        messagebox.showinfo("Falta", "Falta registrada!" if ok else "Falhou.")

#TelaAluno
class AlunoScreen:
    def __init__(self, app: App, aluno_nome: str):
        self.app = app
        self.aluno = aluno_nome

        page = criar_pagina(app.container)

        _, right = header_bar(page, f"Olá, {aluno_nome}", "Suas notas e faltas", icon="🎒")
        ttk.Button(
            right,
            text="Logout",
            style="Secondary.TButton",
            command=self.app.mostrar_login
        ).pack()

        frm = card(page)
        frm.pack(pady=6, fill="both", expand=True)

        colunas = ("Matéria", "P1", "P2", "Trab", "Média", "Situação")

        self.tree = ttk.Treeview(frm, columns=colunas, show="headings", height=12)

        for c in colunas:
            self.tree.heading(c, text=c)
            anchor = "w" if c == "Matéria" else "center"
            if c == "Matéria":
                width = 240
            elif c in ("P1", "P2", "Trab", "Média"):
                width = 80
            else:
                width = 140
            self.tree.column(c, width=width, anchor=anchor)

        self.tree.grid(row=0, column=0, columnspan=3, padx=4, pady=4, sticky="nsew")
        style_tree_status(self.tree)

        frm.rowconfigure(0, weight=1)
        frm.columnconfigure(0, weight=1)

        self.faltas_var = tk.StringVar(value="Faltas: 0")
        ttk.Label(frm, textvariable=self.faltas_var).grid(
            row=1, column=0, sticky="w", padx=4, pady=(6, 4)
        )

        ttk.Button(
            frm,
            text="Atualizar",
            style="Secondary.TButton",
            command=self.atualizar
        ).grid(row=1, column=2, sticky="e", padx=6)

        ttk.Button(
            frm,
            text="Ajuda / Chat",
            style="Accent.TButton",
            command=lambda: abrir_chat(app.root, aluno_nome)
        ).grid(row=1, column=1, sticky="e", padx=6)

        self.atualizar()

    def atualizar(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for mat, p1, p2, tr, md, st in obter_notas3(self.aluno):
            tag = "ok" if st.lower().startswith("apro") else "bad"
            self.tree.insert("", "end", values=(mat, p1, p2, tr, md, st), tags=(tag,))

        faltas = contar_faltas(self.aluno)
        self.faltas_var.set(f"Faltas: {faltas}")


if __name__ == "__main__":
    App().run()
