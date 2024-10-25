import random
import argparse

def shuffle_file_lines(input_filename, output_filename):
    # Lê o arquivo e armazena as linhas em uma lista
    with open(input_filename, 'r') as file:
        lines = file.readlines()

    # Embaralha as linhas
    random.shuffle(lines)

    # Escreve as linhas embaralhadas em um novo arquivo
    with open(output_filename, 'w') as file:
        file.writelines(lines)

def main():
    # Configura o parser de argumentos
    parser = argparse.ArgumentParser(description='Embaralha as linhas de um arquivo.')
    parser.add_argument('input_file', type=str, help='Nome do arquivo de entrada.')
    parser.add_argument('output_file', type=str, help='Nome do arquivo de saída.')

    # Lê os argumentos
    args = parser.parse_args()

    # Chama a função para embaralhar as linhas
    shuffle_file_lines(args.input_file, args.output_file)
    print(f"As linhas de {args.input_file} foram embaralhadas e salvas em {args.output_file}.")

if __name__ == '__main__':
    main()
