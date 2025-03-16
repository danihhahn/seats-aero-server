import requests
import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from milegenius import buscar_melhores_voos  # Importando a função do milegenius.py

# Carregar variáveis de ambiente
load_dotenv()
SEATS_AERO_API_KEY = os.getenv("SEATS_AERO_API_KEY")

app = Flask(__name__)

@app.route('/')
def home():
    return "API do MileGenius funcionando!"

@app.route('/buscar_voos', methods=['GET'])
def buscar_voos():
    origem = request.args.get('origem')
    destino = request.args.get('destino')
    data = request.args.get('data')

    if not origem or not destino or not data:
        return jsonify({"erro": "Parâmetros inválidos. Use origem, destino e data."}), 400

    # Chamando a função que processa os melhores voos
    melhores_voos = buscar_melhores_voos(origem, destino, data)

    return jsonify(melhores_voos)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
