import argparse
import datetime
import os

# Configuração do parser de argumentos
parser = argparse.ArgumentParser(
    prog='ls',
    description='Script para listar arquivos e diretórios.',
    epilog='Obrigado por usar %(prog)s! :)',
    allow_abbrev=False # Desativa abreviação automática de opções
)

# Argumento opcional para o caminho do diretório com valor padrão para o diretório atual
parser.add_argument('path', nargs='?', default=os.getcwd(), help='Caminho do diretório (padrão: diretório atual)')

# Argumento opcional para formato longo
parser.add_argument('-l', '--long', action='store_true', help='Exibe informações detalhadas dos arquivos')

# Flag para listar subdiretórios de forma recursiva
parser.add_argument('-r', '--recursive', action='store_true', help='Lista arquivos e subdiretórios de forma recursiva')

# Argumento opcional para filtrar por tipo de arquivo
parser.add_argument(
    '-f', '--filter',
    choices=['files', 'dirs', 'all'],
    default='all',
    help='Filtrar por tipo de conteúdo: `files` para listar apenas arquivos, `dirs` para listar apenas diretórios, `all` (padrão) para listar ambos'
)

# Argumento opcional para exportar para arquivo
parser.add_argument('-o', '--output', metavar='ARQUIVO', help='Exporta a saída para o arquivo especificado')

# Flag para contagem de arquivos e diretórios
parser.add_argument('-c', '--count', action='store_true', help='Exibe a contagem de arquivos e diretórios')

args = parser.parse_args() # Parse dos argumentos

target_dir = args.path # Atribui o caminho fornecido à variável target_dir

# Verifica se o diretório existe
if not os.path.exists(target_dir):
    print("The target directory doesn't exist")
    raise SystemExit(1)

# Função para construir a saída formatada
def build_output(entry, long=False):
    if long:
        size = os.path.getsize(entry) # Obtém o tamanho do arquivo
        date = datetime.datetime.fromtimestamp(
            os.path.getmtime(entry) # Obtém a data de modificação do arquivo
        ).strftime('%b %d %H:%M:%S')
        file_type = 'd' if os.path.isdir(entry) else '-'
        return f'{file_type} {size:>6d} {date} {os.path.basename(entry)}' # Formata a saída para o formato longo
    return os.path.basename(entry) # Retorna apenas o nome do arquivo

# Função para listar arquivos no diretório, possivelmente de forma recursiva
def list_files(base_dir, recursive=False, long=False, filter_type='all'):
    output_lines = [] # Lista para armazenar as linhas de saída
    file_count = 0 # Contador de arquivos
    dir_count = 0 # Contador de diretórios

    if recursive:
        # Uso de os.walk para listar de forma recursiva
        for root, dirs, files in os.walk(base_dir):
            for name in files:
                file_path = os.path.join(root, name) # Constrói o caminho completo do arquivo
                if filter_type in ['files', 'all']:
                    output_lines.append(build_output(file_path, long=long))
                    file_count += 1 # Incrementa o contador de arquivos
            for name in dirs:
                dir_path = os.path.join(root, name) # Constrói o caminho completo do subdiretório
                if filter_type in ['dirs', 'all']:
                    output_lines.append(build_output(dir_path, long=long))
                    dir_count += 1 # Incrementa o contador de diretórios
    else:
        # Uso de os.listdir para listar apenas o conteúdo do diretório base
        for entry in os.listdir(base_dir):
            entry_path = os.path.join(base_dir, entry) # Constrói o caminho completo do arquivo
            if os.path.isfile(entry_path) and filter_type in ['files', 'all']:
                output_lines.append(build_output(entry_path, long=long))
                file_count += 1 # Incrementa o contador de arquivos
            elif os.path.isdir(entry_path) and filter_type in ['dirs', 'all']:
                output_lines.append(build_output(entry_path, long=long))
                dir_count += 1 # Incrementa o contador de diretórios

    return output_lines, file_count, dir_count

# Função para exportar a lista para um arquivo
def export_to_file(output_file, lines):
    with open(output_file, 'w') as f:
        for line in lines:
            f.write(line + '\n')

# Chamada da função para listar arquivos
output_lines, file_count, dir_count = list_files(target_dir, recursive=args.recursive, long=args.long, filter_type=args.filter)

# Se especificado, exporta para arquivo
if args.output:
    export_to_file(args.output, output_lines)
else:
    # Caso contrário, imprime na saída padrão
    for line in output_lines:
        print(line)

# Exibe a contagem de arquivos e diretórios, se solicitado
if args.count:
    print(f'\nTotal de arquivos: {file_count}')
    print(f'Total de diretórios: {dir_count}')