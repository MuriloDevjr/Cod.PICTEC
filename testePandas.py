import pandas as pd
ph = "7,2"
valor = pd.read_csv(f"tabelas/ph{ph}.csv")
linha =0
coluna=0
ct = 0
buscaTemp = 25
buscaAmonia = 0.25
for i in valor.head():

    print(i, buscaAmonia)
    l1 = valor[i]
    linha =0
    if(buscaAmonia == float(i)):
        
        for i2 in l1:
            print(valor["0"][ct])
            if(buscaTemp == int(valor["0"][ct])):
                print("achou!")
                print(i2)
                
            linha+=1
            ct += 1
    coluna+=1
   
#v = valor.loc[valor["6.5"] == 22, "6.5"]
#v = valor.iloc[22 , 6.5].values(0)
#print(v.head())