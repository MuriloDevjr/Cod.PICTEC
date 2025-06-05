import cv2
import numpy as np
from collections import Counter

def cor_mais_frequente(imagem_path):
    
    imagem = cv2.imread(imagem_path)
    
   
    if imagem is None:
        print("Erro ao carregar a imagem!")
        return
    
   
    imagem_rgb = cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB)


    imagem_rgb = cv2.resize(imagem_rgb, (imagem_rgb.shape[1] // 10, imagem_rgb.shape[0] // 10))

 
    pixels = imagem_rgb.reshape(-1, 3)
    
  
    counter = Counter(tuple(pixel) for pixel in pixels)
    
  
    cor_mais_comum = counter.most_common(1)[0]
    
    return cor_mais_comum


imagem_path = "fotos/arcoiris.jpg" 
cor_comum = cor_mais_frequente(imagem_path)

print(f'A cor mais comum é {cor_comum[0]} com {cor_comum[1]} ocorrências.')