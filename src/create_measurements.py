import os
import random
import sys
import time
from pathlib import Path

DATA_DIR: Path = Path("./data")
STATIONS_FILE: Path = DATA_DIR / "weather_stations.csv"
OUTPUT_FILE: Path = DATA_DIR / "measurements.txt"

NUM_ROWS_TO_CREATE: int = 1_000_000_000
BATCH_SIZE: int = 10_000
STATION_SAMPLE_SIZE: int = 10_000
COLDEST_TEMP: float = -99.9
HOTTEST_TEMP: float = 99.9


def build_weather_station_name_list() -> list[str]:
    """Lê o CSV de estações, ignora comentários e remove duplicatas."""
    station_names: list[str] = []
    with open(STATIONS_FILE, "r", encoding="utf-8") as file:
        file_contents: str = file.read()
    for station in file_contents.splitlines():
        if "#" in station:
            continue
        station_names.append(station.split(";")[0])
    return list(set(station_names))


def convert_bytes(num: float) -> str:
    """Converte bytes em formato legível (KiB, MiB, GiB)."""
    for unit in ["bytes", "KiB", "MiB", "GiB"]:
        if num < 1024.0:
            return f"{num:3.1f} {unit}"
        num /= 1024.0
    return f"{num:3.1f} TiB"


def format_elapsed_time(seconds: float) -> str:
    """Formata segundos em uma string legível (h/min/seg)."""
    if seconds < 60:
        return f"{seconds:.3f} seconds"
    if seconds < 3600:
        minutes, seconds = divmod(seconds, 60)
        return f"{int(minutes)} minutes {int(seconds)} seconds"
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    if minutes == 0:
        return f"{int(hours)} hours {int(seconds)} seconds"
    return f"{int(hours)} hours {int(minutes)} minutes {int(seconds)} seconds"


def estimate_file_size(
    weather_station_names: list[str], num_rows_to_create: int
) -> str:
    """Estima o tamanho final do arquivo de medições."""
    max_string: int = max(len(s) for s in weather_station_names)
    min_string: int = min(len(s) for s in weather_station_names)
    per_record_size: float = ((max_string + min_string * 2) + len(",-123.4")) / 2

    total_file_size: float = num_rows_to_create * per_record_size
    human_file_size: str = convert_bytes(total_file_size)

    return (
        f"O tamanho estimado do arquivo é: {human_file_size}.\n"
        f"O tamanho final será provavelmente muito menor (metade)."
    )


def build_test_data(weather_station_names: list[str], num_rows_to_create: int) -> None:
    """Gera o arquivo de medições com a quantidade de linhas solicitada."""
    start_time: float = time.time()
    station_names_sample: list[str] = random.choices(
        weather_station_names, k=STATION_SAMPLE_SIZE
    )
    print("Criando o arquivo... isso vai demorar uns 10 minutos...")

    try:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
            for _ in range(num_rows_to_create // BATCH_SIZE):
                batch: list[str] = random.choices(station_names_sample, k=BATCH_SIZE)
                prepped_batch: str = "\n".join(
                    f"{station};{random.uniform(COLDEST_TEMP, HOTTEST_TEMP):.1f}"
                    for station in batch
                )
                file.write(prepped_batch + "\n")

        sys.stdout.write("\n")
    except (IOError, OSError) as e:
        print("Erro ao escrever o arquivo. Detalhes:")
        print(e)
        sys.exit(1)

    elapsed_time: float = time.time() - start_time
    file_size: int = os.path.getsize(OUTPUT_FILE)
    human_file_size: str = convert_bytes(file_size)

    print(f"Arquivo escrito com sucesso em {OUTPUT_FILE}")
    print(f"Tamanho final: {human_file_size}")
    print(f"Tempo decorrido: {format_elapsed_time(elapsed_time)}")


def main() -> None:
    """Ponto de entrada: gera o arquivo de teste de medições."""
    weather_station_names: list[str] = build_weather_station_name_list()
    print(estimate_file_size(weather_station_names, NUM_ROWS_TO_CREATE))
    build_test_data(weather_station_names, NUM_ROWS_TO_CREATE)
    print("Arquivo de teste finalizado.")


if __name__ == "__main__":
    main()
