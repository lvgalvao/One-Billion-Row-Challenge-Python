import os
import sys
import random
import time
import tempfile   # cria arquivos temporários
import atexit     # registra funções para rodar ao encerrar o programa
import argparse   # lê argumentos da linha de comando (ex: --temp)


def check_args(file_args):
    """
    Sanity checks out input and prints out usage if input is not a positive integer
    """
    try:
        if len(file_args) != 2 or int(file_args[1]) <= 0:
            raise Exception()
    except:
        print(
            "Usage:  create_measurements.sh <positive integer number of records to create>")
        print("        You can use underscore notation for large number of records.")
        print("        For example:  1_000_000_000 for one billion")
        exit()


def build_weather_station_name_list():
    """
    Grabs the weather station names from example data provided in repo and dedups
    """
    station_names = []
    with open('./data/weather_stations.csv', 'r', encoding="utf-8") as file:
        file_contents = file.read()
    for station in file_contents.splitlines():
        if "#" in station:
            continue
        else:
            station_names.append(station.split(';')[0])
    return list(set(station_names))


def convert_bytes(num):
    """
    Convert bytes to a human-readable format (e.g., KiB, MiB, GiB)
    """
    for x in ['bytes', 'KiB', 'MiB', 'GiB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0


def format_elapsed_time(seconds):
    """
    Format elapsed time in a human-readable format
    """
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


def estimate_file_size(weather_station_names, num_rows_to_create):
    """
    Tries to estimate how large a file the test data will be
    """
    max_string = float('-inf')
    min_string = float('inf')
    per_record_size = 0
    record_size_unit = "bytes"

    for station in weather_station_names:
        if len(station) > max_string:
            max_string = len(station)
        if len(station) < min_string:
            min_string = len(station)
        per_record_size = ((max_string + min_string * 2) + len(",-123.4")) / 2

    total_file_size = num_rows_to_create * per_record_size
    human_file_size = convert_bytes(total_file_size)

    return f"O tamanho estimado do arquivo é:  {human_file_size}.\nO tamanho final será provavelmente muito menor (metade)."


def build_test_data(weather_station_names, num_rows_to_create, output_path="./data/measurements.txt"):
    """
    Generates and writes to file the requested length of test data
    """
    start_time = time.time()
    coldest_temp = -99.9
    hottest_temp = 99.9
    station_names_10k_max = random.choices(weather_station_names, k=10_000)
    # instead of writing line by line to file, process a batch of stations and put it to disk
    batch_size = 10000
    progress_step = max(1, (num_rows_to_create // batch_size) // 100)
    print('Criando o arquivo... isso vai demorar uns 10 minutos...')

    try:
        with open(output_path, 'w', encoding="utf-8") as file:
            for s in range(0, num_rows_to_create // batch_size):

                batch = random.choices(station_names_10k_max, k=batch_size)
                # :.1f should quicker than round on a large scale, because round utilizes mathematical operation
                prepped_deviated_batch = '\n'.join(
                    [f"{station};{random.uniform(coldest_temp, hottest_temp):.1f}" for station in batch])
                file.write(prepped_deviated_batch + '\n')

        sys.stdout.write('\n')
    except Exception as e:
        print("Something went wrong. Printing error info and exiting...")
        print(e)
        exit()

    end_time = time.time()
    elapsed_time = end_time - start_time
    file_size = os.path.getsize(output_path)
    human_file_size = convert_bytes(file_size)

    print(f"Arquivo escrito com sucesso em: {output_path}")
    print(f"Tamanho final:  {human_file_size}")
    print(f"Tempo decorrido: {format_elapsed_time(elapsed_time)}")


def verificar_e_deletar_arquivo_expirado(measurements_path="./data/measurements.txt"):
    expiry_file = "./data/.measurements_expiry"

    if os.path.exists(expiry_file):
        with open(expiry_file, 'r') as f:
            expiry_timestamp = float(f.read().strip())

        if time.time() >= expiry_timestamp:
            if os.path.exists(measurements_path):
                os.remove(measurements_path)
                print("Arquivo measurements.txt expirado e removido automaticamente.")
            os.remove(expiry_file)


def registrar_expiracao(measurements_path="./data/measurements.txt"):
    expiry_file = "./data/.measurements_expiry"
    expiry_timestamp = time.time() + 86400  # 24 horas em segundos

    with open(expiry_file, 'w') as f:
        f.write(str(expiry_timestamp))

    print("\nAVISO: Este arquivo sera deletado automaticamente em 24 horas.")
    print(
        f"       Remocao agendada para: {time.strftime('%d/%m/%Y %H:%M', time.localtime(expiry_timestamp))}\n")


def criar_arquivo_temporario():
    tmp = tempfile.NamedTemporaryFile(
        suffix='.txt', delete=False, encoding='utf-8', mode='w'
    )
    path = tmp.name
    tmp.close()

    print(f"\nAVISO: arquivo temporario criado em: {path}")
    print("       Sera apagado automaticamente ao final.\n")

    def cleanup():
        if os.path.exists(path):
            os.remove(path)
            print(f"\nArquivo temporario removido: {path}")

    atexit.register(cleanup)
    return path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--temp',
        action='store_true',
        help='Cria arquivo temporario apagado automaticamente ao final'
    )
    args = parser.parse_args()

    verificar_e_deletar_arquivo_expirado()

    output_path = criar_arquivo_temporario() if args.temp else "./data/measurements.txt"

    num_rows_to_create = 1_000_000
    weather_station_names = build_weather_station_name_list()
    print(estimate_file_size(weather_station_names, num_rows_to_create))
    build_test_data(weather_station_names, num_rows_to_create, output_path)

    if not args.temp:
        registrar_expiracao(output_path)
    print("Arquivo de teste finalizado.")


if __name__ == "__main__":
    main()
exit()
