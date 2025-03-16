from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()
SEATS_AERO_API_KEY = os.getenv("SEATS_AERO_API_KEY")

app = Flask(__name__)

@app.route('/')
def home():
    return "API do Seats.aero funcionando!" 

@app.route('/buscar_voos', methods=['GET'])
def buscar_voos():
    origem = request.args.get('origem')
    destino = request.args.get('destino')
    data = request.args.get('data')

    if not origem or not destino or not data:
        return jsonify({"erro": "Parâmetros inválidos. Use origem, destino e data."}), 400

    url = f"https://seats.aero/partnerapi/search?origin_airport={origem}&destination_airport={destino}&start_date={data}&end_date={data}"
    headers = {
        "Partner-Authorization": f"{SEATS_AERO_API_KEY}",
        "Accept": "application/json"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return jsonify({"erro": f"Erro na requisição: {response.status_code}", "detalhes": response.text})

    dados = response.json()
    
    # Formatar os dados para garantir a exibição correta
    voos_formatados = []
    for voo in dados.get("data", []):
        voos_formatados.append({
            "Data": voo.get("Date", "N/A"),
            "Origem": voo.get("Route", {}).get("OriginAirport", "N/A"),
            "Destino": voo.get("Route", {}).get("DestinationAirport", "N/A"),
            "Companhia": voo.get("YAirlinesRaw", "N/A"),  # Companhia aérea
            "Milhas": voo.get("YMileageCostRaw", "N/A"),  # Custo em milhas
            "Cabine": "Econômica" if voo.get("YAvailableRaw", False) else "N/A",  # Tipo de cabine
            "Assentos Disponíveis": voo.get("YRemainingSeatsRaw", "N/A")  # Quantidade de assentos disponíveis
        })

    if not voos_formatados:
        return jsonify({"mensagem": "Nenhum voo encontrado."})

    return jsonify({"voos_encontrados": voos_formatados})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)