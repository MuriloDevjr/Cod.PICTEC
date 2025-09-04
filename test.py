import numpy as np
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000

# 🔧 Patch para versões novas do NumPy
if not hasattr(np, "asscalar"):
    np.asscalar = lambda x: x.item()

def comparar_cores(rgb1, rgb2):
    """
    Compara duas cores RGB e retorna a similaridade em porcentagem.
    rgb1 e rgb2 devem ser tuplas (R, G, B) no intervalo [0, 255]
    """
    # Converter para objetos sRGB
    cor1 = sRGBColor(rgb1[0], rgb1[1], rgb1[2], is_upscaled=True)
    cor2 = sRGBColor(rgb2[0], rgb2[1], rgb2[2], is_upscaled=True)

    # Converter para Lab
    cor1_lab = convert_color(cor1, LabColor)
    cor2_lab = convert_color(cor2, LabColor)

    # Calcular DeltaE (diferença perceptiva)
    diferenca = delta_e_cie2000(cor1_lab, cor2_lab)

    # Converter em porcentagem de similaridade
    similaridade = max(0, 100 - diferenca * 2)  # ajuste de escala
    return round(similaridade, 2), round(float(diferenca), 2)


# 🔹 Testes
cor_a = (255, 0, 0)   # Vermelho puro
cor_b = (254, 0, 0)   # Vermelho quase igual
cor_c = (0, 255, 0)   # Verde

print(comparar_cores(cor_a, cor_b))  # Deve dar ~99%
print(comparar_cores(cor_a, cor_c))  # Deve dar baixo (~_
