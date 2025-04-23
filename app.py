from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'minha_chave_super_secreta'

# Dados simulados (como se fosse um banco de dados simples em memória)
usuarios = [
    {'nome': 'admin', 'senha': '1234', 'nivel': 'admin'},
    {'nome': 'gerente', 'senha': 'senha123', 'nivel': 'gerente'},
    {'nome': 'caixa', 'senha': 'lanchonete2025', 'nivel': 'funcionario'}
]
vendas = []
ingredientes = [
    {'nome': 'Pão', 'quantidade': 100},
    {'nome': 'Queijo', 'quantidade': 50},
    {'nome': 'Hamburguer', 'quantidade': 30},
    {'nome': 'Alface', 'quantidade': 40}
]

produtos = [
    {'nome': 'Hamburguer', 'preco': 15.00, 'custo': 5.00, 'ingredientes': [
        {'nome': 'Pão', 'quantidade': 1},
        {'nome': 'Queijo', 'quantidade': 1},
        {'nome': 'Hamburguer', 'quantidade': 1}
    ]},
    {'nome': 'Cheeseburger', 'preco': 18.00, 'custo': 7.00, 'ingredientes': [
        {'nome': 'Pão', 'quantidade': 1},
        {'nome': 'Queijo', 'quantidade': 2},
        {'nome': 'Hamburguer', 'quantidade': 1}
    ]}
]

# Funções auxiliares
def get_usuario(nome):
    for u in usuarios:
        if u['nome'] == nome:
            return u
    return None

# Rotas
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nome = request.form['usuario']
        senha = request.form['senha']
        usuario = get_usuario(nome)
        if usuario and usuario['senha'] == senha:
            session['usuario'] = usuario['nome']
            session['nivel'] = usuario['nivel']
            return redirect(url_for('menu'))
        else:
            flash("Login inválido")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    session.pop('nivel', None)
    return redirect(url_for('index'))

@app.route('/menu')
def menu():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    return render_template('menu.html', usuario=session['usuario'], nivel=session['nivel'])

@app.route('/cadastrar_usuario', methods=['GET', 'POST'])
def cadastrar_usuario():
    if 'nivel' not in session or session['nivel'] != 'admin':
        return "Acesso negado. Apenas administradores podem cadastrar novos usuários."
    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']
        nivel = request.form['nivel']
        if get_usuario(nome):
            flash("Usuário já existe.")
        else:
            usuarios.append({'nome': nome, 'senha': senha, 'nivel': nivel})
            flash("Usuário cadastrado com sucesso.")
            return redirect(url_for('menu'))
    return render_template('cadastrar_usuario.html')

@app.route('/cadastrar_produto', methods=['GET', 'POST'])
def cadastrar_produto():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        nome = request.form['nome']
        preco = float(request.form['preco'])
        custo = float(request.form['custo'])
        ingredientes_prod = request.form.getlist('ingredientes')
        produtos.append({
            'nome': nome,
            'preco': preco,
            'custo': custo,
            'ingredientes': ingredientes_prod
        })
        flash('Produto cadastrado com sucesso!')
        return redirect(url_for('menu'))
    return render_template('cadastrar_produto.html', ingredientes=ingredientes)

@app.route('/estoque')
def ver_estoque():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    return render_template('estoque.html', ingredientes=ingredientes)

@app.route('/atualizar_estoque/<ingrediente>/<acao>', methods=['GET', 'POST'])
def atualizar_estoque(ingrediente, acao):
    if 'usuario' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        quantidade = int(request.form['quantidade'])

        # Procurar o ingrediente no estoque
        for ing in ingredientes:
            if ing['nome'] == ingrediente:
                if acao == 'adicionar':
                    ing['quantidade'] += quantidade
                elif acao == 'subtrair' and ing['quantidade'] >= quantidade:
                    ing['quantidade'] -= quantidade
                else:
                    flash('Quantidade insuficiente no estoque para subtrair!')
                    return redirect(url_for('ver_estoque'))
                flash(f'{acao.capitalize()} {quantidade} de {ingrediente} no estoque com sucesso!')
                return redirect(url_for('ver_estoque'))

    return render_template('atualizar_estoque.html', ingrediente=ingrediente, acao=acao)

