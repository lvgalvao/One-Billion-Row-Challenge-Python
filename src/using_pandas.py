import os
import pandas as pd
from multiprocessing import Pool

CHUNK_COUNT = 8
CONCURRENCY = 8

def process_chunk(args):
    filename, chunk_start, chunk_size = args
    # Pula a primeira linha se não for o início do arquivo para evitar ler uma linha incompleta
    skiprows = 1 if chunk_start > 0 else 0
    
    # Usa o Pandas para ler um chunk específico do arquivo
    chunk = pd.read_csv(filename, sep=';', header=None, names=['station', 'measure'], 
                        skiprows=skiprows, skipfooter=chunk_size, engine='python')
    
    # Agrega os dados dentro do chunk usando Pandas
    aggregated = chunk.groupby('station')['measure'].agg(['min', 'max', 'mean']).reset_index()
    
    return aggregated

def create_df_with_pandas(filename):
    size = os.path.getsize(filename)
    chunk_size = size // CHUNK_COUNT

    start_positions = [i * chunk_size for i in range(CHUNK_COUNT)]

    # Define os argumentos para cada chunk a ser processado
    chunks_args = [(filename, start, chunk_size) for start in start_positions]

    # Processa os chunks em paralelo
    with Pool(CONCURRENCY) as pool:
        results = pool.map(process_chunk, chunks_args)

    # Combina os DataFrames resultantes
    final_df = pd.concat(results, ignore_index=True)

    # Agrega novamente no caso de estações repetidas entre os chunks
    final_aggregated_df = final_df.groupby('station').agg({
        'min': 'min',
        'max': 'max',
        'mean': 'mean'  # Note que essa agregação da média pode não ser totalmente precisa
    }).reset_index().sort_values('station')
    
    return final_aggregated_df

if __name__ == "__main__":
    import time

    filename = "data/measurements.txt"  # Certifique-se de que este é o caminho correto para o arquivo

    start_time = time.time()
    df = create_df_with_pandas(filename)
    took = time.time() - start_time

    print(df.head())
    print(f"Processing took: {took:.2f} sec")
