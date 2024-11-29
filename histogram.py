import cv2
import matplotlib.pyplot as plt
import numpy as np

def mostrar_histograma(path, canal):
    imagen = cv2.imread(path)
    if imagen is None:
        print("No se pudo cargar la imagen. Verifica la ruta.")
        return

    canales = {'r': 2, 'g': 1, 'b': 0}
    colormaps = {'r': 'Reds', 'g': 'Greens', 'b': 'Blues'}
    
    if canal not in canales:
        print("Canal inválido. Usa 'r', 'g' o 'b'.")
        return

    canal_imagen = cv2.split(imagen)[canales[canal]]
    histograma = cv2.calcHist([canal_imagen], [0], None, [256], [0, 256])

    fig = plt.figure(figsize=(14, 6))
    gs = fig.add_gridspec(2, 2, height_ratios=[4, 0.5], width_ratios=[1.5, 4])
    
    ax_img = fig.add_subplot(gs[:, 0])
    ax_hist = fig.add_subplot(gs[0, 1])
    ax_grad = fig.add_subplot(gs[1, 1])

    ax_img.imshow(cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB))
    ax_img.axis('off')
    ax_img.set_title("Imagen Original")

    ax_hist.bar(np.arange(256), histograma.flatten(), color=canal, width=1)
    ax_hist.set_title(f"Histograma del Canal {canal.upper()}")
    ax_hist.set_xlabel("Intensidad de píxel")
    ax_hist.set_ylabel("Frecuencia")
    ax_hist.set_xlim([0, 256])

    degradado = np.linspace(0, 1, 256).reshape(1, -1)
    cmap = colormaps[canal]
    ax_grad.imshow(degradado, aspect='auto', cmap=cmap, extent=[0, 256, 0, 1])
    ax_grad.set_axis_off()

    plt.tight_layout()
    plt.show()

mostrar_histograma('imagenes/brain.png', 'r')
mostrar_histograma('imagenes/brain.png', 'r')
