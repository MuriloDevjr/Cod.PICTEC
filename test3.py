import cv2
import numpy as np
import os
from collections import Counter
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000

# 🔧 Patch para compatibilidade (NumPy 2.x não tem mais asscalar)
if not hasattr(np, "asscalar"):
    np.asscalar = lambda x: x.item()

def comparar_cores(rgb1, rgb2):
    """Compara duas cores RGB e retorna a similaridade (%) e a diferença DeltaE."""
    cor1 = sRGBColor(rgb1[0], rgb1[1], rgb1[2], is_upscaled=True)
    cor2 = sRGBColor(rgb2[0], rgb2[1], rgb2[2], is_upscaled=True)

    cor1_lab = convert_color(cor1, LabColor)
    cor2_lab = convert_color(cor2, LabColor)

    diferenca = delta_e_cie2000(cor1_lab, cor2_lab)
    similaridade = max(0, 100 - diferenca * 2)  
    return round(similaridade, 2), round(float(diferenca), 2)

def cor_mais_frequente(imagem, reduzir=10):
    """Reduz a imagem e encontra a cor mais frequente."""
    img_rgb = cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB)
    img_rgb = cv2.resize(img_rgb, (img_rgb.shape[1] // reduzir, img_rgb.shape[0] // reduzir))
    pixels = img_rgb.reshape(-1, 3)
    contador = Counter(tuple(int(p) for p in px) for px in pixels)
    cor = contador.most_common(1)[0][0]
    return cor  # (R, G, B)

def capturar_com_roi():
    """Abre a câmera e permite selecionar uma ROI."""
    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        print("Erro: não consegui acessar a câmera.")
        return None

    while True:
        ret, frame = cam.read()
        if not ret:
            print("Erro ao capturar frame.")
            break

        cv2.imshow("Pressione ENTER para capturar", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == 13:  # ENTER
            cv2.destroyAllWindows()
            break

    cam.release()

    r = cv2.selectROI("Selecione a região e pressione ENTER", frame, fromCenter=False)
    cv2.destroyAllWindows()
    x, y, w, h = r
    if w == 0 or h == 0:
        print("Nenhuma região selecionada.")
        return None

    return frame[y:y+h, x:x+w]

def cadastrar():
    # Abre a camera
    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        print("Erro: não consegui acessar a câmera.")
        return None
    
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
  
            # Obter pH
            ph = input("Digite o valor do pH (ou pressione ENTER para encerrar): ")
            if not ph.strip():
                print("Encerrando coleta.")
                break

            nomeRef = os.path.join(pasta_ref, f"{ph}.jpg")
            cv2.imwrite(nomeRef, recorteRef)
            cv2.destroyAllWindows()
            break
        
    cor_cad = cor_mais_frequente(recorteRef)

    print(type(cor_cad))

# ---------------- MAIN ----------------
while True:
    print("""
1- Cadastrar;
2- Analisar;

0- Sair.
    """)
    selecao = int(input())
    if (selecao == 0):
        exit()
    elif (selecao == 1):
        print('''
Selecione o tipo da analise:

- Amonia;
- PH;
- O² Dissolvido;
- Nitrito.
            ''')
        ref = input()
        ref = ref.lower()
    
        # 📂 Pasta com imagens de referência
        if (ref == "amonia" or ref == "ph" or ref == "o2 dissolvido" or ref == "nitrito"):    
            pasta_ref = ref
        else:
            print("Essa opção não existe, por favor tente novamente!")
            exit()
    
        cadastrar()
    elif (selecao == 2):
        print('''
Selecione o tipo da analise:

- Amonia;
- PH;
- O² Dissolvido;
- Nitrito.
            ''')
        ref = input()
        ref = ref.lower()

        # 📂 Pasta com imagens de referência
        if (ref == "amonia" or ref == "ph" or ref == "o2 dissolvido" or ref == "nitrito"):    
            pasta_ref = ref
        else:
            print("Essa opção não existe, por favor tente novamente!")
            exit()
        # 📸 Capturar ROI da câmera
        roi = capturar_com_roi()
        
        if roi is None:
            exit()
    
        cor_ref = cor_mais_frequente(roi)
        print(f"🎨 Cor capturada: {cor_ref}")
 
        melhor_sim = -1
        melhor_img = None
    
        # 🔍 Percorrer imagens na pasta
        for arquivo in os.listdir(pasta_ref):
            if arquivo.lower().endswith((".jpg", ".png", ".jpeg")):
                caminho = os.path.join(pasta_ref, arquivo)
                img = cv2.imread(caminho)
                if img is None:
                    continue
                
                cor_img = cor_mais_frequente(img)
                similaridade, diferenca = comparar_cores(cor_ref, cor_img)
    
                print(f"{arquivo} -> Similaridade: {similaridade}% | ΔE: {diferenca}")
    
                if similaridade > melhor_sim:
                    melhor_sim = similaridade
                    melhor_img = arquivo
    
        # Resultado final
        if melhor_img:
            print(f"\n✅ A imagem mais similar é: {melhor_img} ({melhor_sim}%)")
        else:
            print("Nenhuma imagem encontrada na pasta.")
    
    else: 
        print("Essa opção não existe, por favor tente novamente!")  