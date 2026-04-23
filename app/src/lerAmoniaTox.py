import pandas as pd
import os


def procurarTab(ph, buscaAmonia, temp):
    try:
        temp = int(float(str(temp).replace(",", ".")))
    except:
        return "Temperatura inválida"

 
    ph = str(ph).replace(".", ",")

 
    if ph in ["6,2", "6,4"]:
        return "Não crítica"

  
    nome_csv = f"ph{ph}.csv"

   
    caminhos = [
        os.path.join("tabelas", nome_csv),
        os.path.join("src", "tabelas", nome_csv),
    ]

    caminho = None
    for c in caminhos:
        if os.path.exists(c):
            caminho = c
            break

    if caminho is None:
        return f"Tabela {nome_csv} não encontrada"

    try:
        df = pd.read_csv(caminho, dtype=str)
    except Exception as e:
        return f"Erro CSV: {e}"


    try:
        amonia = float(buscaAmonia.split(".")[0].replace(",", "."))
    except:
        return "Erro valor amônia"

    
    col_temp = df.columns[0]

   
    for col in df.columns[1:]:
        try:
            col_val = float(col.replace(",", "."))
        except:
            continue

        if abs(col_val - amonia) < 0.0001:

          
            for _, row in df.iterrows():
                try:
                    temp_linha = int(float(str(row[col_temp]).replace(",", ".")))
                except:
                    continue

                if temp_linha == temp:
                    return str(row[col])

            return f"Temp {temp} não encontrada"

    return f"Amonia {amonia} não encontrada"
