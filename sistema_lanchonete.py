import os
import json

# ========================
# VARIÁVEIS GLOBAIS
# ========================
produtos = {}
vendas = []

# ========================
# FUNÇÕES DE ARQUIVO
# ========================
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

# ========================
# OUTRAS FUNÇÕES
# ========================
def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def cadastrar_produto():
    nome = input("Nome do produto: ")
    preco = float(input("Preço de venda: R$ "))
    custo = float(input("Custo do produto: R$ "))
    quantidade = int(input("Quantidade em estoque: "))
    produtos[nome] = {'preco': preco, 'custo': custo, 'quantidade': quantidade}
    salvar_produtos()
    print(f"Produto '{nome}' cadastrado com sucesso!")

def vender_produto():
    nome = input("Nome do produto vendido: ")
    if nome in produtos:
        quantidade = int(input("Quantidade vendida: "))
        if produtos[nome]['quantidade'] >= quantidade:
            produtos[nome]['quantidade'] -= quantidade
            total_venda = produtos[nome]['preco'] * quantidade
            lucro = (produtos[nome]['preco'] - produtos[nome]['custo']) * quantidade
            vendas.append({'produto': nome, 'quantidade': quantidade, 'total': total_venda, 'lucro': lucro})
            salvar_produtos()
            salvar_vendas()
            print(f"Venda de {quantidade}x '{nome}' registrada com sucesso! Total: R$ {total_venda:.2f}")
        else:
            print("Estoque insuficiente!")
    else:
        print("Produto não encontrado!")

def ver_estoque():
    print("\n=== ESTOQUE ATUAL ===")
    if not produtos:
        print("Nenhum produto cadastrado.")
    for nome, dados in produtos.items():
        print(f"{nome}: {dados['quantidade']} unidades | Preço: R$ {dados['preco']:.2f}")

def ver_vendas():
    total_vendido = sum(v['total'] for v in vendas)
    total_lucro = sum(v['lucro'] for v in vendas)
    print("\n=== RELATÓRIO DE VENDAS ===")
    for v in vendas:
        print(f"{v['quantidade']}x {v['produto']} - Total: R$ {v['total']:.2f} | Lucro: R$ {v['lucro']:.2f}")
    print(f"\nTOTAL VENDIDO: R$ {total_vendido:.2f}")
    print(f"LUCRO TOTAL: R$ {total_lucro:.2f}")

# ========================
# MENU PRINCIPAL
# ========================
def menu():
    while True:
        print("\n=== SISTEMA DE LANCHONETE ===")
        print("1 - Cadastrar Produto")
        print("2 - Vender Produto")
        print("3 - Ver Estoque")
        print("4 - Ver Vendas e Lucros")
        print("5 - Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            cadastrar_produto()
        elif opcao == '2':
            vender_produto()
        elif opcao == '3':
            ver_estoque()
        elif opcao == '4':
            ver_vendas()
        elif opcao == '5':
            print("Saindo...")
            break
        else:
            print("Opção inválida!")

# ========================
# INÍCIO DO PROGRAMA
# ========================
carregar_produtos()
carregar_vendas()
menu()

