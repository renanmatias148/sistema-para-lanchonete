import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os
import matplotlib.pyplot as plt

# Funções de manipulação de arquivos
def carregar_dados(arquivo):
    if os.path.exists(arquivo):
        with open(arquivo, 'r') as f:
            return json.load(f)
    return []

def salvar_dados(arquivo, dados):
    with open(arquivo, 'w') as f:
        json.dump(dados, f, indent=4)

# Dados principais
ingredientes = carregar_dados("ingredientes.json")
produtos = carregar_dados("produtos.json")
vendas = carregar_dados("vendas.json")
funcionarios = carregar_dados("funcionarios.json")

# Interface
janela = tk.Tk()
janela.title("Sistema de Lanchonete")
janela.geometry("400x400")

# Funções principais
def cadastrar_ingrediente():
    nome = simpledialog.askstring("Ingrediente", "Nome do ingrediente:")
    if nome:
        try:
            custo = float(simpledialog.askstring("Ingrediente", f"Custo por unidade de {nome}:").replace(",", "."))
            ingredientes.append({"nome": nome, "custo": custo})
            salvar_dados("ingredientes.json", ingredientes)
            messagebox.showinfo("Sucesso", "Ingrediente cadastrado!")
        except:
            messagebox.showerror("Erro", "Custo inválido")

def cadastrar_produto():
    nome = simpledialog.askstring("Produto", "Nome do produto:")
    preco = float(simpledialog.askstring("Produto", "Preço de venda:").replace(",", "."))
    quantidade = int(simpledialog.askstring("Produto", "Quantidade inicial em estoque:"))
    ingrs = []
    while True:
        ing_nome = simpledialog.askstring("Ingrediente", "Nome do ingrediente (deixe vazio para parar):")
        if not ing_nome:
            break
        qtd = float(simpledialog.askstring("Quantidade", f"Quantidade de {ing_nome} usada:").replace(",", "."))
        ingrs.append({"nome": ing_nome, "quantidade": qtd})
    produtos.append({"nome": nome, "preco": preco, "ingredientes": ingrs, "quantidade": quantidade})
    salvar_dados("produtos.json", produtos)
    messagebox.showinfo("Sucesso", "Produto cadastrado!")

def vender():
    nome = simpledialog.askstring("Venda", "Nome do produto vendido:")
    produto = next((p for p in produtos if p["nome"] == nome), None)
    if not produto:
        messagebox.showerror("Erro", "Produto não encontrado")
        return

    if produto["quantidade"] <= 0:
        messagebox.showerror("Estoque", f"O produto '{produto['nome']}' está sem estoque!")
        return

    adicionais = []
    while True:
        add = simpledialog.askstring("Adicional", "Adicional (Enter para parar):")
        if not add:
            break
        adicionais.append(add)

    total = produto["preco"]

    # Calcular custo dos ingredientes usados
    custo_total = 0
    for usado in produto["ingredientes"]:
        ing = next((i for i in ingredientes if i["nome"] == usado["nome"]), None)
        if ing:
            custo_total += usado["quantidade"] * ing["custo"]

    lucro = total - custo_total

    produto["quantidade"] -= 1
    salvar_dados("produtos.json", produtos)

    vendas.append({
        "produto": produto["nome"],
        "adicionais": adicionais,
        "total": total,
        "custo": custo_total,
        "lucro": lucro
    })
    salvar_dados("vendas.json", vendas)
    messagebox.showinfo("Venda", f"Venda registrada. Total: R$ {total:.2f}\nLucro: R$ {lucro:.2f}")

def ver_estoque():
    estoque = "\n".join([f"{i['nome']} - R$ {i['custo']:.2f}" for i in ingredientes])
    messagebox.showinfo("Estoque de Ingredientes", estoque)

def ver_estoque_produtos():
    texto = "\n".join([f"{p['nome']}: {p['quantidade']} unidades" for p in produtos])
    messagebox.showinfo("Estoque de Produtos", texto)

def ver_vendas():
    texto = "\n".join([f"{v['produto']} - R$ {v['total']:.2f}" for v in vendas])
    messagebox.showinfo("Vendas Realizadas", texto)

