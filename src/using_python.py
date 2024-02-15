from csv import reader
from collections import defaultdict, Counter
import time

def processar_temperaturas(path_do_csv):
    minimas = defaultdict(lambda: 99.9)
    maximas = defaultdict(lambda: -99.9)
    somas = defaultdict(float)
    medicoes = Counter()

    with open(path_do_csv, 'r') as file:
        _reader = reader(file, delimiter=';')
        for row in _reader:
            nome_da_station, temperatura = str(row[0]), float(row[1])
            medicoes.update([nome_da_station])
            minimas[nome_da_station] = min(minimas[nome_da_station], temperatura)
            maximas[nome_da_station] = max(maximas[nome_da_station], temperatura)
            somas[nome_da_station] += temperatura

    print("Dados carregados. Calculando estatísticas...")

    # Dicionário para armazenar os resultados calculados
    results = {}

    # Calculando min, média e max para cada estação
    for station, qtd_medicoes in medicoes.items():
        mean_temp = somas[station]/qtd_medicoes
        results[station] = (minimas[station], mean_temp, maximas[station])

    print("Estatística calculada. Ordenando...")
    # Ordenando os resultados pelo nome da estação
    sorted_results = dict(sorted(results.items()))

    # Formatando os resultados para exibição
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