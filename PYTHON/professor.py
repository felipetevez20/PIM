import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date

from escola_wrapper import listar_alunos, salvar_notas3, registrar_falta, obter_materia_professor
from chatbot import abrir_chat
from estilo import apply_theme, header_bar, card


def abrir_painel_prof(pai, nome_prof):
    tela = tk.Toplevel(pai)
    tela.title("Professor")
    tela.geometry("820x460")
    apply_theme(tela)

    materia = obter_materia_professor(nome_prof) or ""

    header_bar(tela, f"Professor: {nome_prof}", f"Matéria: {materia if materia else '(nenhuma)'}", icon="📚")

    conteudo = ttk.Frame(tela)
    conteudo.pack(fill="both", expand=True, padx=10, pady=10)
    conteudo.columnconfigure(1, weight=1)

    bloco_lista = card(conteudo)
    bloco_lista.grid(row=0, column=0, sticky="nsew", padx=6)
    ttk.Label(bloco_lista, text="Alunos").pack(anchor="w", pady=4)

    filtro = tk.StringVar()
    ttk.Entry(bloco_lista, textvariable=filtro, width=28).pack(fill="x", padx=2)
    lista = tk.Listbox(bloco_lista, height=18, exportselection=False)
    lista.pack(fill="both", expand=True, padx=2, pady=6)

    def carregar_lista():
        nomes = listar_alunos()
        termo = filtro.get().strip().lower()
        lista.delete(0, "end")
        for n in nomes:
            if not termo or termo in n.lower():
                lista.insert("end", n)

    ttk.Button(bloco_lista, text="Recarregar", command=carregar_lista).pack(anchor="e", pady=4)

    bloco_registro = card(conteudo)
    bloco_registro.grid(row=0, column=1, sticky="nsew", padx=6)
    bloco_registro.columnconfigure(1, weight=1)

    aluno_atual = tk.StringVar(value="(nenhum)")
    prova1 = tk.StringVar()
    prova2 = tk.StringVar()
    trabalho = tk.StringVar()

    ttk.Label(bloco_registro, text="Aluno escolhido:").grid(row=0, column=0, sticky="e", padx=4, pady=4)
    ttk.Label(bloco_registro, textvariable=aluno_atual).grid(row=0, column=1, sticky="w", pady=4)

    ttk.Label(bloco_registro, text="Prova 1:").grid(row=1, column=0, sticky="e", padx=4, pady=3)
    ttk.Entry(bloco_registro, textvariable=prova1, width=8).grid(row=1, column=1, sticky="w", pady=3)

    ttk.Label(bloco_registro, text="Prova 2:").grid(row=2, column=0, sticky="e", padx=4, pady=3)
    ttk.Entry(bloco_registro, textvariable=prova2, width=8).grid(row=2, column=1, sticky="w", pady=3)

    ttk.Label(bloco_registro, text="Trabalho:").grid(row=3, column=0, sticky="e", padx=4, pady=3)
    ttk.Entry(bloco_registro, textvariable=trabalho, width=8).grid(row=3, column=1, sticky="w", pady=3)

    def pegar_nome():
        s = lista.curselection()
        return lista.get(s[0]) if s else ""

    def checar_nota(txt):
        try:
            v = float(txt.replace(",", "."))
            return v if 0 <= v <= 10 else None
        except:
            return None

    def salvar_notas():
        aluno = pegar_nome()
        if not aluno:
            messagebox.showwarning("Atenção", "Selecione um aluno da lista.")
            return
        if not materia:
            messagebox.showwarning("Atenção", "Esse professor não tem matéria definida ainda.")
            return

        n1 = checar_nota(prova1.get())
        n2 = checar_nota(prova2.get())
        nt = checar_nota(trabalho.get())
        if None in (n1, n2, nt):
            messagebox.showwarning("Atenção", "Coloca notas de 0 a 10.")
            return

        ok = salvar_notas3(aluno, materia, n1, n2, nt)
        messagebox.showinfo("Notas", "Salvou!" if ok else "Deu ruim ao salvar.")

        if ok:
            prova1.set("")
            prova2.set("")
            trabalho.set("")

    def salvar_falta():
        aluno = pegar_nome()
        if not aluno:
            messagebox.showwarning("Atenção", "Selecione um aluno.")
            return
        if not materia:
            messagebox.showwarning("Atenção", "Sem matéria atribuída a esse professor.")
            return

        hoje = date.today().strftime("%Y%m%d")
        ok = registrar_falta(aluno, materia, hoje)
        messagebox.showinfo("Faltas", "Falta salva!" if ok else "Falhou ao salvar a falta.")

    def quando_clicar(_evt=None):
        nome = pegar_nome()
        aluno_atual.set(nome if nome else "(nenhum)")

    lista.bind("<<ListboxSelect>>", quando_clicar)
    filtro.trace_add("write", lambda *_: carregar_lista())

    linha_btns = ttk.Frame(bloco_registro)
    linha_btns.grid(row=4, column=0, columnspan=2, sticky="e", pady=8)

    ttk.Button(linha_btns, text="Salvar notas", command=salvar_notas).pack(side="left", padx=4)
    ttk.Button(linha_btns, text="Registrar falta", command=salvar_falta).pack(side="left", padx=4)
    ttk.Button(bloco_registro, text="Chat ajuda", command=lambda: abrir_chat(tela, nome_prof)).grid(row=5, column=1, sticky="e", pady=6)

    carregar_lista()
