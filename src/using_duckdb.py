import duckdb
import time

# Processa dados meteorólogicos de um arquivo CSV calculando estatisticasde temperatura para cada estação meteorólogica.
def create_duckdb():
    duckdb.sql("""
        SELECT station,
            MIN(temperature) AS min_temperature,
            CAST(AVG(temperature) AS DECIMAL(3,1)) AS mean_temperature,
            MAX(temperature) AS max_temperature
        FROM read_csv("data/measurements.txt", AUTO_DETECT=FALSE, sep=';', columns={'station':VARCHAR, 'temperature': 'DECIMAL(3,1)'})
        GROUP BY station
        ORDER BY station
    """).show()
    
# Executa a análise de dados meteorologicos e mede o tempo de processamento do DuckDB exibindo o resultado final.
if __name__ == "__main__":
    import time
    start_time = time.time()
    create_duckdb()
    took = time.time() - start_time
    print(f"Duckdb processing time: {took:.2f} seconds")