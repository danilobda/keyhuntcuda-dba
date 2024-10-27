import subprocess
import argparse
import signal
import sys
import requests
import json
from datetime import datetime
from urllib.parse import urljoin

# Token para a requisição POST
TOKEN = "bae56f07-63ce-4f8f-9a49-c5cc80048448"

# Função para lidar com o sinal de interrupção
def signal_handler(sig, frame):
    print("\nInterrupção detectada. Saindo...")
    sys.exit(0)

# Função para buscar os ranges via HTTP
def obter_ranges(api_url):
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Lança uma exceção para erros HTTP
        data = response.json()
        return data['enderecoInicial'], data['enderecoFinal']
    except requests.exceptions.RequestException as e:
        print(f"Erro ao obter dados da API: {e}")
        return None, None

# Função para informar a pesquisa após execução
def informar_pesquisa(base_url, endereco_inicial, endereco_final):
    url = urljoin(base_url, "/subranges/informar-pesquisa")
    payload = {
        "enderecoInicial": endereco_inicial,
        "enderecoFinal": endereco_final,
        "bits": 67,
        "token": TOKEN
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Verifica se a solicitação foi bem-sucedida
        print(f"Pesquisa informada com sucesso: {payload}")
    except requests.exceptions.RequestException as e:
        print(f"Erro ao informar a pesquisa: {e}")

# Função para processar e executar o comando com os ranges obtidos
def process_ranges(api_url, address):
    while True:
        # Obtém os ranges inicial e final do endpoint
        range_start, range_end = obter_ranges(api_url)
        
        # Se não conseguir obter os ranges, interrompe a execução
        if not range_start or not range_end:
            print("Não foi possível obter os ranges. Encerrando.")
            break

        # Montar o comando com os ranges obtidos
        command = f"./KeyHunt -t 0 -g --gpui 0 --gpux 4096,512 -m address --coin BTC --range {range_start}:{range_end} {address}"

        # Executa o comando e exibe a saída no terminal
        print(f"Executando: {command}")
        result = subprocess.run(command, shell=True)

        # Registra o resultado no log com o range inicial e final
        log_entry = f"{datetime.now()} - Range Inicial: {range_start}, Range Final: {range_end} - Comando: {command} - Retorno: {result.returncode}\n"
        with open("execucao_log.txt", "a") as log_file:
            log_file.write(log_entry)

        # Verifica se a execução foi bem-sucedida
        if result.returncode == 0:
            print("Execução concluída com sucesso.")
            # Envia a informação da pesquisa ao servidor
            informar_pesquisa(api_url, range_start, range_end)
        else:
            print("Erro durante a execução do comando.")
            break  # Interrompe o loop em caso de erro

def main():
    # Configura o parser de argumentos
    parser = argparse.ArgumentParser(description='Processa ranges obtidos via HTTP.')
    parser.add_argument('api_url', type=str, help='URL da API para obter os ranges.')
    parser.add_argument('address', type=str, help='Endereço para usar na execução.')

    # Lê os argumentos
    args = parser.parse_args()

    # Registra o manipulador de sinal
    signal.signal(signal.SIGINT, signal_handler)

    # Chama a função com o URL da API e o endereço
    process_ranges(args.api_url, args.address)

if __name__ == '__main__':
    main()
