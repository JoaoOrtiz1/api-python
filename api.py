from flask import Flask, request, jsonify
import os
import json
app = Flask(__name__)

ARQUIVO_USUARIOS = 'usuarios.json'


@app.route('/')
def index():
    return 'Bem-vindo à sua API Flask simples!'

@app.route('/calculate', methods=['POST'])
def calculate():
    print(request)
    data = request.get_json()
    print(data)
    if 'number1' not in data or 'number2' not in data or 'operation' not in data:
        return jsonify({'error': 'Certifique-se de fornecer número1, número2 e operação'}), 400

    number1 = data['number1']
    number2 = data['number2']
    operation = data['operation']

    if not (isinstance(number1, (int, float)) and isinstance(number2, (int, float))):
        return jsonify({'error': 'Número1 e número2 devem ser números'}), 400

    if operation == 'add':
        result = number1 + number2
    elif operation == 'sub':
        result = number1 - number2
    elif operation == 'mult':
        result = number1 * number2
    elif operation == 'div':
        if number2 == 0:
            return jsonify({'error': 'Não é possível dividir por zero'}), 400
        result = number1 / number2
    else:
        return jsonify({'error': 'Operação não encontrada, escolha entre: add, sub, mult, div'}), 400

    return jsonify({'result': result})


def carregar_usuarios():
    if os.path.exists(ARQUIVO_USUARIOS):
        with open(ARQUIVO_USUARIOS, 'r') as arquivo:
            return json.load(arquivo)
    return {}

def salvar_usuarios(usuarios):
    with open(ARQUIVO_USUARIOS, 'w') as arquivo:
        json.dump(usuarios, arquivo)


@app.route('/usuarios', methods=['GET', 'POST'])
@app.route('/usuarios/<int:id_usuario>', methods=['GET', 'PUT', 'DELETE'])
def usuarios(id_usuario=None):
    usuarios = carregar_usuarios()
    if request.method == 'POST':
        dados = request.json
        novo_id = max(usuarios.keys(), default=0) + 1
        usuarios[novo_id] = dados
        salvar_usuarios(usuarios)
        return jsonify({'id': novo_id}), 201
    elif request.method == 'GET':
        if id_usuario is None:
            return jsonify(usuarios)
        else:
            usuario = usuarios.get(id_usuario)
            if usuario:
                return jsonify(usuario)
            else:
                return jsonify({'erro': 'Usuário não encontrado'}), 404
    elif request.method == 'PUT':
        if id_usuario in usuarios:
            dados = request.json
            usuarios[id_usuario] = dados
            salvar_usuarios(usuarios)
            return jsonify({'sucesso': 'Usuário atualizado com sucesso'})
        else:
            return jsonify({'erro': 'Usuário não encontrado'}), 404
    elif request.method == 'DELETE':
        if id_usuario in usuarios:
            del usuarios[id_usuario]
            salvar_usuarios(usuarios)
            return jsonify({'sucesso': 'Usuário excluído com sucesso'})
        else:
            return jsonify({'erro': 'Usuário não encontrado'}), 404

ARQUIVO_TAREFAS = 'tarefas.json'

def carregar_tarefas():
    """Carrega as tarefas do arquivo JSON."""
    if os.path.exists(ARQUIVO_TAREFAS):
        with open(ARQUIVO_TAREFAS, 'r') as arquivo:
            return json.load(arquivo)
    return {}

def salvar_tarefas(tarefas):
    """Salva as tarefas no arquivo JSON."""
    with open(ARQUIVO_TAREFAS, 'w') as arquivo:
        json.dump(tarefas, arquivo)

@app.route('/tarefas', methods=['GET', 'POST'])
@app.route('/tarefas/<int:id_tarefa>', methods=['PUT', 'DELETE'])
def tarefas(id_tarefa=None):
    tarefas = carregar_tarefas()
    if request.method == 'POST':
        dados = request.json
        novo_id = max([int(k) for k in tarefas.keys()], default=0) + 1
        dados['concluida'] = False
        tarefas[novo_id] = dados
        salvar_tarefas(tarefas)
        return jsonify({'id': novo_id}), 201
    elif request.method == 'GET':
        return jsonify(tarefas)
    elif request.method == 'PUT':
        if str(id_tarefa) in tarefas:
            tarefas[str(id_tarefa)]['concluida'] = True
            salvar_tarefas(tarefas)
            return jsonify({'sucesso': 'Tarefa marcada como concluída'})
        else:
            return jsonify({'erro': 'Tarefa não encontrada'}), 404
    elif request.method == 'DELETE':
        if str(id_tarefa) in tarefas:
            del tarefas[str(id_tarefa)]
            salvar_tarefas(tarefas)
            return jsonify({'sucesso': 'Tarefa excluída com sucesso'})
        else:
            return jsonify({'erro': 'Tarefa não encontrada'}), 404


ARQUIVO_PRODUTOS = 'produtos.json'
ARQUIVO_CARRINHO = 'carrinho.json'

def carregar_dados(arquivo):
    """Carrega dados do arquivo JSON especificado."""
    if os.path.exists(arquivo):
        with open(arquivo, 'r') as f:
            return json.load(f)
    return {}

def salvar_dados(arquivo, dados):
    """Salva dados no arquivo JSON especificado."""
    with open(arquivo, 'w') as f:
        json.dump(dados, f, indent=4)

@app.route('/produtos', methods=['GET', 'POST'])
@app.route('/produtos/<int:id_produto>', methods=['PUT', 'DELETE'])
def produtos(id_produto=None):
    produtos = carregar_dados(ARQUIVO_PRODUTOS)
    if request.method == 'POST':
        dados = request.json
        novo_id = max([int(k) for k in produtos.keys()], default=0) + 1
        produtos[novo_id] = dados
        salvar_dados(ARQUIVO_PRODUTOS, produtos)
        return jsonify({'id': novo_id}), 201
    elif request.method == 'GET':
        return jsonify(produtos)
    elif request.method == 'PUT':
        if str(id_produto) in produtos:
            dados = request.json
            produtos[str(id_produto)]['estoque'] = dados.get('estoque', produtos[str(id_produto)]['estoque'])
            salvar_dados(ARQUIVO_PRODUTOS, produtos)
            return jsonify({'sucesso': 'Estoque atualizado com sucesso'})
        else:
            return jsonify({'erro': 'Produto não encontrado'}), 404
    elif request.method == 'DELETE':
        if str(id_produto) in produtos:
            del produtos[str(id_produto)]
            salvar_dados(ARQUIVO_PRODUTOS, produtos)
            return jsonify({'sucesso': 'Produto excluído com sucesso'})
        else:
            return jsonify({'erro': 'Produto não encontrado'}), 404


if __name__ == '__main__':
    app.run(debug=True)
