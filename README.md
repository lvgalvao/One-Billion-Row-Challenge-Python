# Um Bilhão de Linhas: Desafio de Processamento de Dados com Python

## Introdução

O objetivo deste projeto é demonstrar como processar eficientemente um arquivo de dados massivo contendo 1 bilhão de linhas (~14GB), especificamente para calcular estatísticas (Incluindo agregação e ordenação que são operações pesadas) utilizando Python. 

Este desafio foi inspirado no [The One Billion Row Challenge](https://github.com/gunnarmorling/1brc), originalmente proposto para Java.

O arquivo de dados consiste em medições de temperatura de várias estações meteorológicas. Cada registro segue o formato `<string: nome da estação>;<double: medição>`, com a temperatura sendo apresentada com precisão de uma casa decimal.

Aqui estão dez linhas de exemplo do arquivo:

```
Hamburg;12.0
Bulawayo;8.9
Palembang;38.8
St. Johns;15.2
Cracow;12.6
Bridgetown;26.9
Istanbul;6.2
Roseau;34.4
Conakry;31.2
Istanbul;23.0
```

O desafio é desenvolver um programa Python capaz de ler esse arquivo e calcular a temperatura mínima, média (arredondada para uma casa decimal) e máxima para cada estação, exibindo os resultados em uma tabela ordenada por nome da estação.

## Dependências

Para executar os scripts deste projeto, você precisará das seguintes bibliotecas:

* Polars: `0.20.3`
* DuckDB: `0.10.0`

## Resultados

Os testes foram realizados em um laptop equipado com um processador M1 da Apple e 8GB de RAM. As implementações utilizaram abordagens puramente Python, Pandas, Polars e DuckDB. Os resultados de tempo de execução para processar o arquivo de 1 bilhão de linhas são apresentados abaixo:

| Implementação | Tempo |
| --- | --- |
| Python | Não rodou |
| Python + Pandas | Não rodou |
| Python + Polars | 33.86 sec |
| Python + Duckdb | 14.98 sec |

Obrigado por [Koen Vossen](https://github.com/koenvo) pela implementação em Polars

## Conclusão

Este desafio ilustrou claramente a capacidade de diferentes bibliotecas Python em lidar com grandes conjuntos de dados. Enquanto métodos convencionais como Python puro e Pandas não conseguiram processar o arquivo devido a limitações de memória ou desempenho, Polars e DuckDB mostraram-se excepcionalmente eficientes. O DuckDB se destacou, oferecendo o menor tempo de execução, graças à sua otimização para operações de banco de dados em grandes volumes de dados.

Esses resultados enfatizam a importância de selecionar a ferramenta adequada para análise de dados em larga escala, demonstrando que Python, com as bibliotecas certas, é uma escolha poderosa para enfrentar desafios de big data.

## Como Executar

Para executar este projeto e reproduzir os resultados:

1. Clone esse repositório
2. Execute o comando `python src/create_measurements.py` para gerar o arquivo de teste
3. Tenha paciência e vá fazer um café, vai demorar uns 10 minutos para gerar o arquivo
4. Certifique-se de instalar as versões especificadas das bibliotecas Polars e DuckDB
5. Execute os scripts `python src/using_polars.py` e `python src/using_duckdb.py` através de um terminal ou ambiente de desenvolvimento que suporte Python.

Este projeto destaca a versatilidade do ecossistema Python para tarefas de processamento de dados, oferecendo valiosas lições sobre escolha de ferramentas para análises em grande escala.

## Próximos passos

Esse projeto faz parte da *Jornada de Dados*
Nossa missão é fornecer o melhor ensino em engenharia de dados

Se você quer:

- Aprender sobre Duckdb e engenharia de dados
- Construir uma base sólida em Python e SQL
- Criar ou melhorar seu portfólio de dados
- Criar ou aumentar o seu networking na área
- Mudar ou dar o próximo passo em sua carreira

A Jornada de Dados é o seu lugar

![https://github.com/lvgalvao/data-engineering-roadmap/raw/main/pics/jornada.png](https://www.jornadadedados2024.com.br/workshops)

Para entrar na lista de espera clique no botao

![https://raw.githubusercontent.com/lvgalvao/data-engineering-roadmap/main/pics/lista_de_espera.png](https://forms.gle/hJMtRDP3MPBUGvwS7?orbt_src=orbt-vst-1RWyYmpICDu9gPknLgaD)