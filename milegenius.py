import requests
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()
SEATS_AERO_API_KEY = os.getenv("SEATS_AERO_API_KEY")

# Tabela de preços médios do milheiro
MILHEIRO_PRECOS = {
    "Smiles": 16.00,
    "Latam Pass": 25.00,
    "Azul Fidelidade": 16.50,
    "TAP Miles": 45.00,
    "Iberia Plus": 49.80,
    "Flying Blue": 60.00,
    "Privilege Club": 55.00,
    "Summa": 71.00,
    "Mileage Plan": 83.00,
    "AAdvantage": 92.50,
    "Connect Miles": 68.00
}

def buscar_melhores_voos(origem, destino, data):
    url = f"https://seats.aero/partnerapi/search?origin_airport={origem}&destination_airport={destino}&start_date={data}&end_date={data}"
    headers = {"Partner-Authorization": f"{SEATS_AERO_API_KEY}", "Accept": "application/json"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return {"erro": f"Erro na requisição: {response.status_code}", "detalhes": response.text}

    dados = response.json()
    melhores_opcoes = []

    for voo in dados.get("data", []):
        # Priorizar Business Class, mas considerar Econômica se for mais barata
        if voo.get("JAvailable", False):
            classe = "Executiva"
            milhas = int(voo.get("JMileageCostRaw", 0))
            programa = voo.get("Source", "Desconhecido")
        elif voo.get("YAvailable", False):
            classe = "Econômica"
            milhas
