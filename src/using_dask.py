import dask
import dask.dataframe as dd

def create_dask_df():
    dask.config.set({'dataframe.query-planning': True})
    # Configurando o Dask DataFrame para ler o arquivo CSV
    # Como o arquivo não tem cabeçalho, especificamos os nomes das colunas manualmente
    df = dd.read_csv("data/measurements.txt", sep=";", header=None, names=["station", "measure"])
    
    # Agrupando por 'station' e calculando o máximo, mínimo e média de 'measure'
    # O Dask realiza operações de forma lazy, então esta parte apenas define o cálculo
    grouped_df = df.groupby("station")['measure'].agg(['max', 'min', 'mean']).reset_index()

    # O Dask não suporta a ordenação direta de DataFrames agrupados/resultantes de forma eficiente
    # Mas você pode computar o resultado e então ordená-lo se o dataset resultante não for muito grande
    # ou se for essencial para a próxima etapa do processamento
    # A ordenação será realizada após a chamada de .compute(), se necessário

    return grouped_df

if __name__ == "__main__":
    import time

    start_time = time.time()
    df = create_dask_df()
    
    # O cálculo real e a ordenação são feitos aqui
    result_df = df.compute().sort_values("station")
    took = time.time() - start_time

    print(result_df)
    print(f"Dask Took: {took:.2f} sec")
