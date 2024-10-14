import os
import random
import subprocess
import time
from datetime import datetime

# Parâmetros base
start_range = int("40000000000000000", 16)
end_range = int("7ffffffffffffffff", 16)
total_subranges = 10000000
address = "1BY8GQbnueYofwSuFAT3USAhGjPrkxDdW9"
output_file = "67.txt"
log_file = "ranges_verificados-67.tsv"

# Tamanho de cada subrange
subrange_size = (end_range - start_range) // total_subranges

# Função para gerar um subrange aleatório
def gerar_subrange():
    subrange_start = random.randint(start_range, end_range - subrange_size)
    subrange_end = subrange_start + subrange_size
    return hex(subrange_start), hex(subrange_end)

# Função para verificar se o subrange já foi escaneado
def ja_escaneado(subrange_start, subrange_end):
    if os.path.exists(log_file):
        with open(log_file, 'r') as f:
            for linha in f:
                if f"{subrange_start}:{subrange_end}" in linha:
                    return True
    return False

# Função para salvar o subrange no arquivo de log
def salvar_subrange(subrange_start, subrange_end):
    with open(log_file, 'a') as f:
        f.write(f"{datetime.now()}: {subrange_start}:{subrange_end}\n")

# Função para executar o KeyHunt
def executar_keyhunt(subrange_start, subrange_end):
    comando = [
        "./KeyHunt", "--gpu", "-m", "address", address, 
        "--range", f"{subrange_start}:{subrange_end}", 
        "--coin", "BTC", "-o", output_file,
    ]
    subprocess.run(comando)

# Função principal
def gerenciar_busca():
    subranges_verificados = 0
    inicio = time.time()  # Tempo de início do escaneamento
    proxima_atualizacao = inicio + 3600  # Próxima atualização em uma hora

    # Log de início da verificação
    with open(log_file, 'a') as f:
        f.write(f"Início do escaneamento: {datetime.now()}\n")
    
    try:
        while subranges_verificados < total_subranges:
            # Sorteia um novo subrange
            subrange_start, subrange_end = gerar_subrange()

            # Verifica se já foi escaneado
            if ja_escaneado(subrange_start, subrange_end):
                continue

            # Salva o subrange como iniciado no log
            salvar_subrange(subrange_start, subrange_end)

            # Executa o software com o subrange
            print(f"Escaneando range {subrange_start}:{subrange_end}")
            executar_keyhunt(subrange_start, subrange_end)

            # Incrementa o contador de subranges verificados
            subranges_verificados += 1
            print(f"Subranges verificados: {subranges_verificados}/{total_subranges}")

            # Verifica se já passou uma hora para atualizar o log
            if time.time() >= proxima_atualizacao:
                with open(log_file, 'a') as f:
                    progresso = f"Progresso após {subranges_verificados} subranges verificados às {datetime.now()}\n"
                    f.write(progresso)
                proxima_atualizacao += 3600  # Atualiza a próxima hora para logar novamente

    except KeyboardInterrupt:
        print("\nEncerrando, aguarde...")
        time.sleep(2)
        print("Processo interrompido com sucesso.")

if __name__ == "__main__":
    gerenciar_busca()
