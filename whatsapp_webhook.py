from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import sqlite3

app = Flask(__name__)

DB_PATH = 'pecas_empilhadeira_pronto.db'

estado_usuario = {}

@app.route('/', methods=['GET'])
def home():
    return "API funcionando! 🚀"

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

@app.route('/whatsapp', methods=['POST'])
def whatsapp():
    numero = request.form.get('From')
    mensagem = request.form.get('Body').strip()

    resposta = MessagingResponse()
    msg = resposta.message()

    if numero not in estado_usuario:
        estado_usuario[numero] = {"etapa": "marca"}
        msg.body("👋 Olá! Qual é a marca da empilhadeira? (Ex: Yale, Hyster)")
        return str(resposta)

    user = estado_usuario[numero]

    if user['etapa'] == 'marca':
        user['marca'] = mensagem
        user['etapa'] = 'tipo_energia'
        msg.body("🔋 É elétrica, GLP ou diesel?")
        return str(resposta)

    if user['etapa'] == 'tipo_energia':
        user['tipo_energia'] = mensagem
        user['etapa'] = 'modelo'
        msg.body("📦 Qual é o modelo da empilhadeira? (Ex: GDP50VX, 70VX...)")
        return str(resposta)

    if user['etapa'] == 'modelo':
        user['modelo'] = mensagem
        user['etapa'] = 'motor'
        msg.body("⚙️ Qual é o motor? (Ex: Kubota 3.8L, GM, PSI...)")
        return str(resposta)

    if user['etapa'] == 'motor':
        user['motor'] = mensagem

        resultado = buscar_peca(
            user['marca'], 
            user['tipo_energia'], 
            user['modelo'], 
            user['motor']
        )

        if resultado:
            resposta_texto = "✅ Peças encontradas:\n"
            for nome, codigo, obs in resultado:
                resposta_texto += f"\n📦 {nome}\n🔧 Código: {codigo}\nℹ️ {obs}\n"
        else:
            resposta_texto = "❌ Nenhuma peça encontrada com essas informações."

        msg.body(resposta_texto + "\n\nSe quiser consultar outra peça, envie qualquer mensagem.")
        estado_usuario.pop(numero)  # Reinicia o fluxo
        return str(resposta)

    msg.body("❌ Não entendi. Vamos começar de novo. Qual é a marca da empilhadeira?")
    estado_usuario.pop(numero)
    return str(resposta)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
