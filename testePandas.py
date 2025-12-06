import pandas as pd
def procurarTab(ph,buscaAmonia):
    linha =0
    coluna=0
    ct = 0
    v = False
    buscaTemp = int(input("Digite o valor da temperatura: "))
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
        valor = pd.read_csv(f"tabelas/ph{ph}.csv")
    if(v == False):
        for i in valor.head():
            l1 = valor[i]
            linha =0
            if(buscaAmonia == float(i)):
                for i2 in l1:
                    if(buscaTemp == int(valor["0"][ct])):
                        print(f"Amonia Crítica: {i2}")
                    linha+=1
                    ct += 1
            coluna+=1