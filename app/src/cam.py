import cv2
import numpy as np
import os
from collections import Counter
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000
import lerAmoniaTox as tab

valPH = None  # guarda o valor do pH detectado

# Patch compatibilidade NumPy 2.x
if not hasattr(np, "asscalar"):
    np.asscalar = lambda x: x.item()

def comparar_cores(rgb1, rgb2):
    cor1 = sRGBColor(rgb1[0], rgb1[1], rgb1[2], is_upscaled=True)
    cor2 = sRGBColor(rgb2[0], rgb2[1], rgb2[2], is_upscaled=True)
    cor1_lab = convert_color(cor1, LabColor)
    cor2_lab = convert_color(cor2, LabColor)
    diferenca = delta_e_cie2000(cor1_lab, cor2_lab)
    similaridade = max(0, 100 - diferenca * 2)
    return round(similaridade, 2), round(float(diferenca), 2)

def cor_mais_frequente(imagem, reduzir=10):
    img_rgb = cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB)
    img_rgb = cv2.resize(img_rgb, (img_rgb.shape[1] // reduzir, img_rgb.shape[0] // reduzir))
    pixels = img_rgb.reshape(-1, 3)
    contador = Counter(tuple(int(p) for p in px) for px in pixels)
    cor = contador.most_common(1)[0][0]
    return cor

def capturar_com_roi():
    """Abre a câmera, permite selecionar ROI e retorna imagem recortada."""
    numCam = 0
    while True:
        cam = cv2.VideoCapture(numCam)
        if cam.isOpened():
            break
        numCam += 1
        if numCam > 3:
            return None

    while True:
        ret, frame = cam.read()
        if not ret:
            cam.release()
            return None

        cv2.imshow("Pressione ENTER para capturar", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == 13:  # ENTER
            cv2.destroyAllWindows()
            break

    r = cv2.selectROI("Selecione a região e pressione ENTER", frame, fromCenter=False)
    cv2.destroyAllWindows()
    x, y, w, h = r
    cam.release()
    if w == 0 or h == 0:
        return None
    return frame[y:y+h, x:x+w]

def analisarTipo(tipo, temp):
    """Captura ROI e compara com referências"""
    global valPH
    roi = capturar_com_roi()
    if roi is None:
        return "Nenhuma região selecionada"

    pasta_ref = str(f"src/{tipo.lower()}")
    if not os.path.exists(pasta_ref):
        return f"Pasta de referência '{tipo}' não encontrada"

    cor_ref = cor_mais_frequente(roi)
    melhor_sim = -1
    melhor_img = None

    for arquivo in os.listdir(pasta_ref):
        if arquivo.lower().endswith((".jpg", ".png", ".jpeg")):
            caminho = os.path.join(pasta_ref, arquivo)
            img = cv2.imread(caminho)
            if img is None:
                continue
            cor_img = cor_mais_frequente(img)
            similaridade, _ = comparar_cores(cor_ref, cor_img)
            if similaridade > melhor_sim:
                melhor_sim = similaridade
                melhor_img = arquivo

    if not melhor_img:
        return "Nenhuma referência encontrada"

    if tipo.lower() == "ph":
        valPH = melhor_img.split(".")[0]
        return f"pH detectado: {valPH}"
    elif tipo.lower() == "amonia":
        if valPH is None:
            return "Erro: analise o pH primeiro"
        amoniaCrit = tab.procurarTab(valPH, melhor_img, temp)
        return f"Amonia Crítica: {amoniaCrit}"

    return f"{tipo.capitalize()} analisado: {melhor_img} ({melhor_sim}%)"