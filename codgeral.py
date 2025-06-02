import cv2
import numpy as np
from collections import Counter
import os

def cor_mais_frequente(imagem, reduzir=10):
    imagem_rgb = cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB)
    imagem_rgb = cv2.resize(imagem_rgb, (imagem_rgb.shape[1] // reduzir, imagem_rgb.shape[0] // reduzir))
    pixels = imagem_rgb.reshape(-1, 3)
    counter = Counter(tuple(pixel) for pixel in pixels)
    cor_mais_comum = counter.most_common(1)[0]  # ((R, G, B), ocorrências)
    return cor_mais_comum

# Diretório para salvar arquivos
PASTA_SAIDA = "files"
os.makedirs(PASTA_SAIDA, exist_ok=True)

# Carregar imagem original
imagem_path = "fotos/telaazul.jpg"
imagem = cv2.imread(imagem_path)

if imagem is None:
    print("Erro: imagem não encontrada! Verifique se o nome está correto.")
    exit()

indice = len([arq for arq in os.listdir(PASTA_SAIDA) if arq.endswith(".jpg")]) + 1

while True:
    # Selecionar ROI
    r = cv2.selectROI("Selecione o retângulo com o mouse (tecle ENTER para confirmar)", imagem, False, False)
    x, y, w, h = r
    cv2.destroyAllWindows()

    if w == 0 or h == 0:
        print("Seleção vazia. Encerrando.")
        break

    # Recortar região
    recorte = imagem[int(y):int(y+h), int(x):int(x+w)]

    # Obter pH
    ph = input("Digite o valor do pH (ou pressione ENTER para encerrar): ")
    if not ph.strip():
        print("Encerrando coleta.")
        break

    # Obter cor mais frequente
    cor_comum, ocorrencias = cor_mais_frequente(recorte)

    # Nomes dos arquivos
    nome_imagem = os.path.join(PASTA_SAIDA, f"retang{indice}.jpg")
    nome_txt = os.path.join(PASTA_SAIDA, f"retang{indice}.txt")

    # Salvar imagem recortada
    cv2.imwrite(nome_imagem, recorte)

    # Salvar dados no .txt
    with open(nome_txt, "w") as f:
        f.write(f"PH: {ph}\n")
        f.write(f"Cor mais comum (RGB): {cor_comum}\n")
        f.write(f"Ocorrências: {ocorrencias}\n")

    print(f"[✔] Imagem salva como: {nome_imagem}")
    print(f"[✔] Dados salvos em: {nome_txt}")

    indice += 1  # Incrementar para próxima iteração
