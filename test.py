print("""
1- Cadastrar;
2- Analisar;
0- Sair.
""")
selecao = int(input())
try:
    if (selecao == 0):
        exit()
    elif (selecao == 1):
        cadastrar()
    elif (selecao == 2):
        print("alisa meu pelo")
except ValueError: 
    print("ta errado ae krai")