import time
from collections import Counter, defaultdict
from csv import reader
from pathlib import Path
from typing import DefaultDict, Dict, Iterator, List, Tuple

from tqdm import tqdm  # barra de progresso

NUMERO_DE_LINHAS = 1_000_000_000


def processar_temperaturas(path_do_csv: Path) -> Dict[str, str]:
    # utilizando infinito positivo e negativo para comparar
    minimas: DefaultDict[str, float] = defaultdict(lambda: float("inf"))
    maximas: DefaultDict[str, float] = defaultdict(lambda: float("-inf"))
    somas: DefaultDict[str, float] = defaultdict(float)
    medicoes: Counter[str] = Counter()

    with open(path_do_csv, "r", encoding="utf-8") as file:
        _reader: Iterator[List[str]] = reader(file, delimiter=";")
        # usando tqdm diretamente no iterador, isso mostrará a porcentagem de conclusão.
        for row in tqdm(_reader, total=NUMERO_DE_LINHAS, desc="Processando"):
            nome_da_station: str
            temperatura: float
            nome_da_station, temperatura = str(row[0]), float(row[1])
            medicoes.update([nome_da_station])
            minimas[nome_da_station] = min(minimas[nome_da_station], temperatura)
            maximas[nome_da_station] = max(maximas[nome_da_station], temperatura)
            somas[nome_da_station] += temperatura

    print("Dados carregados. Calculando estatísticas...")

    # calculando min, média e max para cada estação
    results: Dict[str, Tuple[float, float, float]] = {}
    for station, qtd_medicoes in medicoes.items():
        mean_temp: float = somas[station] / qtd_medicoes
        results[station] = (minimas[station], mean_temp, maximas[station])

    print("Estatística calculada. Ordenando...")
    # ordenando os resultados pelo nome da estação
    sorted_results: Dict[str, Tuple[float, float, float]] = dict(
        sorted(results.items())
    )

    # formatando os resultados para exibição
    formatted_results: Dict[str, str] = {
        station: f"{min_temp:.1f}/{mean_temp:.1f}/{max_temp:.1f}"
        for station, (min_temp, mean_temp, max_temp) in sorted_results.items()
    }

    return formatted_results


if __name__ == "__main__":
    path_do_csv: Path = Path("data/measurements.txt")

    print("Iniciando o processamento do arquivo.")
    start_time: int = time.time()  # Tempo de início

    resultados: Dict[str, str] = processar_temperaturas(path_do_csv)

    end_time: int = time.time()  # Tempo de término

    for station, metrics in resultados.items():
        print(station, metrics, sep=": ")

    print(f"\nProcessamento concluído em {end_time - start_time:.2f} segundos.")
