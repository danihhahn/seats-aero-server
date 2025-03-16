import requests
import json
import pandas as pd

# Função para buscar voos na API
def buscar_voos(origem, destino, data):
    url = f"https://seats-aero-server.onrender.com/buscar_voos?origem={origem}&destino={destino}&data={data}"
    
    try:
        resposta = requests.get(url)
        resposta.raise_for_status()  # Gera erro se a resposta não for 200
        dados = resposta.json()

        # Exibir resposta formatada para depuração
        print("\n🔹 Resposta da API:")
        print(json.dumps(dados, indent=4, ensure_ascii=False))

        return dados

    except requests.exceptions.RequestException as e:
        print(f"❌ Erro na requisição: {e}")
        return None

# Função para formatar os resultados em tabela
def formatar_resultados(dados):
    voos = []

    for voo in dados.get("data", []):
        voos.append({
            "Data": voo.get("Date", "N/A"),
            "Origem": voo.get("Route", {}).get("OriginAirport", "N/A"),
            "Destino": voo.get("Route", {}).get("DestinationAirport", "N/A"),
            "Companhia": voo.get("YAirlinesRaw", "N/A"),  # Ajustado para buscar a informação correta
            "Milhas": voo.get("YMileageCostRaw", "N/A"),  # Ajustado para buscar a informação correta
            "Cabine": voo.get("Cabin", "Econômica"),  # Definindo padrão para evitar "N/A"
            "Assentos Disponíveis": voo.get("YRemainingSeatsRaw", "N/A")  # Ajustado para buscar a informação correta
        })

    if voos:
        df = pd.DataFrame(voos)
        print("\n🛫 Voos Encontrados:")
        print(df.to_string(index=False))
    else:
        print("\n⚠️ Nenhum voo encontrado.")

# Entrada do usuário
if __name__ == "__main__":
    origem = input("Digite o aeroporto de origem (ex: MIA): ").strip().upper()
    destino = input("Digite o aeroporto de destino (ex: JFK): ").strip().upper()
    data = input("Digite a data de partida (YYYY-MM-DD): ").strip()

    # Buscar e formatar os voos
    resultados = buscar_voos(origem, destino, data)
    if resultados:
        formatar_resultados(resultados)