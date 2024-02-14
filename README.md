# Um do Bilhão de Linhas

Como ler um arquivo de 1 bilhão de linhas (~14GB) , realizar um GROUP BY e um ORDER BY utilizando Python?

Esse código é uma implementação do [The One Billion Row Challenge:](https://github.com/gunnarmorling/1brc) realizado para Java

O arquivo em questão contém valores de temperatura para uma variedade de estações meteorológicas.

Cada linha é uma medição no formato <string: nome da estação>;<double: medição>, com o valor da medição tendo exatamente uma casa decimal.

A seguir, dez linhas como exemplo:

```json
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

A tarefa é escrever um programa que leia o arquivo, calcule o valor mínimo, médio e máximo da temperatura por estação meteorológica e emita os resultados arredondados para uma casa decimal:

| station      | min_temperature | mean_temperature | max_temperature |
|--------------|-----------------|------------------|-----------------|
| Abha         | -31.1           | 18.0             | 66.5            |
| Abidjan      | -25.9           | 26.0             | 74.6            |
| Abéché       | -19.8           | 29.4             | 79.9            |
| Accra        | -24.8           | 26.4             | 76.3            |
| Addis Ababa  | -31.8           | 16.0             | 63.9            |
| Adelaide     | -31.8           | 17.3             | 71.5            |
| Aden         | -19.6           | 29.1             | 78.3            |
| Ahvaz        | -24.0           | 25.4             | 72.6            |
| Albuquerque  | -35.0           | 14.0             | 61.9            |
| Alexandra    | -40.1           | 11.0             | 67.9            |
| ...          | ...             | ...              | ...             |
| Yangon       | -23.6           | 27.5             | 77.3            |
| Yaoundé      | -26.2           | 23.8             | 73.4            |
| Yellowknife  | -53.4           | -4.3             | 46.7            |
| Yerevan      | -38.6           | 12.4             | 62.8            |
| Yinchuan     | -45.2           | 9.0              | 56.9            |
| Zagreb       | -39.2           | 10.7             | 58.1            |
| Zanzibar City| -26.5           | 26.0             | 75.2            |
| Zürich       | -42.0           | 9.3              | 63.6            |
| Ürümqi       | -42.1           | 7.4              | 56.7            |
| İzmir        | -34.4           | 17.9             | 67.9            |

Meu objetivo com esse desafio era testar como o Python se comportaria utilizando de forma nativa, com Pandas, Polars e Duckdb.

## Resultado
Rodando no meu laptop, equipado com M1 (8 núcleos) da Apple e 8 GB RAM

Obs: O dataset em questão é maior do que minha memória, o que faz o

| Implementação      | Tempo |
|--------------|-------------|
Python	| Não rodou
Python + Pandas	| Não rodou
Python + Polars |	33.86 sec
Python + Duckdb	| 14.98 sec