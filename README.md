# O Desafio do Bilhão de Linhas

O Desafio do Bilhão de Linhas é uma exploração para avaliar como agregar um bilhão de linhas de um arquivo de texto.

O arquivo de texto contém valores de temperatura para uma variedade de estações meteorológicas.
Cada linha é uma medição no formato <string: nome da estação>;<double: medição>, com o valor da medição tendo exatamente uma casa decimal.
A seguir, dez linhas como exemplo:

```json
Hamburg;12.0
Bulawayo;8.9
Palembang;38.8
St. John's;15.2
Cracow;12.6
Bridgetown;26.9
Istanbul;6.2
Roseau;34.4
Conakry;31.2
Istanbul;23.0
```

A tarefa é escrever um programa que leia o arquivo, calcule o valor mínimo, médio e máximo da temperatura por estação meteorológica e emita os resultados no stdout assim
(ou seja, ordenado alfabeticamente pelo nome da estação, e os valores resultantes por estação no formato <min>/<mean>/<max>, arredondados para uma casa decimal):

```json
{Abha=-23.0/18.0/59.2, Abidjan=-16.2/26.0/67.3, Abéché=-10.0/29.4/69.0, Accra=-10.1/26.4/66.4, Addis Ababa=-23.7/16.0/67.0, Adelaide=-27.8/17.3/58.5, ...}
```