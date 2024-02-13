from csv import reader
from collections import defaultdict
import time
from concurrent.futures import ThreadPoolExecutor

def processar_batch(batch):
    temperatura_por_station = defaultdict(list)
    for nome_da_station, temperatura in batch:
        temperatura_por_station[nome_da_station].append(float(temperatura))
    return temperatura_por_station

def combinar_resultados(resultados):
    temperatura_final_por_station = defaultdict(list)
    for resultado in resultados:
        for station, temperatures in resultado.items():
            temperatura_final_por_station[station].extend(temperatures)
    return temperatura_final_por_station

def calcular_estatisticas(temperatura_por_station):
    results = {}
    for station, temperatures in temperatura_por_station.items():
        min_temp = min(temperatures)
        mean_temp = sum(temperatures) / len(temperatures)
        max_temp = max(temperatures)
        results[station] = (min_temp, mean_temp, max_temp)
    return results

def processar_temperaturas(path_do_csv, num_workers=4):
    print("Iniciando o processamento do arquivo.")
    start_time = time.time()

    with open(path_do_csv, 'r') as file:
        linhas = list(reader(file, delimiter=';'))

    batch_size = len(linhas) // num_workers + (len(linhas) % num_workers > 0)
    batches = [linhas[i:i + batch_size] for i in range(0, len(linhas), batch_size)]

    print("Processando em paralelo com threads...")
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        resultados_paralelos = list(executor.map(processar_batch, batches))

    temperatura_por_station = combinar_resultados(resultados_paralelos)
    resultados_finais = calcular_estatisticas(temperatura_por_station)

    print("Ordenando em paralelo com threads...")
    sorted_results = dict(sorted(resultados_finais.items()))
    formatted_results = {station: f"{min_temp:.1f}/{mean_temp:.1f}/{max_temp:.1f}" for station, (min_temp, mean_temp, max_temp) in sorted_results.items()}

    end_time = time.time()
    print(f"Processamento concluído em {end_time - start_time:.2f} segundos.")
    return formatted_results

# Ajuste o caminho do arquivo conforme necessário
if __name__ == "__main__":
    path_do_csv = "data/measurements100M.txt"
    # 10M 10 segundos.
    resultados = processar_temperaturas(path_do_csv, num_workers=4)