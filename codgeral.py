import cv2
import numpy as np
from collections import Counter
import os
from skimage.metrics import structural_similarity

def similaridade(img1,img2):
   
    #for i in range(2,20):
    img1 = recorte
    img2 = cv2.imread('amarelo.png')

    imagem1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
    
    #imagem1 = cv2.resize(imagem1, (imagem1.shape[1] // i, imagem1.shape[0] // i))

    imagem2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
    
    #    imagem2 = cv2.resize(imagem2, (imagem2.shape[1] // i, imagem2.shape[0] // i))
    
    c1 = imagem1[1:10,1:10]
    c2 = imagem2[1:10,1:10]
    cv2.imwrite('img1.png', c1)
    cv2.imwrite('img2.png', c2)

    (score) = structural_similarity(c1, c2,  win_size=7, channel_axis=-1)
    print("Image Similarity: {:.4f}%".format(score * 100))
     
    return score
  

def cor_mais_frequente(imagem, reduzir=1):
    
    img_calib = cv2.imread('amarelo.png')
    
    similaridade(img_calib,reduzir)
   
    imagem_rgb = cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB)
    
    imagem_rgb = cv2.resize(imagem_rgb, (imagem_rgb.shape[1] // reduzir, imagem_rgb.shape[0] // reduzir))
    
    

    pixels = imagem_rgb.reshape(-1, 3)
    counter = Counter(tuple(pixel) for pixel in pixels)
    cor_mais_comum = counter.most_common(1)[0]  # ((R, G, B), ocorrências)
    return cor_mais_comum

# Diretório para salvar arquivos
PASTA_SAIDA = "files"
os.makedirs(PASTA_SAIDA, exist_ok=True)

#Iniciar a câmera
cam = cv2.VideoCapture(0)
if not cam.isOpened():
    print("Erro ao acessar a câmera.")
    exit()

indice = len([arq for arq in os.listdir(PASTA_SAIDA) if arq.endswith(".jpg")]) + 1

while True:
    while True:
        ret, frame = cam.read()
        if not ret:
            print("Erro ao ler da câmera.")
            break
        cv2.imshow("Capturar imagem", frame)
        key = cv2.waitKey(1) & 0xFF
        # if the 'enter' key is pressed, stop the loop
        if key == 13:
            imagem = frame
            cv2.destroyAllWindows()
            break
        
    # Selecionar ROI
    r = cv2.selectROI("Selecione o retangulo com o mouse (tecle ENTER para confirmar)", frame, False, False)
    x, y, w, h = r
    cv2.destroyAllWindows()

    recorte = frame[int(y):int(y+h), int(x):int(x+w)]

    if w == 0 or h == 0:
        print("Seleção vazia. Encerrando.")
        break

    # Obter pH
    ph = input("Digite o valor do pH (ou pressione ENTER para encerrar): ")
    if not ph.strip():
        print("Encerrando coleta.")
        break
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

cam.release()
cv2.destroyAllWindows()