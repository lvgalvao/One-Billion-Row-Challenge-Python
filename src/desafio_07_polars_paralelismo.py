import polars as pl
import time

def processar_temperaturas_polars(path_do_txt):
    start_time = time.time()  # Marca o início do processamento

    print("Iniciando o processamento do arquivo com Polars (modo lazy).")

    # Definindo o esquema: nomes das colunas e tipos de dados
    schema ={
            "station": pl.Utf8,
            "temperature": pl.Float32,
        }

    # Lendo o arquivo em modo lazy com o esquema definido e aumentando o chunk size
    lazy_df = pl.scan_csv(
        path_do_txt, 
        has_header=False, 
        separator=';',  # Use delimiter ao invés de separator
        schema=schema,
    )

    # Calculando as estatísticas mínima, média e máxima por estação em paralelo
    resultado = (
        lazy_df
        .group_by("station")
        .agg([
            pl.col("temperature").min().alias("min_temperature"),
            pl.col("temperature").mean().alias("mean_temperature"),
            pl.col("temperature").max().alias("max_temperature"),
        ])
        .sort("station")
        .collect() 
    )

    end_time = time.time()  # Marca o fim do processamento
    print(f"Processamento concluído. Tempo de execução: {end_time - start_time:.2f} segundos.")
    
    return resultado

if __name__ == "__main__":
    # Substitua o caminho do arquivo conforme necessário
    path_do_txt = "data/measurements100M.txt"
    # Nao consegui rodar com 1B
    resultados_df = processar_temperaturas_polars(path_do_txt)
    print(resultados_df)
