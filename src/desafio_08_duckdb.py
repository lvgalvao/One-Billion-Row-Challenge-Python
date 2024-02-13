import duckdb
import time

def processar_temperaturas_duckdb():
    start_time = time.time()  # Marca o início do processamento
    
    print("Iniciando o processamento do arquivo com DuckDB.")

    # Conectando-se ao banco de dados DuckDB
    print("Calculando estatísticas...")
    resultado = duckdb.sql("""
        SELECT station,
               MIN(temperature) AS min_temperature,
               AVG(temperature) AS mean_temperature,
               MAX(temperature) AS max_temperature
        FROM read_csv("data/measurements1B.txt", AUTO_DETECT=FALSE, sep=';', columns={'station':VARCHAR, 'temperature': FLOAT})
        GROUP BY station
        ORDER BY station
    """).fetchall()
    print("Estatísticas calculadas:")


    end_time = time.time()  # Marca o fim do processamento
    print(f"Processamento concluído. Tempo de execução: {end_time - start_time:.2f} segundos.")

    return resultado

if __name__ == "__main__":
    # Substitua o caminho do arquivo conforme necessário
    resultados_df = processar_temperaturas_duckdb()
    # Com duckdb Tempo de execução: 76.27 segundos.
    print(resultados_df)
