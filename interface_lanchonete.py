import tkinter as tk
from tkinter import messagebox
import json

# =========================
# DADOS
# =========================
produtos = {}
vendas = []

def salvar_produtos():
    with open('produtos.json', 'w') as arquivo:
        json.dump(produtos, arquivo, indent=4)

def carregar_produtos():
    global produtos
    try:
        with open('produtos.json', 'r') as arquivo:
            produtos = json.load(arquivo)
    except FileNotFoundError:
        produtos = {}

def salvar_vendas():
    with open('vendas.json', 'w') as arquivo:
        json.dump(vendas, arquivo, indent=4)

def carregar_vendas():
    global vendas
    try:
        with open('vendas.json', 'r') as arquivo:
            vendas = json.load(arquivo)
    except FileNotFoundError:
        vendas = []

# =========================
# FUNÇÕES GRÁFICAS
# =========================

def cadastrar_produto():
    def salvar():
        nome = entry_nome.get()
        preco = float(entry_preco.get())
        custo = float(entry_custo.get())
        quantidade = int(entry_quantidade.get())
        produtos[nome] = {'preco': preco, 'custo': custo, 'quantidade': quantidade}
        salvar_produtos()
        messagebox.showinfo("Sucesso", f"Produto '{nome}' cadastrado!")
        janela.destroy()

    janela = tk.Toplevel()
    janela.title("Cadastrar Produto")

    tk.Label(janela, text="Nome:").grid(row=0, column=0)
    tk.Label(janela, text="Preço:").grid(row=1, column=0)
    tk.Label(janela, text="Custo:").grid(row=2, column=0)
    tk.Label(janela, text="Quantidade:").grid(row=3, column=0)

    entry_nome = tk.Entry(janela)
    entry_preco = tk.Entry(janela)
    entry_custo = tk.Entry(janela)
    entry_quantidade = tk.Entry(janela)

    entry_nome.grid(row=0, column=1)
    entry_preco.grid(row=1, column=1)
    entry_custo.grid(row=2, column=1)
    entry_quantidade.grid(row=3, column=1)

    tk.Button(janela, text="Salvar", command=salvar).grid(row=4, columnspan=2)

def vender_produto():
    def registrar_venda():
        nome = entry_nome.get()
        if nome in produtos:
            quantidade = int(entry_quantidade.get())
            if produtos[nome]['quantidade'] >= quantidade:
                produtos[nome]['quantidade'] -= quantidade
                total = produtos[nome]['preco'] * quantidade
                lucro = (produtos[nome]['preco'] - produtos[nome]['custo']) * quantidade
                vendas.append({'produto': nome, 'quantidade': quantidade, 'total': total, 'lucro': lucro})
                salvar_produtos()
                salvar_vendas()
                messagebox.showinfo("Venda registrada", f"Total: R$ {total:.2f}\nLucro: R$ {lucro:.2f}")
                janela.destroy()
            else:
                messagebox.showwarning("Erro", "Estoque insuficiente!")
        else:
            messagebox.showerror("Erro", "Produto não encontrado!")

    janela = tk.Toplevel()
    janela.title("Vender Produto")

    tk.Label(janela, text="Nome do produto:").grid(row=0, column=0)
    tk.Label(janela, text="Quantidade:").grid(row=1, column=0)

    entry_nome = tk.Entry(janela)
    entry_quantidade = tk.Entry(janela)

    entry_nome.grid(row=0, column=1)
    entry_quantidade.grid(row=1, column=1)

    tk.Button(janela, text="Confirmar Venda", command=registrar_venda).grid(row=2, columnspan=2)

def ver_estoque():
    janela = tk.Toplevel()
    janela.title("Estoque de Produtos")

    if not produtos:
        tk.Label(janela, text="Nenhum produto cadastrado.").pack(pady=10)
        return

    for nome, info in produtos.items():
        texto = f"{nome} | Preço: R$ {info['preco']:.2f} | Custo: R$ {info['custo']:.2f} | Quantidade: {info['quantidade']}"
        tk.Label(janela, text=texto, anchor="w", justify="left").pack(anchor="w", padx=10, pady=2)

def ver_vendas():
    janela = tk.Toplevel()
    janela.title("Vendas Realizadas")

    if not vendas:
        tk.Label(janela, text="Nenhuma venda registrada.").pack(pady=10)
        return

    total_vendas = 0
    total_lucro = 0

    for venda in vendas:
        texto = (f"Produto: {venda['produto']} | "
                 f"Quantidade: {venda['quantidade']} | "
                 f"Total: R$ {venda['total']:.2f} | "
                 f"Lucro: R$ {venda['lucro']:.2f}")
        tk.Label(janela, text=texto, anchor="w", justify="left").pack(anchor="w", padx=10, pady=2)
        total_vendas += venda['total']
        total_lucro += venda['lucro']

    tk.Label(janela, text=f"\nTotal de Vendas: R$ {total_vendas:.2f}", font=("Arial", 12, "bold")).pack(pady=10)
    tk.Label(janela, text=f"Lucro Total: R$ {total_lucro:.2f}", font=("Arial", 12, "bold")).pack(pady=5)

def ver_custos_produtos():
    janela = tk.Toplevel()
    janela.title("Custos dos Produtos em Estoque")

    if not produtos:
        tk.Label(janela, text="Nenhum produto cadastrado.").pack(pady=10)
        return

    custo_total_estoque = 0

    for nome, info in produtos.items():
        custo_total = info['custo'] * info['quantidade']
        custo_total_estoque += custo_total
        texto = f"{nome} | Custo Unitário: R$ {info['custo']:.2f} | Quantidade: {info['quantidade']} | Custo Total: R$ {custo_total:.2f}"
        tk.Label(janela, text=texto, anchor="w", justify="left").pack(anchor="w", padx=10, pady=2)

    tk.Label(janela, text=f"\nCusto Total do Estoque: R$ {custo_total_estoque:.2f}", font=("Arial", 12, "bold")).pack(pady=10)

def tela_principal():
    root = tk.Tk()
    root.title("Sistema de Lanchonete")

    tk.Label(root, text="Menu Principal", font=("Arial", 16)).pack(pady=10)

    tk.Button(root, text="Cadastrar Produto", width=30, command=cadastrar_produto).pack(pady=5)
    tk.Button(root, text="Vender Produto", width=30, command=vender_produto).pack(pady=5)
    tk.Button(root, text="Ver Estoque", width=30, command=ver_estoque).pack(pady=5)
    tk.Button(root, text="Ver Vendas", width=30, command=ver_vendas).pack(pady=5)
    tk.Button(root, text="Ver Custos de Produtos", width=30, command=ver_custos_produtos).pack(pady=5)
    tk.Button(root, text="Sair", width=30, command=root.destroy).pack(pady=20)

    root.mainloop()

# =========================
# INICIAR
# =========================

carregar_produtos()
carregar_vendas()
tela_principal()
