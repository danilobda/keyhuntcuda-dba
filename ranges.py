import subprocess
import argparse
import signal
import sys

# Variável global para armazenar o caminho do arquivo
file_path = None

# Função para lidar com o sinal de interrupção
def signal_handler(sig, frame):
    print("\nInterrupção detectada. Saindo...")
    sys.exit(0)

# Função para ler o arquivo e processar os ranges
def process_ranges(file_path_param, address):
    global file_path
    file_path = file_path_param

    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Processar cada linha
    for index, line in enumerate(lines):
        # Remover espaços e quebras de linha
        line = line.strip()
        # Ignorar linhas vazias
        if not line:
            continue

        # Dividir os dados da linha
        parts = line.split(':')
        if len(parts) != 3:
            continue  # Se a linha não tiver 3 partes, ignorar
        
        range_start = parts[0].strip()  # Primeiro dado (range inicial)
        range_end = parts[1].strip()    # Segundo dado (range final)
        executed = parts[2].strip()     # Status de execução (0 ou 1)

        # Executar apenas se ainda não foi executado
        if executed == '0':
            # Formatar o comando com os parâmetros fornecidos
            command = f"./KeyHunt -t 0 -g --gpui 0 --gpux 4096,512 -m address --coin BTC --range {range_start}:{range_end} {address}"

            # Executar o comando e imprimir a saída no terminal
            print(f"Executando: {command}")
            result = subprocess.run(command, shell=True)  # Execute e mostre a saída

            # Verifica se a execução foi bem-sucedida
            if result.returncode == 0:
                print("Execução concluída com sucesso.")
                # Atualizar o status para '1' na linha correspondente
                lines[index] = f"{range_start}:{range_end}:1\n"  # Atualiza a linha

                # Gravar apenas a linha alterada no arquivo
                with open(file_path, 'w') as file:
                    file.writelines(lines)
                # Interrompe o loop após a primeira execução bem-sucedida
            else:
                print("Erro durante a execução do comando.")
                break  # Interrompe o loop em caso de erro também

def main():
    # Configura o parser de argumentos
    parser = argparse.ArgumentParser(description='Processa ranges de um arquivo.')
    parser.add_argument('file_path', type=str, help='Nome do arquivo contendo os ranges.')
    parser.add_argument('address', type=str, help='Endereço para usar na execução.')

    # Lê os argumentos
    args = parser.parse_args()

    # Registra o manipulador de sinal
    signal.signal(signal.SIGINT, signal_handler)

    # Chama a função com o nome do arquivo e o endereço
    process_ranges(args.file_path, args.address)

if __name__ == '__main__':
    main()
