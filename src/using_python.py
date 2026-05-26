import csv
from collections import defaultdict, Counter
from tqdm import tqdm
import time

def processar_temperaturas(path_do_csv):
    """
    Processa um arquivo CSV contendo dados de temperatura por estação.
    
    Args:
    path_do_csv (str): Caminho para o arquivo CSV.

    Returns:
    dict: Dicionário com a estação como chave e as estatísticas de temperatura formatadas como valor.
    """
    minimas = defaultdict(lambda: float('inf'))
    maximas = defaultdict(lambda: float('-inf'))
    somas = defaultdict(float)
    medicoes = Counter()

    try:
        with open(path_do_csv, 'r') as file:
            reader = csv.reader(file, delimiter=';')
            total_linhas = sum(1 for _ in file)  # Contando o total de linhas para a barra de progresso

            file.seek(0)  # Retornando ao início do arquivo após a contagem

            for row in tqdm(reader, total=total_linhas, desc="Processando"):
                try:
                    nome_da_station, temperatura = row[0], float(row[1])
                    medicoes.update([nome_da_station])
                    minimas[nome_da_station] = min(minimas[nome_da_station], temperatura)
                    maximas[nome_da_station] = max(maximas[nome_da_station], temperatura)
                    somas[nome_da_station] += temperatura
                except ValueError:
                    # Ignora linhas com dados inválidos
                    continue

    except FileNotFoundError:
        print(f"Erro: O arquivo {path_do_csv} não foi encontrado.")
        return {}
    except Exception as e:
        print(f"Erro inesperado: {e}")
        return {}

    print("Dados carregados. Calculando estatísticas...")

    # Calculando min, média e max para cada estação
    results = {}
    for station, qtd_medicoes in medicoes.items():
        mean_temp = somas[station] / qtd_medicoes
        results[station] = (minimas[station], mean_temp, maximas[station])

    print("Estatísticas calculadas. Ordenando...")

    # Ordenando os resultados pelo nome da estação
    sorted_results = dict(sorted(results.items()))

    # Formatando os resultados para exibição
    formatted_results = {station: f"{min_temp:.1f}/{mean_temp:.1f}/{max_temp:.1f}"
                         for station, (min_temp, mean_temp, max_temp) in sorted_results.items()}

    return formatted_results

if __name__ == "__main__":
    path_do_csv = "data/measurements.txt"

    print("Iniciando o processamento do arquivo.")
    start_time = time.time()

    resultados = processar_temperaturas(path_do_csv)

    end_time = time.time()

    for station, metrics in resultados.items():
        print(station, metrics, sep=': ')

    print(f"\nProcessamento concluído em {end_time - start_time:.2f} segundos.")

# O que foi alterado:
# Tratamento de Exceções: Adicionado tratamento de exceções para problemas comuns ao abrir e ler o arquivo CSV.
# Contagem de Linhas: Ajustada a contagem de linhas para melhorar a exatidão da barra de progresso.
# Verificação de Dados: Adicionada verificação para lidar com linhas de dados inválidos.
# Comentários e Docstrings: Adicionados para melhorar a legibilidade e a documentação do código.