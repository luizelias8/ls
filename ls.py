import argparse
import datetime
import os

# Configuração do parser de argumentos
parser = argparse.ArgumentParser()

# Argumento opcional para o caminho do diretório com valor padrão para o diretório atual
parser.add_argument('path', nargs='?', default=os.getcwd(), help='Caminho do diretório (padrão: diretório atual)')

# Argumento opcional para formato longo
parser.add_argument('-l', '--long', action='store_true', help='Exibe informações detalhadas dos arquivos')

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

# Itera pelos arquivos no diretório
for entry in os.listdir(target_dir):
    entry_path = os.path.join(target_dir, entry) # Constrói o caminho completo do arquivo
    print(build_output(entry_path, long=args.long))