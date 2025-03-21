import time
from multiprocessing import Pool, cpu_count
from multiprocessing.pool import ApplyResult
from pathlib import Path
from typing import Iterator, List

import pandas as pd
from tqdm import tqdm  # importa o tqdm para barra de progresso

CONCURRENCY: int = cpu_count()
frase_input = "Digite o número total de linhas processadas: "
total_linhas: int = int(input(frase_input))  # Total de linhas conhecido
chunksize: int = 100_000_000  # Define o tamanho do chunk
# Certifique-se de que este é o caminho correto para o arquivo
filename: Path = Path("data/measurements.txt")


def process_chunk(chunk: pd.DataFrame) -> pd.DataFrame:
    # Agrega os dados dentro do chunk usando Pandas
    aggregated: pd.DataFrame = (
        chunk.groupby("station")["measure"].agg(["min", "max", "mean"]).reset_index()
    )
    return aggregated


def create_df_with_pandas(
    filename: Path, total_linhas: int, chunksize: int = chunksize
):
    total_chunks: int = total_linhas // chunksize + (
        1 if total_linhas % chunksize else 0
    )
    async_results: List[ApplyResult[pd.DataFrame]] = []

    reader: Iterator[pd.DataFrame] = pd.read_csv(
        filepath_or_buffer=filename,
        sep=";",
        header=None,
        names=["station", "measure"],
        chunksize=chunksize,
    )
    # Criando um pool de processos
    with Pool(CONCURRENCY) as pool:
        # Envolvendo o iterador com tqdm para visualizar o progresso
        for chunk in tqdm(reader, total=total_chunks, desc="Processando"):
            # Processa cada chunk em paralelo
            result: ApplyResult[pd.DataFrame] = pool.apply_async(
                process_chunk, (chunk,)
            )
            async_results.append(result)

        results: List[pd.DataFrame] = [result.get() for result in async_results]

    final_df: pd.DataFrame = pd.concat(results, ignore_index=True)

    final_aggregated_df: pd.DataFrame = (
        final_df.groupby("station")
        .agg({"min": "min", "max": "max", "mean": "mean"})
        .reset_index()
        .sort_values("station")
    )

    return final_aggregated_df


if __name__ == "__main__":

    print("Iniciando o processamento do arquivo.")
    start_time: int = time.time()
    df: pd.DataFrame = create_df_with_pandas(filename, total_linhas, chunksize)
    took: int = time.time() - start_time

    print(df.head())
    print(f"Processing took: {took:.2f} sec")
