import pandas as pd
nh3V = 6.5
valor = pd.read_csv("valor.csv")
amonia = valor.loc[valor["6.5"], "ph"]
print(amonia)