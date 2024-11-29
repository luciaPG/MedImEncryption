import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

def analizar_correlacion_pixeles(path, num_pares=5000):
    imagen = cv2.imread(path)
    if imagen is None:
        print("No se pudo cargar la imagen. Verifica la ruta.")
        return
    
    altura, ancho, _ = imagen.shape
    pares = []

    for _ in range(num_pares):
        x = np.random.randint(0, altura - 1)
        y = np.random.randint(0, ancho - 1)

        p1 = imagen[x, y]
        p2 = imagen[x, y + 1] if y + 1 < ancho else imagen[x, y]
        pares.append((p1, p2))

    pares = np.array(pares)
    colores = {'Rojo': 'red', 'Verde': 'green', 'Azul': 'blue'}
    fig, axs = plt.subplots(1, 4, figsize=(20, 5))  

    imagen_rgb = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)  
    axs[0].imshow(imagen_rgb)
    axs[0].set_title("Imagen Original")
    axs[0].axis('off')

    for idx, (canal, nombre_canal) in enumerate(zip(range(3), ['Rojo', 'Verde', 'Azul'])):
        valores_canal_p1 = pares[:, 0, canal]
        valores_canal_p2 = pares[:, 1, canal]

        coef_corr, _ = pearsonr(valores_canal_p1, valores_canal_p2)

        axs[idx + 1].scatter(valores_canal_p1, valores_canal_p2, alpha=0.5, s=5, color=colores[nombre_canal])
        axs[idx + 1].set_title(f"{nombre_canal}\nCoef.: {coef_corr:.5f}")
        axs[idx + 1].set_xlabel("Píxel 1")
        axs[idx + 1].set_ylabel("Píxel 2")
        axs[idx + 1].set_xlim(0, 255)
        axs[idx + 1].set_ylim(0, 255)
        axs[idx + 1].grid(True)

    plt.tight_layout()
    plt.show()

analizar_correlacion_pixeles('imagenes/brain.png')
analizar_correlacion_pixeles('imagenes/brain_encrypted.png')

