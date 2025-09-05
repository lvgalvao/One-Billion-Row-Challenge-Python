import os
import time
import psycopg2
from dotenv import load_dotenv
from psycopg2.extensions import connection as PgConnection
from psycopg2 import OperationalError

# (As funções create_db_connection, execute_sql, load_data_from_file, 
# e query_and_fetch continuam as mesmas do script anterior)

def create_db_connection() -> PgConnection | None:
    """Carrega as variáveis de ambiente e estabelece uma conexão com o banco de dados PostgreSQL."""
    load_dotenv()
    db_params = {
        "host": os.getenv("DB_HOST"), "port": os.getenv("DB_PORT"),
        "user": os.getenv("DB_USER"), "password": os.getenv("DB_PASSWORD"),
        "dbname": os.getenv("DB_NAME"),
    }
    try:
        conn = psycopg2.connect(**db_params)
        return conn
    except OperationalError as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

def execute_sql(conn: PgConnection, sql: str):
    """Executa uma instrução SQL que não retorna dados (CREATE, INSERT, etc.)."""
    with conn.cursor() as cur:
        cur.execute(sql)

def load_data_from_file(conn: PgConnection, file_path: str, table_name: str, separator: str = ';'):
    """Carrega dados de um arquivo para uma tabela do PostgreSQL usando o método COPY."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            with conn.cursor() as cur:
                cur.copy_from(f, table_name, sep=separator)
    except FileNotFoundError:
        print(f"ERRO: Arquivo não encontrado em '{file_path}'")
        raise
    except Exception as e:
        print(f"Ocorreu um erro durante o carregamento dos dados: {e}")
        raise

def query_and_fetch(conn: PgConnection, query: str) -> list:
    """Executa uma consulta SELECT e retorna todas as linhas encontradas."""
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

def main():
    """Função principal que orquestra a execução e o benchmark."""
    FILE_PATH = "data/measurements.txt"
    TABLE_NAME = "temperatures"
    
    CREATE_TABLE_SQL = f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        station_name VARCHAR(100),
        measurement NUMERIC(3, 1)
    );
    """
    TRUNCATE_TABLE_SQL = f"TRUNCATE TABLE {TABLE_NAME};"

    conn = None
    try:
        conn = create_db_connection()
        if conn:
            # --- BENCHMARK DE CARGA ---
            start_load_time = time.time()

            execute_sql(conn, CREATE_TABLE_SQL)
            execute_sql(conn, TRUNCATE_TABLE_SQL) # Limpa a tabela para um benchmark justo
            load_data_from_file(conn, FILE_PATH, TABLE_NAME)
            conn.commit() # Salva a carga de dados

            load_duration = time.time() - start_load_time

            # --- BENCHMARK DE PROCESSAMENTO ---
            start_process_time = time.time()
            
            # CORREÇÃO: Usando os nomes de coluna corretos (station_name, measurement)
            query_sql = f"""
            SELECT
                station_name,
                MIN(measurement) AS min_measurement,
                CAST(AVG(measurement) AS DECIMAL(3,1)) AS mean_measurement,
                MAX(measurement) AS max_measurement
            FROM {TABLE_NAME}
            GROUP BY station_name
            ORDER BY station_name;
            """
            results = query_and_fetch(conn, query_sql)
            process_duration = time.time() - start_process_time

            # --- EXIBIÇÃO DOS RESULTADOS ---
            print("\n--- Amostra do Resultado do Processamento (10 primeiras estações) ---")
            print(f"{'Estação':<30} | {'Min':>6} | {'Média':>6} | {'Máx':>6}")
            print("-" * 54)
            for row in results[:10]:
                # row[0] = station_name, row[1] = min, row[2] = avg, row[3] = max
                print(f"{row[0]:<30} | {row[1]:>6.1f} | {row[2]:>6.1f} | {row[3]:>6.1f}")
            
            # --- RESULTADOS DO BENCHMARK ---
            print("\n--- Resultados do Benchmark (PostgreSQL) ---")
            print(f"Tempo de Carga           : {load_duration:.2f} segundos")
            print(f"Tempo de Processamento   : {process_duration:.2f} segundos")
            print(f"Tempo Total              : {load_duration + process_duration:.2f} segundos")

    except Exception as e:
        print(f"\nOcorreu um erro! Revertendo a transação (rollback)...: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    main()