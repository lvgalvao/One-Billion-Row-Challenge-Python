"""Processador Paralelo para o Desafio de 1 Bilhão de Linhas.

Este script foi projetado para processar de forma eficiente arquivos de texto
de grande volume (na ordem de bilhões de linhas) contendo medições de
estações meteorológicas. A tarefa consiste em calcular o valor mínimo,
médio e máximo das medições para cada estação.

Metodologia:
  1. Leitura em Chunks: O arquivo é lido em pedaços (chunks) para não
     sobrecarregar a memória RAM, permitindo o processamento de arquivos
     maiores que a memória disponível.
  2. Processamento Paralelo (Multiprocessing): Cada chunk é distribuído
     para um processo separado (worker), utilizando todos os núcleos de
     CPU disponíveis para máxima performance.
  3. Agregação em Duas Fases:
     a. Parcial: Cada worker calcula estatísticas intermediárias (min,
        max, soma, contagem) para o seu chunk.
     b. Final: O processo principal coleta os resultados parciais e
        realiza a agregação final para obter os valores globais corretos.

Otimizações Chave:
  - Cálculo Correto da Média: Utiliza 'soma' e 'contagem' para evitar o
    erro matemático da "média das médias".
  - Eficiência de Memória: Especificação de `dtypes` e uso de
    `pool.imap_unordered` para minimizar o consumo de memória de pico.
  - Performance de Leitura: O uso de `dtype='category'` para a coluna de
    estações acelera drasticamente a leitura e o processamento do arquivo.

Uso:
  - Configure as constantes `FILENAME` e `CHUNKSIZE` conforme necessário.
  - Execute o script diretamente a partir de um terminal: `python seu_script.py`

Dependências:
  - pandas
"""

import pandas as pd
from multiprocessing import Pool, cpu_count
import time
import sys
sys.stdout.reconfigure(encoding="utf-8")

# --- Constantes de Configuração ---

# Define o caminho para o arquivo de dados.
FILENAME = "data/measurements.txt"

# Define o tamanho de cada "pedaço" do arquivo a ser lido na memória.
# Ajuste este valor dependendo da memória RAM disponível.
CHUNKSIZE = 100_000_000

# Otimização: Especificar os tipos de dados acelera a leitura e economiza memória.
COLUMN_TYPES = {
    'station': 'category',
    'measure': 'float32'
}

def process_chunk(chunk: pd.DataFrame) -> pd.DataFrame:
    """Processa um único chunk de dados para agregação parcial."""
    # Agregação crucial: calculamos 'sum' e 'count' para podermos derivar a média correta posteriormente.
    # ADICIONADO `observed=True` PARA REMOVER O FUTUTREWARNING E ADOTAR O COMPORTAMENTO MAIS MODERNO E EFICIENTE.
    return chunk.groupby('station', observed=True)['measure'].agg(['min', 'max', 'sum', 'count']).reset_index()

def process_file_in_parallel(filename: str, chunksize: int) -> pd.DataFrame:
    """Orquestra a leitura e o processamento paralelo do arquivo."""
    print(f"Iniciando o processamento com {cpu_count()} processos...")

    with Pool(cpu_count()) as pool:
        with pd.read_csv(
            filename,
            sep=';',
            header=None,
            names=['station', 'measure'],
            chunksize=chunksize,
            dtype=COLUMN_TYPES
        ) as reader:
            intermediate_results = list(pool.imap_unordered(process_chunk, reader))

    print("Agrupando os resultados finais de todos os processos...")
    
    final_df = pd.concat(intermediate_results, ignore_index=True)
    
    # Na agregação final, usamos `observed=False` para garantir que
    # todas as categorias, mesmo que ausentes em alguns chunks, sejam consideradas.
    # No entanto, como concatenamos tudo antes, o comportamento é o mesmo e não gera warning.
    final_aggregated = final_df.groupby('station', observed=False).agg(
        min_measure=('min', 'min'),
        max_measure=('max', 'max'),
        total_sum=('sum', 'sum'),
        total_count=('count', 'sum')
    ).reset_index()

    final_aggregated['mean_measure'] = final_aggregated['total_sum'] / final_aggregated['total_count']
    
    result_df = final_aggregated[['station', 'min_measure', 'mean_measure', 'max_measure']]
    result_df = result_df.sort_values('station')
    
    return result_df

# --- Ponto de Entrada do Script ---
if __name__ == "__main__":
    
    print("Iniciando a execução do script...")
    start_time = time.time()
    
    final_dataframe = process_file_in_parallel(FILENAME, CHUNKSIZE)
    
    took = time.time() - start_time
    
    print("\n--- Processamento concluído! ---")
    print("Cabeçalho do resultado:")
    print(final_dataframe.head())
    print("...")
    print("Final do resultado:")
    print(final_dataframe.tail())
    print(f"\nPandas Took: {took:.2f} segundos")