import cv2
import os

# Cria a pasta "files" se não existir
if not os.path.exists("files"):
    os.makedirs("files")

# Lê a imagem original
imagem = cv2.imread("imagem_original.jpg")

if imagem is None:
    print("Erro: imagem não encontrada! Verifique se o nome está correto.")
    exit()

# Mostra a imagem e permite selecionar o retângulo
r = cv2.selectROI("Selecione o retângulo com o mouse", imagem)
x, y, w, h = r
cv2.destroyAllWindows()

# Recorta a parte selecionada
recorte = imagem[int(y):int(y+h), int(x):int(x+w)]

# Pede ao usuário o valor do pH
ph = input("Digite o valor do PH (ex: 7): ")

# Gera o número do arquivo (ex: retang1, retang2...)
arquivos = os.listdir("files")
indice = len([arq for arq in arquivos if arq.endswith(".jpg")]) + 1

# Define os nomes dos arquivos
nome_imagem = f"files/retang{indice}.jpg"
nome_txt = f"files/retang{indice}.txt"

# Salva a imagem e o txt
cv2.imwrite(nome_imagem, recorte)
with open(nome_txt, "w") as f:
    f.write(f"PH:{ph}")

print(f"Imagem salva como {nome_imagem}")
print(f"Arquivo de anotação salvo como {nome_txt}")