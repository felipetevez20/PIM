import tkinter as tk
from tkinter import ttk

#CoresPrincipais
COL_BG      = "#0f172a"  
COL_SURFACE = "#111827"  
COL_ACCENT  = "#0ea5e9"
COL_ACCENT2 = "#14b8a6"  
COL_TXT     = "#e5e7eb"  
COL_TXT_MUT = "#94a3b8"  
COL_OK      = "#10b981"  
COL_BAD     = "#ef4444" 
COL_LINE    = "#1f2937" 

DEFAULT_FONT = ("Segoe UI", 10)
DEFAULT_FONT_BOLD = ("Segoe UI Semibold", 10)


def apply_theme(root: tk.Tk | tk.Toplevel):
    """Aplica um tema escuro simples na janela."""
    root.configure(bg=COL_BG)
    style = ttk.Style(root)

    try:
        style.theme_use("clam")
    except:
        pass

    #Fonte
    root.option_add("*Font", DEFAULT_FONT)

    style.configure("TFrame", background=COL_BG)
    style.configure("Card.TFrame", background=COL_SURFACE)
    style.configure("TLabel", background=COL_BG, foreground=COL_TXT)
    style.configure("Subtle.TLabel", background=COL_BG, foreground=COL_TXT_MUT)
    style.configure("Card.TLabel", background=COL_SURFACE, foreground=COL_TXT)

    #Botões1
    style.configure(
        "Accent.TButton",
        background=COL_ACCENT,
        foreground="white",
        bordercolor=COL_ACCENT,
        relief="flat"
    )
    style.map("Accent.TButton", background=[("active", "#0284c7")])

    #Botóes2
    style.configure(
        "Secondary.TButton",
        background=COL_SURFACE,
        foreground=COL_TXT,
        bordercolor=COL_LINE,
        relief="flat"
    )
    style.map("Secondary.TButton", background=[("active", "#1f2937")])

    #Emtradas
    style.configure(
        "TEntry",
        fieldbackground=COL_SURFACE,
        foreground=COL_TXT,
        insertcolor=COL_TXT,
        bordercolor=COL_LINE,
        relief="flat"
    )

    style.configure(
        "TCombobox",
        fieldbackground=COL_SURFACE,
        foreground=COL_TXT,
        arrowcolor=COL_TXT,
        bordercolor=COL_LINE
    )

    #Abas
    style.configure("TNotebook", background=COL_BG, borderwidth=0)
    style.configure("TNotebook.Tab", background=COL_SURFACE, foreground=COL_TXT)
    style.map(
        "TNotebook.Tab",
        background=[("selected", COL_ACCENT2)],
        foreground=[("selected", COL_BG)]
    )

    #Tabelas
    style.configure(
        "Treeview",
        background=COL_SURFACE,
        fieldbackground=COL_SURFACE,
        foreground=COL_TXT,
        rowheight=24,
        bordercolor=COL_LINE,
        borderwidth=0
    )
    style.configure(
        "Treeview.Heading",
        background="#0b1220",
        foreground=COL_TXT,
        bordercolor=COL_LINE,
        relief="flat"
    )


def header_bar(parent, title: str, subtitle: str | None = None, icon: str = "🎓"):
   
    wrap = ttk.Frame(parent, style="TFrame")
    wrap.pack(fill="x", padx=12, pady=(12, 8))

    left = ttk.Frame(wrap, style="TFrame")
    left.pack(side="left")

    icon_lbl = ttk.Label(left, text=icon, font=("Segoe UI Emoji", 18))
    icon_lbl.grid(row=0, column=0, rowspan=2, sticky="w", padx=(0, 8))

    ttl = ttk.Label(left, text=title, font=DEFAULT_FONT_BOLD)
    ttl.grid(row=0, column=1, sticky="w")

    if subtitle:
        sub = ttk.Label(left, text=subtitle, style="Subtle.TLabel")
        sub.grid(row=1, column=1, sticky="w")

    right = ttk.Frame(wrap, style="TFrame")
    right.pack(side="right")

    return wrap, right


def card(parent):
    
    frm = ttk.Frame(parent, style="Card.TFrame")
    frm.configure(padding=12)
    return frm


def style_tree_status(tree: ttk.Treeview):
    
    tree.tag_configure("ok", foreground=COL_OK)
    tree.tag_configure("bad", foreground=COL_BAD)
