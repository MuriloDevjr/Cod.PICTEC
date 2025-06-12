import cv2
import numpy as np
from collections import Counter
import os

def cor_mais_frequente(imagem_path, reduzir=10):
    imagem = cv2.imread(imagem_path)
    
    if imagem is None:
        raise FileNotFoundError(f"Erro ao carregar a imagem: {imagem_path}")
    
    imagem_rgb = cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB)
    imagem_rgb = cv2.resize(imagem_rgb, (imagem_rgb.shape[1] // reduzir, imagem_rgb.shape[0] // reduzir))
    
    pixels = imagem_rgb.reshape(-1, 3)
    counter = Counter(tuple(pixel) for pixel in pixels)
    cor_mais_comum = counter.most_common(1)[0]  # ((R, G, B), ocorrencias)
    
    return cor_mais_comum

def salvar_em_txt(rgb, ocorrencias, caminho_pasta='RGC_calibration', nome_arquivo='RGB.txt'):
    # Cria a pasta se ela não existir
    os.makedirs(caminho_pasta, exist_ok=True)

    caminho_completo = os.path.join(caminho_pasta, nome_arquivo)
    
    with open(caminho_completo, 'w') as f:
        f.write(f"Cor mais comum (RGB): {rgb}\n")
        f.write(f"Ocorrências: {ocorrencias}\n")
    
    print(f"Informações salvas em: {caminho_completo}")

# Caminho da imagem
imagem_path = "fotos/telaazul.jpg"

# Obter cor mais comum
cor_comum = cor_mais_frequente(imagem_path)

# Salvar em arquivo .txt
salvar_em_txt(cor_comum[0], cor_comum[1])
