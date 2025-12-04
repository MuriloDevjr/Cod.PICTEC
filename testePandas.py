import pandas as pd
def procurarTab(ph,buscaAmonia):
    linha =0
    coluna=0
    ct = 0
    buscaTemp = int(input("Digite o valor da temperatura: "))
    buscaAmonia = buscaAmonia.split(".")    
    amonia = buscaAmonia[0]
    print(amonia)
    if(amonia == "0,25 "):
        buscaAmonia = 0.25
    elif(amonia == "0,50 "):
        buscaAmonia = 0.50
    elif(amonia == "1,00 "):
        buscaAmonia = 1.00
    elif(amonia == "2,00 "):
        buscaAmonia = 2.00
    elif(amonia == "3,50 "):
        buscaAmonia = 3.50
    elif(amonia == "6,50 "):
        buscaAmonia = 6.50
    if(ph == "6,4" or ph == "6,2"):
            print("A amonia não é crítica!")
            exit()
    else:
        valor = pd.read_csv(f"tabelas/ph{ph}.csv")
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