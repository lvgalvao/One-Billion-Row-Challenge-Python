import os
import random
import sys
import time
from typing import List, Tuple

from tqdm import tqdm  # importa o tqdm para barra de progresso


# Sanity checks out input and prints out usage if input is not a positive integer
def check_args(file_args: List[str]) -> None:

    if len(file_args) != 2 or int(file_args[1]) <= 0:
        raise Exception(
            """Usage: create_measurements.sh
            <positive integer number of records to create>
            You can use underscore notation for large number of records.
            For example:  1_000_000_000 for one billion"""
        )


# Grabs the weather station names from example data provided in repo and dedups
def build_weather_station_name_list_and_temperature_list() -> (
    Tuple[List[str], List[str]]
):

    station_names: List[str] = []
    temperatures: List[str] = []

    with open("./data/weather_stations.csv", "r", encoding="utf-8") as file:
        file_contents: str = file.read()

    for station in file_contents.splitlines():
        if "#" in station:
            continue
        else:
            station_names.append(station.split(";")[0])
            temperatures.append(station.split(";")[1])

    return list(set(station_names)), list(set(temperatures))


# Convert bytes to a human-readable format (e.g., KiB, MiB, GiB)
def convert_bytes(num: float) -> str:

    for x in ["bytes", "KiB", "MiB", "GiB"]:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0


# Format elapsed time in a human-readable format
def format_elapsed_time(seconds: float) -> str:

    if seconds < 60:
        return f"{seconds:.3f} seconds"
    elif seconds < 3600:
        minutes, seconds = divmod(seconds, 60)
        return f"{int(minutes)} minutes {int(seconds)} seconds"
    else:
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        if minutes == 0:
            return f"{int(hours)} hours {int(seconds)} seconds"
        else:
            return f"{int(hours)} hours {int(minutes)} minutes {int(seconds)} seconds"


#  Tries to estimate how large a file the test data will be
def estimate_file_size(
    weather_station_names: List[str], temperatures: List[str], num_rows_to_create: int
) -> str:

    weather_station_names_lengh: float = sum(
        len(station) for station in weather_station_names
    ) / len(weather_station_names)
    temperatures_lengh: float = sum(
        len(temperature) for temperature in temperatures
    ) / len(temperatures)

    total_file_size: float = num_rows_to_create * (
        weather_station_names_lengh + temperatures_lengh
    )
    human_file_size: str = convert_bytes(total_file_size)

    return (
        f"O tamanho estimado do arquivo é:  {human_file_size}.\n"
        "O tamanho vai variar pois o cálculo se baseou na média dos valores únicos."
    )


# Generates and writes to file the requested length of test data
def build_test_data(
    weather_station_names: List[str], temperatures: List[str], num_rows_to_create: int
):

    start_time: int = time.time()
    station_names_10k_max: List[str]
    station_names_10k_max = random.choices(weather_station_names, k=10_000)  # nosec
    # instead of writing line by line to file,
    # process a batch of stations and put it to disk
    batch_size: int = 10000
    print(
        "Criando o arquivo... Para um bilhão demora =~ uns 15 min, "
        "para 1 milhão menos de 3 seg..."
    )

    try:
        with open("./data/measurements.txt", "w", encoding="utf-8") as file:
            for _ in tqdm(
                range(0, num_rows_to_create // batch_size), desc="Processando"
            ):
                batch: List[str]
                batch = random.choices(station_names_10k_max, k=batch_size)  # nosec
                prepped_deviated_batch: str
                aleatory_temperature = random.choice(temperatures)  # nosec
                prepped_deviated_batch = "\n".join(
                    [f"{station};{aleatory_temperature}" for station in batch]
                )
                file.write(prepped_deviated_batch + "\n")

        sys.stdout.write("\n")

    except Exception as e:
        print(f"Something went wrong. Printing error info and exiting...\n{e}")
        exit()

    end_time: int = time.time()
    elapsed_time: int = end_time - start_time
    file_size: int = os.path.getsize("./data/measurements.txt")
    human_file_size: str = convert_bytes(file_size)

    print("Arquivo escrito com sucesso data/measurements.txt")
    print(f"Tamanho final:  {human_file_size}")
    print(f"Tempo decorrido: {format_elapsed_time(elapsed_time)}")


# main program function
def main():

    check_args(sys.argv)
    num_rows_to_create: int = int(sys.argv[1])
    weather_station_names, temperatures = (
        build_weather_station_name_list_and_temperature_list()
    )
    weather_station_names: List[str]  # Anotação após a atribuição (jeito certo)
    temperatures: List[str]  # Anotação após a atribuição (jeito certo)
    print(estimate_file_size(weather_station_names, temperatures, num_rows_to_create))
    build_test_data(weather_station_names, temperatures, num_rows_to_create)
    print("Arquivo de teste finalizado.")


if __name__ == "__main__":
    main()