def ver_grafico_vendas():
    nomes = [v["produto"] for v in vendas]
    contagem = {}
    for nome in nomes:
        contagem[nome] = contagem.get(nome, 0) + 1

    if not contagem:
        messagebox.showinfo("Gráfico", "Nenhuma venda registrada")
        return

    plt.bar(contagem.keys(), contagem.values())
    plt.title("Produtos Mais Vendidos")
    plt.xlabel("Produto")
    plt.ylabel("Quantidade Vendida")
    plt.tight_layout()
    plt.show()

def ver_relatorios_detalhados():
    total_vendas = len(vendas)
    faturamento_total = sum(venda["total"] for venda in vendas)
    lucro_total = sum(venda.get("lucro", 0.0) for venda in vendas)

    mais_vendido = ""
    qtd_mais_vendido = 0
    contagem = {}
    for venda in vendas:
        nome = venda["produto"]
        contagem[nome] = contagem.get(nome, 0) + 1
        if contagem[nome] > qtd_mais_vendido:
            mais_vendido = nome
            qtd_mais_vendido = contagem[nome]

    relatorio = (
        f"📋 RELATÓRIO DETALHADO\n\n"
        f"Total de Vendas: {total_vendas}\n"
        f"Faturamento Total: R$ {faturamento_total:.2f}\n"
        f"Lucro Total: R$ {lucro_total:.2f}\n\n"
        f"Produto Mais Vendido: {mais_vendido} ({qtd_mais_vendido} vendas)"
    )
    messagebox.showinfo("Relatório", relatorio)

# Funções de login
def cadastrar_funcionario():
    nome = simpledialog.askstring("Funcionário", "Nome do funcionário:")
    senha = simpledialog.askstring("Funcionário", "Senha do funcionário:", show="*")
    
    if nome and senha:
        funcionarios.append({"nome": nome, "senha": senha})
        salvar_dados("funcionarios.json", funcionarios)
        messagebox.showinfo("Sucesso", "Funcionário cadastrado com sucesso!")
    else:
        messagebox.showerror("Erro", "Por favor, preencha todos os campos.")

def login_funcionario():
    nome = simpledialog.askstring("Login", "Nome do funcionário:")
    senha = simpledialog.askstring("Login", "Senha do funcionário:", show="*")

    funcionario = next((f for f in funcionarios if f["nome"] == nome and f["senha"] == senha), None)
    
    if funcionario:
        messagebox.showinfo("Login", "Login realizado com sucesso!")
        return True  # Login bem-sucedido
    else:
        messagebox.showerror("Erro", "Nome ou senha incorretos!")
        return False  # Login falhou

def verificar_login(func):
    def wrapper(*args, **kwargs):
        if login_funcionario():  # Solicita login antes de executar a função
            return func(*args, **kwargs)
        else:
            return None
    return wrapper

# Menu
menu = tk.Menu(janela)
janela.config(menu=menu)

menu_estoque = tk.Menu(menu, tearoff=0)
menu_estoque.add_command(label="Cadastrar Ingrediente", command=cadastrar_ingrediente)
menu_estoque.add_command(label="Ver Estoque", command=ver_estoque)
menu.add_cascade(label="Ingredientes", menu=menu_estoque)

menu_produto = tk.Menu(menu, tearoff=0)
menu_produto.add_command(label="Cadastrar Produto", command=cadastrar_produto)
menu_produto.add_command(label="Ver Estoque de Produtos", command=ver_estoque_produtos)
menu.add_cascade(label="Produtos", menu=menu_produto)

menu_venda = tk.Menu(menu, tearoff=0)
menu_venda.add_command(label="Registrar Venda", command=vender)
menu_venda.add_command(label="Ver Vendas", command=ver_vendas)
menu_venda.add_command(label="Gráfico de Vendas", command=ver_grafico_vendas)
menu_venda.add_command(label="Relatório Detalhado", command=ver_relatorios_detalhados)
menu.add_cascade(label="Vendas", menu=menu_venda)

menu_funcionario = tk.Menu(menu, tearoff=0)
menu_funcionario.add_command(label="Cadastrar Funcionário", command=cadastrar_funcionario)
menu.add_cascade(label="Funcionários", menu=menu_funcionario)

janela.mainloop()
