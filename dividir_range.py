import argparse

def create_ranges(start_hex, end_hex, num_divisions, filename):
    # Converte os valores hexadecimais para inteiros
    start = int(start_hex, 16)
    end = int(end_hex, 16)

    # Calcula o tamanho de cada subdivisão
    step = (end - start) // num_divisions

    # Abre o arquivo para escrita
    with open(filename, 'w') as file:
        for i in range(num_divisions):
            range_start = start + i * step
            range_end = start + (i + 1) * step if i < num_divisions - 1 else end
            
            # Converte os ranges de volta para hexadecimal
            file.write(f"{hex(range_start).upper()[2:]}:{hex(range_end).upper()[2:]}:0\n")

def main():
    # Configura o parser de argumentos
    parser = argparse.ArgumentParser(description='Cria um arquivo com ranges subdivididos em hexadecimal.')
    parser.add_argument('start', type=str, help='Valor inicial do range em hexadecimal (ex: 5000000).')
    parser.add_argument('end', type=str, help='Valor final do range em hexadecimal (ex: 6000000).')
    parser.add_argument('num_divisions', type=int, help='Número de divisões do range.')
    parser.add_argument('filename', type=str, help='Nome do arquivo de saída.')

    # Lê os argumentos
    args = parser.parse_args()

    # Chama a função para criar os ranges
    create_ranges(args.start, args.end, args.num_divisions, args.filename)

if __name__ == '__main__':
    main()
