import requests
import sys

def obter_pais_por_cidade(nome_cidade, chave_api):
    url = f'https://api.opencagedata.com/geocode/v1/json?q={nome_cidade}&key={chave_api}&language=pt'
    response = requests.get(url)
   
    if response.status_code == 200:
        data = response.json()

        if 'results' in data and len(data['results']) > 0:
            pais = data['results'][0]['components']['country']
            return pais
        else:
            return None
    else:
        print(f'Erro ao fazer requisição: {response.status_code}')
        return None

def main():
    if len(sys.argv) != 3:
        print('Uso: python script.py <nome_cidade> <chave_api>')
        return

    cidade = sys.argv[1]
    chave_api = sys.argv[2]

    pais = obter_pais_por_cidade(cidade, chave_api)

    if pais:
        print(pais)
        print("-----------------------------------") 
    else:
        print(f'Não foi possível encontrar informações para a cidade de {cidade}')
        print("-----------------------------------") 

if __name__ == "__main__":
    main()
