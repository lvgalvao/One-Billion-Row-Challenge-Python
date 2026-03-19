import duckdb
import time
import config

def create_duckdb():
    duckdb.sql(f"""
        SELECT station,
            MIN(temperature) AS min_temperature,
            CAST(AVG(temperature) AS DECIMAL(3,1)) AS mean_temperature,
            MAX(temperature) AS max_temperature
        FROM read_csv("{config.FOLDER_PATH}", AUTO_DETECT=FALSE, sep=';', columns={{'station':VARCHAR, 'temperature': 'DECIMAL(3,1)'}})
        GROUP BY station
        ORDER BY station
    """).show()

if __name__ == "__main__":
    import time
    start_time = time.time()
    create_duckdb()
    took = time.time() - start_time
    print(f"Duckdb Took: {took:.2f} sec")