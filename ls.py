import argparse
import datetime
import os

# Configuração do parser de argumentos
parser = argparse.ArgumentParser()

# Argumento opcional para o caminho do diretório com valor padrão para o diretório atual
parser.add_argument('path', nargs='?', default=os.getcwd(), help='Caminho do diretório (padrão: diretório atual)')

# Argumento opcional para formato longo
parser.add_argument('-l', '--long', action='store_true', help='Exibe informações detalhadas dos arquivos')

# Flag para listar subdiretórios de forma recursiva
parser.add_argument('-r', '--recursive', action='store_true', help='Lista arquivos e subdiretórios de forma recursiva')

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
        return f'{size:>6d} {date} {os.path.basename(entry)}' # Formata a saída para o formato longo
    return os.path.basename(entry) # Retorna apenas o nome do arquivo

# Função para listar arquivos no diretório, possivelmente de forma recursiva
def list_files(base_dir, recursive=False, long=False):
    if recursive:
        # Uso de os.walk para listar de forma recursiva
        for root, dirs, files in os.walk(base_dir):
            for name in files:
                file_path = os.path.join(root, name) # Constrói o caminho completo do arquivo
                print(build_output(file_path, long=long))
            for name in dirs:
                dir_path = os.path.join(root, name) # Constrói o caminho completo do subdiretório
                print(build_output(dir_path, long=long))
    else:
        # Uso de os.listdir para listar apenas o conteúdo do diretório base
        for entry in os.listdir(base_dir):
            entry_path = os.path.join(base_dir, entry) # Constrói o caminho completo do arquivo
            print(build_output(entry_path, long=long))

# Chamada da função para listar arquivos
list_files(target_dir, recursive=args.recursive, long=args.long)