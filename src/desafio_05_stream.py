from collections import defaultdict
import time

def processar_temperaturas_stream(path_do_csv):
    start_time = time.time()
    print("Iniciando o processamento do arquivo em stream.")
    
    temperatura_por_station = defaultdict(list)

    with open(path_do_csv, 'r') as file:
        for line in file:
            nome_da_station, temperatura = line.strip().split(';')
            temperatura_por_station[nome_da_station].append(float(temperatura))

    print("Calculando...")
    # Calculando min, média e max para cada estação
    results = {}
    for station, temperatures in temperatura_por_station.items():
        min_temp = min(temperatures)
        mean_temp = sum(temperatures) / len(temperatures)
        max_temp = max(temperatures)
        results[station] = (min_temp, mean_temp, max_temp)


    # Ordenando os resultados pelo nome da estação e formatando para impressão
    sorted_results = dict(sorted(results.items()))
    formatted_results = {station: f"{min_temp:.1f}/{mean_temp:.1f}/{max_temp:.1f}" for station, (min_temp, mean_temp, max_temp) in sorted_results.items()}
    end_time = time.time()
    print(f"Processamento concluído. Tempo de execução: {end_time - start_time:.2f} segundos.")
    return formatted_results

# Substitua o caminho do arquivo conforme necessário
if __name__ == "__main__":
    path_do_csv = "data/measurements100M.txt"
    resultados = processar_temperaturas_stream(path_do_csv)