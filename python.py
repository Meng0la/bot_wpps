from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Caminho do banco
DB_PATH = 'pecas_empilhadeira_pronto.db'

# Função para buscar no banco
def buscar_peca(marca, tipo_energia, modelo, motor):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT nome_peca, codigo_peca, observacoes
        FROM pecas
        WHERE marca_empilhadeira = ?
        AND tipo_energia = ?
        AND modelo = ?
        AND motor = ?
    ''', (marca, tipo_energia, modelo, motor))
    resultado = cursor.fetchall()
    conn.close()
    return resultado

# Rota principal de consulta
@app.route('/consultar', methods=['POST'])
def consultar():
    data = request.get_json()

    # Captura os dados enviados
    marca = data.get('marca')
    tipo_energia = data.get('tipo_energia')
    modelo = data.get('modelo')
    motor = data.get('motor')

    if not all([marca, tipo_energia, modelo, motor]):
        return jsonify({'erro': 'Faltam parâmetros na requisição'}), 400

    resultado = buscar_peca(marca, tipo_energia, modelo, motor)

    if resultado:
        resposta = []
        for nome_peca, codigo_peca, observacoes in resultado:
            resposta.append({
                'nome_peca': nome_peca,
                'codigo_peca': codigo_peca,
                'observacoes': observacoes
            })
        return jsonify(resposta)
    else:
        return jsonify({'mensagem': 'Peça não encontrada'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