@app.route('/vender', methods=['GET', 'POST'])
def vender():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        produto_nome = request.form['produto']
        quantidade = int(request.form['quantidade'])

        # Buscar o produto no banco de dados (lista de produtos)
        produto = next((p for p in produtos if p['nome'] == produto_nome), None)

        if produto:
            # Calcular o valor total da venda
            total = produto['preco'] * quantidade

            # Verificar se há estoque suficiente de ingredientes
            for ingrediente in produto['ingredientes']:
                ingrediente_nome = ingrediente['nome']
                ingrediente_quantidade = ingrediente['quantidade'] * quantidade
                # Procurar o ingrediente no estoque
                estoque_ingrediente = next((ing for ing in ingredientes if ing['nome'] == ingrediente_nome), None)

                if estoque_ingrediente and estoque_ingrediente['quantidade'] < ingrediente_quantidade:
                    flash(f"Não há estoque suficiente de {ingrediente_nome}!")
                    return redirect(url_for('vender'))

            # Registrar a venda
            vendas.append({
                'produto': produto_nome,
                'quantidade': quantidade,
                'total': total,
                'data': datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
            })

            # Atualizar o estoque de ingredientes
            for ingrediente in produto['ingredientes']:
                ingrediente_nome = ingrediente['nome']
                ingrediente_quantidade = ingrediente['quantidade'] * quantidade
                for ing in ingredientes:
                    if ing['nome'] == ingrediente_nome:
                        ing['quantidade'] -= ingrediente_quantidade

            flash("Venda registrada com sucesso!")
            return redirect(url_for('menu'))
        else:
            flash("Produto não encontrado!")

    return render_template('vender.html', produtos=produtos)

from datetime import datetime

# Exemplo de dados de vendas (isso pode ser extraído de um banco de dados)
vendas = [
    {'data': '2025-04-01', 'produto': 'Hamburguer', 'quantidade': 3, 'valor_total': 30.00},
    {'data': '2025-04-02', 'produto': 'Refrigerante', 'quantidade': 5, 'valor_total': 15.00},
    {'data': '2025-04-03', 'produto': 'Pizza', 'quantidade': 2, 'valor_total': 40.00},
    # Adicione mais vendas conforme necessário
]

@app.route('/vendas', methods=['GET', 'POST'])
def ver_vendas():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    
    # Filtragem por data
    if request.method == 'POST':
        inicio = request.form['inicio']
        fim = request.form['fim']

        # Converter as datas de string para datetime
        if inicio and fim:
            inicio = datetime.strptime(inicio, '%Y-%m-%d')
            fim = datetime.strptime(fim, '%Y-%m-%d')

            # Filtrando as vendas dentro do intervalo
            vendas_filtradas = [
                venda for venda in vendas 
                if inicio <= datetime.strptime(venda['data'], '%Y-%m-%d') <= fim
            ]
        else:
            vendas_filtradas = vendas
    else:
        vendas_filtradas = vendas

    return render_template('vendas.html', vendas=vendas_filtradas)


@app.route('/relatorio')
def relatorio():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    # Calcular o total de vendas
    total_vendas = sum([venda.get('valor_total', 0) for venda in vendas])


    # Calcular o lucro (total de vendas - custo total dos produtos vendidos)
    lucro = sum([
        (produto['preco'] - produto['custo']) * quantidade
        for venda in vendas
        for produto in produtos
        if produto['nome'] == venda['produto']
        for quantidade in [venda['quantidade']]
    ])

    return render_template('relatorio.html', total_vendas=total_vendas, lucro=lucro)

@app.route('/ver_produtos')
def ver_produtos():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    return render_template('ver_produtos.html', produtos=produtos)
@app.route('/cadastrar_ingrediente', methods=['GET', 'POST'])
def cadastrar_ingrediente():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        nome = request.form['nome']
        quantidade = int(request.form['quantidade'])

        # Verifica se o ingrediente já existe
        for ing in ingredientes:
            if ing['nome'].lower() == nome.lower():
                flash('Ingrediente já existe!')
                return redirect(url_for('cadastrar_ingrediente'))

        ingredientes.append({'nome': nome, 'quantidade': quantidade})
        flash('Ingrediente cadastrado com sucesso!')
        return redirect(url_for('menu'))

    return render_template('cadastrar_ingrediente.html')
@app.route('/ingredientes')
def listar_ingredientes():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    return render_template('listar_ingredientes.html', ingredientes=ingredientes)
@app.route('/editar_ingrediente/<nome>', methods=['GET', 'POST'])
def editar_ingrediente(nome):
    if 'usuario' not in session:
        return redirect(url_for('login'))

    ingrediente = next((ing for ing in ingredientes if ing['nome'] == nome), None)

    if not ingrediente:
        flash('Ingrediente não encontrado!')
        return redirect(url_for('listar_ingredientes'))

    if request.method == 'POST':
        ingrediente['nome'] = request.form['nome']
        ingrediente['quantidade'] = int(request.form['quantidade'])
        flash('Ingrediente atualizado com sucesso!')
        return redirect(url_for('listar_ingredientes'))

    return render_template('editar_ingrediente.html', ingrediente=ingrediente)
@app.route('/remover_ingrediente/<nome>')
def remover_ingrediente(nome):
    if 'usuario' not in session:
        return redirect(url_for('login'))

    global ingredientes
    ingredientes = [ing for ing in ingredientes if ing['nome'] != nome]
    flash('Ingrediente removido com sucesso!')
    return redirect(url_for('listar_ingredientes'))

if __name__ == '__main__':
    app.run(debug=True, port=5001)
