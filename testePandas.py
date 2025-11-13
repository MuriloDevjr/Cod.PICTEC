import pandas as pd
valor = pd.read_csv("tabelas/ph6,6.csv")
coluna = valor["temp"]
print(coluna.head())