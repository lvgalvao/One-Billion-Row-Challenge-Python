from csv import reader
from collections import defaultdict
from tqdm import tqdm  # barra de progresso
import time
import sys
sys.stdout.reconfigure(encoding='utf-8')

NUMERO_DE_LINHAS = 1_000_000_000

def processar_temperaturas(path_do_csv):
    # utilizando infinito positivo e negativo para comparar
    estatisticas = defaultdict(
    lambda: [float('inf'), float('-inf'), 0, 0]
)

    with open(path_do_csv, 'r', encoding='utf-8') as file:
        _reader = reader(file, delimiter=';')
        # usando tqdm diretamente no iterador, isso mostrará a porcentagem de conclusão.
        for row in tqdm(_reader, total=NUMERO_DE_LINHAS, desc="Processando"):
            nome_da_station, temperatura = row[0], float(row[1])

            dados = estatisticas[nome_da_station]

            dados[0] = min(dados[0], temperatura)
            dados[1] = max(dados[1], temperatura)
            dados[2] += temperatura
            dados[3] += 1

    print("Dados carregados. Calculando estatísticas...")

    # calculando min, média e max para cada estação
    results = {}
    for station, dados in estatisticas.items():
        minimo, maximo, soma, quantidade = dados

        mean_temp = soma / quantidade

        results[station] = (
            minimo,
            mean_temp,
            maximo
        )

    print("Estatística calculada. Ordenando...")
    # ordenando os resultados pelo nome da estação
    sorted_results = dict(sorted(results.items()))

    # formatando os resultados para exibição
    formatted_results = {station: f"{min_temp:.1f}/{mean_temp:.1f}/{max_temp:.1f}"
                         for station, (min_temp, mean_temp, max_temp) in sorted_results.items()}

    return formatted_results


if __name__ == "__main__":
    path_do_csv = "data/measurements.txt"

    print("Iniciando o processamento do arquivo.")
    start_time = time.time()  # Tempo de início

    resultados = processar_temperaturas(path_do_csv)

    end_time = time.time()  # Tempo de término

    for station, metrics in resultados.items():
        print(station, metrics, sep=': ')

    print(f"\nProcessamento concluído em {end_time - start_time:.2f} segundos.")
