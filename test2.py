import cv2
import numpy as np
from collections import Counter
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000

# 🔧 Patch para NumPy (compatibilidade com colormath)
if not hasattr(np, "asscalar"):
    np.asscalar = lambda x: x.item()

def comparar_cores(rgb1, rgb2):
    """Compara duas cores RGB e retorna a similaridade em % e a diferença DeltaE."""
    cor1 = sRGBColor(rgb1[0], rgb1[1], rgb1[2], is_upscaled=True)
    cor2 = sRGBColor(rgb2[0], rgb2[1], rgb2[2], is_upscaled=True)

    cor1_lab = convert_color(cor1, LabColor)
    cor2_lab = convert_color(cor2, LabColor)

    diferenca = delta_e_cie2000(cor1_lab, cor2_lab)
    similaridade = max(0, 100 - diferenca * 2)  
    return round(similaridade, 2), round(float(diferenca), 2)

def cor_mais_frequente(imagem, reduzir=10):
    """Reduz a imagem e encontra a cor mais frequente. Retorna (R,G,B) como int normal."""
    img_rgb = cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB)
    img_rgb = cv2.resize(img_rgb, (img_rgb.shape[1] // reduzir, img_rgb.shape[0] // reduzir))

    pixels = img_rgb.reshape(-1, 3)
    contador = Counter(tuple(int(p) for p in px) for px in pixels)  # 🔹 converte direto pra int
    cor = contador.most_common(1)[0][0]
    return cor  # já vem em (R,G,B) inteiro

def capturar_com_roi(mensagem="Selecione uma região e pressione ENTER"):
    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        print("Erro: não consegui acessar a câmera.")
        return None

    while True:
        ret, frame = cam.read()
        if not ret:
            print("Erro ao capturar frame.")
            break

        cv2.imshow(mensagem, frame)
        key = cv2.waitKey(1) & 0xFF
        if key == 13:  # ENTER para congelar
            cv2.destroyAllWindows()
            break

    cam.release()

    # Selecionar região (ROI)
    r = cv2.selectROI("Selecione a região e pressione ENTER", frame, showCrosshair=True, fromCenter=False)
    cv2.destroyAllWindows()
    x, y, w, h = r
    if w == 0 or h == 0:
        print("Nenhuma região selecionada.")
        return None

    recorte = frame[y:y+h, x:x+w]
    return recorte

# ----------------- MAIN -------------------
print("📸 Capture a primeira imagem e selecione a região")
roi1 = capturar_com_roi("Primeira imagem (ENTER para capturar)")
if roi1 is None: exit()

print("📸 Capture a segunda imagem e selecione a região")
roi2 = capturar_com_roi("Segunda imagem (ENTER para capturar)")
if roi2 is None: exit()

# Pegar cor dominante das regiões
cor1 = cor_mais_frequente(roi1)
cor2 = cor_mais_frequente(roi2)

print(f"🎨 Cor 1: {cor1}")
print(f"🎨 Cor 2: {cor2}")

# Comparar
similaridade, diferenca = comparar_cores(cor1, cor2)
print(f"🔹 Similaridade: {similaridade}%")
print(f"🔹 DeltaE: {diferenca}")
