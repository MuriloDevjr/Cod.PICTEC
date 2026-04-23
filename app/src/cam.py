import cv2
import numpy as np
import os
from collections import Counter
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000
import lerAmoniaTox as tab

if not hasattr(np, "asscalar"):
    np.asscalar = lambda x: x.item()

valPH = None


def comparar_cores(rgb1, rgb2):
    cor1 = sRGBColor(rgb1[0], rgb1[1], rgb1[2], is_upscaled=True)
    cor2 = sRGBColor(rgb2[0], rgb2[1], rgb2[2], is_upscaled=True)

    cor1_lab = convert_color(cor1, LabColor)
    cor2_lab = convert_color(cor2, LabColor)

    diferenca = delta_e_cie2000(cor1_lab, cor2_lab)
    similaridade = max(0, 100 - diferenca * 2)

    return round(similaridade, 2)


def cor_mais_frequente(imagem):
    img_rgb = cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB)
    pixels = img_rgb.reshape(-1, 3)
    contador = Counter(tuple(int(p) for p in px) for px in pixels)
    return contador.most_common(1)[0][0]


def capturar_com_roi():
    cam = cv2.VideoCapture(0)

    if not cam.isOpened():
        return None

    while True:
        ret, frame = cam.read()
        if not ret:
            cam.release()
            return None

        cv2.imshow("ENTER = capturar | ESC = sair", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == 13:
            break
        elif key == 27:
            cam.release()
            cv2.destroyAllWindows()
            return None

    r = cv2.selectROI("Selecione área", frame, False)
    cv2.destroyAllWindows()
    cam.release()

    x, y, w, h = r
    if w == 0 or h == 0:
        return None

    return frame[y:y+h, x:x+w]


def analisarTipo(tipo, temp=None):
    global valPH

    roi = capturar_com_roi()
    if roi is None:
        return "Erro na captura"

    pasta = tipo.lower()

    if not os.path.exists(pasta):
        return f"Pasta '{pasta}' não encontrada"

    cor_ref = cor_mais_frequente(roi)

    melhor = None
    melhor_sim = -1

    for arq in os.listdir(pasta):
        if arq.endswith((".jpg", ".png")):
            img = cv2.imread(os.path.join(pasta, arq))
            if img is None:
                continue

            cor_img = cor_mais_frequente(img)
            sim = comparar_cores(cor_ref, cor_img)

            if sim > melhor_sim:
                melhor_sim = sim
                melhor = arq

    if melhor is None:
        return "Sem referência"

    valor = melhor.split(".")[0]


    if tipo.lower() == "ph":
        valPH = valor
        return f"pH: {valor}"

    elif tipo.lower() == "amonia":
        if valPH is None:
            return "Analise o pH primeiro"

        if not temp:
            return "Temperatura não informada"

        resultado = tab.procurarTab(valPH, melhor, temp)

        return f"Amonia: {valor} | Temp: {temp} | pH: {valPH} | Critica: {resultado}"

    return f"{tipo}: {valor}"