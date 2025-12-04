import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from escola_wrapper import cadastrar_usuario, atribuir_materia_professor
from estilo import apply_theme, header_bar, card

def abrir_painel_diretor(pai):
    tela = tk.Toplevel(pai)
    tela.title("Painel do Diretor")
    tela.geometry("640x420")
    apply_theme(tela)

    header_bar(tela, "Diretor", "Gerenciar usuários e matérias", icon="⚙️")

    painel_abas = ttk.Notebook(tela)
    painel_abas.pack(fill="both", expand=True, padx=10, pady=10)

    aba_users = ttk.Frame(painel_abas)
    painel_abas.add(aba_users, text="Novo usuário")

    bloco_users = card(aba_users)
    bloco_users.pack(fill="x", padx=6, pady=12)

    nome_novo = tk.StringVar()
    cargo_novo = tk.StringVar(value="aluno")
    senha_novo = tk.StringVar()

    ttk.Label(bloco_users, text="Nome:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
    ttk.Entry(bloco_users, textvariable=nome_novo, width=26).grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(bloco_users, text="Cargo:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
    ttk.Combobox(bloco_users, textvariable=cargo_novo, values=["aluno", "professor", "diretor"],
                 state="readonly", width=23).grid(row=1, column=1, padx=5, pady=5)

    ttk.Label(bloco_users, text="Senha:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
    ttk.Entry(bloco_users, textvariable=senha_novo, show="*", width=26).grid(row=2, column=1, padx=5, pady=5)

    def criar_usuario():
        n = nome_novo.get().strip()
        t = cargo_novo.get().strip()
        s = senha_novo.get().strip()

        if not n or not s:
            messagebox.showwarning("Atenção", "Preencha nome e senha")
            return

        if cadastrar_usuario(n, t, s):
            messagebox.showinfo("Sucesso", "Usuário cadastrado!")
            nome_novo.set("")
            senha_novo.set("")
        else:
            messagebox.showerror("Erro", "Não foi possível cadastrar")

    ttk.Button(bloco_users, text="Cadastrar", command=criar_usuario).grid(
        row=3, column=0, columnspan=2, sticky="e", pady=7
    )

    aba_mats = ttk.Frame(painel_abas)
    painel_abas.add(aba_mats, text="Matéria do professor")

    bloco_mats = card(aba_mats)
    bloco_mats.pack(fill="x", padx=6, pady=12)

    professor = tk.StringVar()
    materia = tk.StringVar()

    ttk.Label(bloco_mats, text="Professor:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
    ttk.Entry(bloco_mats, textvariable=professor, width=30).grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(bloco_mats, text="Matéria:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
    ttk.Entry(bloco_mats, textvariable=materia, width=30).grid(row=1, column=1, padx=5, pady=5)

    def colocar_materia():
        p = professor.get().strip()
        m = materia.get().strip()

        if not p or not m:
            messagebox.showwarning("Atenção", "Preencha todos os campos")
            return

        if atribuir_materia_professor(p, m):
            messagebox.showinfo("Sucesso", "Matéria salva!")
            materia.set("")
        else:
            messagebox.showerror("Erro", "Professor não encontrado")

    ttk.Button(bloco_mats, text="Salvar", command=colocar_materia).grid(
        row=2, column=0, columnspan=2, sticky="e", pady=7
    )
