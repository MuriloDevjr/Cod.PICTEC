import cv2
import numpy as np
from collections import Counter
import os
from skimage.metrics import structural_similarity

from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from color_diff import delta_e_cie2000


def similaridade2 (cor1_rgb, cor2_rgb):
    # Defina as cores em formato RGB (valores de 0 a 255)
    #cor1_rgb = sRGBColor(255, 0, 0, is_upscaled=True)  # Vermelho
    #cor2_rgb = sRGBColor(254, 0, 0, is_upscaled=True)  # Vermelho quase igual

    # Converta para o espaço de cores Lab, que é melhor para medir diferenças perceptuais
    cor1_lab = convert_color(cor1_rgb, LabColor)
    cor2_lab = convert_color(cor2_rgb, LabColor)

    # Calcule a diferença entre as cores
    diferenca = delta_e_cie2000(cor1_lab, cor2_lab)

    simsim = max(0,100 - diferenca)
    print(f"A diferença entre as cores é: {simsim}")

def analisar():
    print("analisar")

def similaridade():
   
    #for i in range(2,20):
    img1 = recorte
    img2 = cv2.imread(f'imagemReferencia/ref{indice2}.jpg')


    cor1 = cor_mais_frequente(img1)
    print(cor1)
    cor1Final = sRGBColor(cor1[0][0], cor1[0][1], cor1[0][2], is_upscaled=True)

    cor2 = cor_mais_frequente(img2)
    cor2Final = sRGBColor(cor2[0][0], cor2[0][1], cor2[0][2], is_upscaled=True)

    similaridade2(cor1Final, cor2Final)

    
    return 0

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
  
def cor_mais_frequente(imagem, reduzir=10):
    
  
   
    #imagem_rgb = cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB)
    imagem_rgb = imagem

    imagem_rgb = cv2.resize(imagem_rgb, (imagem_rgb.shape[1] // reduzir, imagem_rgb.shape[0] // reduzir))
    
    

    pixels = imagem_rgb.reshape(-1, 3)
    counter = Counter(tuple(pixel) for pixel in pixels)
    cor_mais_comum = counter.most_common(1)[0]  # ((R, G, B), ocorrências)
    return cor_mais_comum

def cadastrar():
    while True:
        ret, frame = cam.read()
        if not ret:
            print("Erro ao ler da câmera.")
            break
        cv2.imshow("Capturar imagem referência", frame)
        key = cv2.waitKey(1) & 0xFF
        # if the 'enter' key is pressed, stop the loop
        if key == 13:
            imagemRef = frame

            r = cv2.selectROI("Selecione o retangulo com o mouse (tecle ENTER para confirmar)", imagemRef, False, False)
            x, y, w, h = r
            cv2.destroyAllWindows()

            recorteRef = frame[int(y):int(y+h), int(x):int(x+w)]

            nomeRef = os.path.join(PASTA_REFERENCIA, f"Ref{indice2}.jpg")
            cv2.imwrite(nomeRef, recorteRef)
            cv2.destroyAllWindows()

            # Obter pH
            ph = input("Digite o valor do pH (ou pressione ENTER para encerrar): ")
            if not ph.strip():
                print("Encerrando coleta.")
                break
            break
        
    cor_cad = cor_mais_frequente(recorteRef)

    print(type(cor_cad))

    # Nomes dos arquivos
    nome_txt = os.path.join(PASTA_REFERENCIA, f"ph.txt")

    # Salvar dados no .txt
    with open(nome_txt, "a") as f:
        f.write(f"PH: {ph}\n")
        f.write(f"(RGB): {cor_cad}\n")
    print(f"[✔] Dados salvos em: {nome_txt}")

# Diretório para salvar arquivos
PASTA_SAIDA = "analise.txt"
PASTA_REFERENCIA = "cadastro"
os.makedirs(PASTA_SAIDA, exist_ok=True)
os.makedirs(PASTA_REFERENCIA, exist_ok=True)

#Iniciar a câmera
cam = cv2.VideoCapture(1)
if not cam.isOpened():
    print("Erro ao acessar a câmera.") 
    exit()

indice = len([arq for arq in os.listdir(PASTA_SAIDA) if arq.endswith(".jpg")]) + 1
indice2 = len([arq for arq in os.listdir(PASTA_REFERENCIA) if arq.endswith(".jpg")]) + 1

print("""
1- Cadastrar;
2- Analisar;
0- Sair.
""")
selecao = int(input())

if (selecao == 0):
    exit()
elif (selecao == 1):
    cadastrar()
elif (selecao == 2):
    print("alisa meu pelo")
else: 
    print("ta errado ae krai")


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

similaridade()
indice += 1  # Incrementar para próxima iteração

cam.release()
cv2.destroyAllWindows()