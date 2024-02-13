import pandas as pd
import time

def processar_temperaturas_pandas(path_do_txt, chunk_size=1000000):
    start_time = time.time()  # Inicia a contagem de tempo
    
    print("Iniciando o processamento do arquivo TXT sem cabeçalho com Pandas e chunks.")
    # Preparando um DataFrame vazio para acumular os resultados
    acumulador_df = pd.DataFrame()

    for chunk in pd.read_csv(path_do_txt, delimiter=';', header=None, names=['station', 'temperature'], chunksize=chunk_size):
        # Agregando as temperaturas por estação dentro do chunk
        agregado = chunk.groupby('station')['temperature'].agg(['min', 'mean', 'max']).reset_index()
        # Acumulando os resultados
        acumulador_df = pd.concat([acumulador_df, agregado])

    # Agregando novamente no caso de estações duplicadas entre chunks
    resultado_final = acumulador_df.groupby('station').agg({'min': 'min', 'mean': 'mean', 'max': 'max'}).reset_index()
    
    # Ordenando os resultados pelo nome da estação
    resultado_final.sort_values(by='station', inplace=True)

    end_time = time.time()  # Encerra a contagem de tempo
    print(f"Processamento concluído. Tempo de execução: {end_time - start_time:.2f} segundos.")
    
    return resultado_final

if __name__ == "__main__":
    # Substitua o caminho do arquivo conforme necessário
    path_do_txt = "data/measurements100M.txt"
    # Tempo de execução 100M: 16.38 segundos.
    resultados_df = processar_temperaturas_pandas(path_do_txt)
    print(resultados_df)
