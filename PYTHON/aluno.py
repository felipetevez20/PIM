import tkinter as tk
from tkinter import ttk, messagebox
from escola_wrapper import obter_notas3, contar_faltas
from chatbot import abrir_chat
from estilo import apply_theme, header_bar, card

def abrir_tela(parent, nome_aluno):
    tela = tk.Toplevel(parent)
    tela.title(f"Aluno - {nome_aluno}")
    tela.geometry("780x420")
    apply_theme(tela)

    header_bar(tela, f"Oi, {nome_aluno}", "Notas e faltas", icon="🎓")

    painel = card(tela)
    painel.pack(fill="both", expand=True, padx=10, pady=10)

    colunas = ("Matéria", "Prova 1", "Prova 2", "Trabalho", "Média", "Resultado")
    tabela = ttk.Treeview(painel, columns=colunas, show="headings", height=12)

    for col in colunas:
        tabela.heading(col, text=col)
        largura = 200 if col == "Matéria" else 95
        alinhamento = "w" if col == "Matéria" else "center"
        tabela.column(col, width=largura, anchor=alinhamento)

    tabela.pack(fill="both", expand=True)

    faltas_texto = tk.StringVar()
    ttk.Label(painel, textvariable=faltas_texto).pack(anchor="w", pady=5)

    def recarregar_dados():
        tabela.delete(*tabela.get_children())
        try:
            notas = obter_notas3(nome_aluno)
            for mat, n1, n2, trab, media, situacao in notas:
                etiqueta = "ok" if "apro" in situacao.lower() else "ruim"
                tabela.insert("", "end", values=(mat, n1, n2, trab, media, situacao), tags=(etiqueta,))
            total_faltas = contar_faltas(nome_aluno)
            faltas_texto.set(f"Faltas totais: {total_faltas}")
        except:
            messagebox.showerror("Erro", "Não consegui carregar os dados.")

    ttk.Button(painel, text="Recarregar").pack(pady=6)
    tk.Button(painel, text="Chat", command=lambda: abrir_chat(tela, nome_aluno)).pack()

    recarregar_dados()
