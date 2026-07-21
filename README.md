# Um Bilhão de Linhas: Desafio de Processamento de Dados com Python

## Introdução

O objetivo deste projeto é demonstrar como processar eficientemente um arquivo de dados massivo contendo 1 bilhão de linhas (~14GB), realizando operações de agregação e ordenação utilizando diferentes abordagens do ecossistema Python.

Este desafio foi inspirado no [The One Billion Row Challenge](https://github.com/gunnarmorling/1brc), originalmente proposto para Java.

O projeto foi desenvolvido durante meus estudos na **Jornada de Dados**, com o objetivo de aprimorar habilidades em Python, processamento de dados e ferramentas utilizadas na Engenharia de Dados.

O arquivo de dados consiste em medições de temperatura de várias estações meteorológicas.

Cada registro segue o formato:

```text
<string: nome da estação>;<double: medição>
```

A temperatura é apresentada com precisão de uma casa decimal.

Exemplo:

```text
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

O desafio consiste em desenvolver soluções capazes de ler esse arquivo e calcular:

- temperatura mínima;
- temperatura média (arredondada para uma casa decimal);
- temperatura máxima;

para cada estação meteorológica, exibindo os resultados ordenados pelo nome da estação.

Exemplo de saída:

| station | min_temperature | mean_temperature | max_temperature |
| --- | --- | --- | --- |
| Abha | -31.1 | 18.0 | 66.5 |
| Abidjan | -25.9 | 26.0 | 74.6 |
| Abéché | -19.8 | 29.4 | 79.9 |
| Accra | -24.8 | 26.4 | 76.3 |
| Addis Ababa | -31.8 | 16.0 | 63.9 |
| ... | ... | ... | ... |
| Zürich | -42.0 | 9.3 | 63.6 |

---

# Implementações

Inicialmente o desafio foi desenvolvido utilizando Python puro.

Posteriormente foram implementadas novas soluções para comparar diferentes estratégias de processamento e entender o comportamento de cada ferramenta.

| Implementação | Descrição |
| --- | --- |
| Python puro | Processamento utilizando estruturas nativas da linguagem |
| Pandas | Processamento utilizando DataFrames e leitura em chunks |
| Dask | Processamento paralelo utilizando DataFrames distribuídos |
| Polars | Processamento otimizado utilizando execução lazy |
| DuckDB | Processamento analítico utilizando SQL diretamente sobre os dados |
| PySpark | Processamento utilizando Apache Spark |

---

# Melhorias Implementadas

Durante a evolução do projeto foram realizadas melhorias além da implementação inicial do desafio.

## Otimização da implementação Python

A implementação utilizando Python puro foi revisada para melhorar a etapa de processamento e agregação dos dados.

Foram otimizados os cálculos de:

- temperatura mínima;
- temperatura máxima;
- soma das medições;
- quantidade de registros.

O objetivo foi reduzir operações desnecessárias e melhorar a eficiência do processamento.

---

## Otimização da implementação Dask

A implementação utilizando Dask recebeu melhorias na etapa de agregação.

Foram revisadas as operações de:

- agrupamento dos dados;
- cálculo das métricas;
- processamento paralelo.

O objetivo foi obter uma execução mais eficiente utilizando o modelo distribuído do Dask.

---

## Implementação utilizando PySpark

Foi adicionada uma nova solução utilizando PySpark para comparar uma ferramenta amplamente utilizada em ambientes profissionais de Engenharia de Dados.

A implementação utiliza:

- leitura estruturada dos dados;
- definição de schema;
- operações de agregação;
- agrupamento por estação meteorológica.

---

## Criação de Benchmark

Foi desenvolvido um script para executar todas as implementações automaticamente e comparar os tempos de execução.

Executar:

```bash
python src/benchmark.py
```

O benchmark compara:

- Python;
- Pandas;
- Dask;
- Polars;
- DuckDB;
- Spark.

---

## Correções e melhorias de compatibilidade

Foram realizadas melhorias para facilitar a execução do projeto em diferentes ambientes:

- ajustes relacionados ao encoding de saída no terminal;
- compatibilidade com Windows;
- organização das dependências utilizando Poetry;
- controle da versão do Python utilizando pyenv.

---

# Dependências

Para executar os scripts deste projeto, são utilizadas as seguintes bibliotecas:

- Pandas
- Dask
- Polars
- DuckDB
- PySpark

As versões utilizadas estão definidas no arquivo:

```text
pyproject.toml
```

---

# Resultados

Os testes foram realizados localmente utilizando:

- Python 3.12
- Ambiente gerenciado com Poetry

Os resultados podem variar conforme hardware utilizado. O objetivo do benchmark é comparar as diferentes estratégias utilizadas para resolver o mesmo problema.

| Implementação | Tempo |
| --- | --- |
| DuckDB | 1.26s |
| Polars | 1.71s |
| Dask | 4.86s |
| Pandas | 5.82s |
| Python puro | 12.07s |
| Spark | 17.28s |

---

# Conclusão

Este desafio demonstrou como diferentes ferramentas possuem características próprias para processamento de grandes volumes de dados.

A implementação utilizando Python puro permitiu compreender os fundamentos do processamento linha a linha, enquanto ferramentas como Pandas, Dask, Polars, DuckDB e Spark apresentaram diferentes estratégias para otimização e escalabilidade.

Nos testes realizados, o DuckDB apresentou o menor tempo de execução, destacando sua eficiência em operações analíticas.

Entretanto, a escolha da tecnologia depende do cenário:

- **DuckDB e Polars** apresentam excelente desempenho para análises locais;
- **Dask** permite processamento paralelo utilizando Python;
- **Spark** é indicado para cenários distribuídos e grandes arquiteturas de dados.

O principal aprendizado deste projeto foi compreender as diferenças entre cada abordagem e entender quando utilizar cada tecnologia dentro de um contexto de Engenharia de Dados.

---

# Como Executar

## Configuração do ambiente

Definir a versão do Python:

```bash
pyenv local 3.12.1
```

Criar ambiente e instalar dependências:

```bash
poetry env use 3.12.1

poetry install
```

---

## Gerar arquivo de dados

Executar:

```bash
python src/create_measurements.py
```

Será criado o arquivo:

```text
data/measurements.txt
```

---

## Executar as implementações

Python:

```bash
python src/using_python.py
```

Pandas:

```bash
python src/using_pandas.py
```

Dask:

```bash
python src/using_dask.py
```

Polars:

```bash
python src/using_polars.py
```

DuckDB:

```bash
python src/using_duckdb.py
```

Spark:

```bash
python src/using_spark.py
```

---

## Executar benchmark

Para comparar automaticamente todas as soluções:

```bash
python src/benchmark.py
```

---

# Próximos passos

Este projeto faz parte da minha jornada de aprendizado em Engenharia de Dados.

Durante seu desenvolvimento foram praticados:

- Python;
- processamento de grandes volumes de dados;
- otimização de código;
- análise de performance;
- bibliotecas do ecossistema de dados.

O objetivo é continuar evoluindo as implementações e aplicar esses conhecimentos em projetos cada vez mais próximos de cenários reais de Engenharia de Dados.