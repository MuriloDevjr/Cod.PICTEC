<<<<<<< HEAD
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
=======
import pandas as pd
def procurarTab(ph,buscaAmonia, temp):
    linha = 0
    coluna = 0
    ct = 0
    v = False
    buscaTemp = temp
    buscaAmonia = buscaAmonia.split(".")    
    amonia = buscaAmonia[0]
    if(amonia == "0,25"):
        buscaAmonia = float(0.25)
    elif(amonia == "0,50"):
        buscaAmonia = float(0.50)
    elif(amonia == "1,00"):
        buscaAmonia = float(1.00)
    elif(amonia == "2,00"):
        buscaAmonia = float(2.00)
    elif(amonia == "3,50"):
        buscaAmonia = float(3.50)
    elif(amonia == "6,50"):
        buscaAmonia = float(6.50)
    if(ph == "6,4" or ph == "6,2"):
            print("A amonia não é crítica!")
            v = True
    else:
        valor = pd.read_csv(f"src/tabelas/ph{ph}.csv")
    if(v == False):
        for i in valor.head():
            l1 = valor[i]
            linha =0
            if(buscaAmonia == float(i)):
                for i2 in l1:
                    if(buscaTemp == int(valor["0"][ct])):
                        print(f"Amonia Crítica: {i2}")
                        return i2
                    linha+=1
                    ct += 1
            coluna+=1
>>>>>>> 2d5a45decaaa3638239b01d7b6ea74e8ae7a85cd
