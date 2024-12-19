import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from PIL import Image, ImageTk
from matplotlib import pyplot as plt
import numpy as np
from algorithm.paper_img_alg import encrypt_image, decrypt_image
from metrics.correlation import analizar_correlacion_pixeles
from metrics.histogram import mostrar_histograma
from roi.algoritmoROB_ROI import process_image
import os


class EncryptionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Medical Images Encryption Tool")
        self.root.geometry("650x900")
        
        self.input_image_path = None
        self.encrypted_image_path = None
        self.decrypted_image_path = None
        
        self.create_widgets()

    def create_widgets(self):
        # titulo y notas
        tk.Label(self.root, text="Medical Images Encryption Tool", font=("Helvetica", 16, "bold")).pack(pady=10)

        self.notes_frame = tk.Frame(self.root, bg="lightyellow", relief="solid", borderwidth=2, width=100)
        self.notes_frame.pack(pady=10)
        self.notes_label = tk.Label(self.notes_frame, text="Aclaraciones:", font=("Helvetica", 12, "bold"), bg="lightyellow")
        self.notes_label.pack(anchor="w")

        self.text_box = tk.Label(self.notes_frame, text="""1. La imagen debe ser de proporción 1:1 (Ej. 256x256, 500x500...).
2. Las dimensiones de la imagen deben ser divisibles por el tamaño del bloque.
3. El número de rondas debe ser múltiplo de 10 (Ej. 10, 20, 30...).
        """, 
        font=("Helvetica", 10), bg="lightyellow", justify="left")
        self.text_box.pack()
        
        # cargar imagen
        tk.Button(self.root, text="Cargar Imagen Original o Encriptada", command=self.load_image).pack(pady=5)
        self.image_label = tk.Label(self.root, text="No se ha seleccionado ninguna imagen.")
        self.image_label.pack()

        ttk.Separator(self.root, orient="horizontal").pack(fill="x", pady=10)
        
        # parametros
        tk.Label(self.root, text="Parámetros Generales:").pack(pady=(5, 5))
        self.block_size_var = tk.IntVar(value=16)
        self.rounds_var = tk.IntVar(value=10)
        tk.Label(self.root, text="Tamaño del Bloque:").pack(pady=(5,5))
        tk.Entry(self.root, textvariable=self.block_size_var).pack()
        tk.Label(self.root, text="Número de Rondas:").pack(pady=5)
        tk.Entry(self.root, textvariable=self.rounds_var).pack()

        # botones de encriptar/desencriptar
        tk.Button(self.root, text="Encriptar Imagen", command=self.encrypt_image).pack(pady=(10,5))
        tk.Button(self.root, text="Desencriptar Imagen", command=self.decrypt_image).pack(pady=5)

        ttk.Separator(self.root, orient="horizontal").pack(fill="x", pady=10)

        # ROB_ROI
        tk.Label(self.root, text="Parámetros de ROB_ROI:").pack(pady=(5, 5))
        self.rob_roi_block_size_var = tk.IntVar(value=16)
        self.rob_roi_threshold_var = tk.IntVar(value=30)
        tk.Label(self.root, text="Tamaño del Bloque (ROB_ROI):").pack(pady=5)
        tk.Entry(self.root, textvariable=self.rob_roi_block_size_var).pack()
        tk.Label(self.root, text="Umbral (Threshold):").pack(pady=5)
        tk.Entry(self.root, textvariable=self.rob_roi_threshold_var).pack()
        tk.Button(self.root, text="Ejecutar Algoritmo ROB_ROI", command=self.show_rob_roi).pack(pady=5)

        ttk.Separator(self.root, orient="horizontal").pack(fill="x", pady=10)
        
        # metrics
        tk.Label(self.root, text="Correlación:").pack(pady=(5, 5))
        tk.Button(self.root, text="Analizar Correlación", command=self.analyze_correlation).pack(pady=5)

        tk.Label(self.root, text="Histogramas:").pack(pady=(10,2))
        histogram_frame = tk.Frame(self.root)
        histogram_frame.pack(pady=5)
        tk.Button(histogram_frame, text="Mostrar Canal Rojo", command=self.show_histogram_red).pack(side="left", padx=5)
        tk.Button(histogram_frame, text="Mostrar Canal Verde", command=self.show_histogram_green).pack(side="left", padx=5)
        tk.Button(histogram_frame, text="Mostrar Canal Azul", command=self.show_histogram_blue).pack(side="left", padx=5)

        

        # salir
        tk.Button(self.root, text="Salir", command=self.root.quit).pack(pady=20)
    
    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Imágenes", "*.jpg;*.png")])
        if file_path:
            self.input_image_path = file_path
            self.image_label.config(text=f"Imagen cargada: {os.path.basename(file_path)}")
        else:
            messagebox.showwarning("Advertencia", "No se seleccionó ninguna imagen.")
    
    def encrypt_image(self):
        if not self.input_image_path:
            messagebox.showerror("Error", "Primero carga una imagen.")
            return
        block_size = self.block_size_var.get()
        rounds = self.rounds_var.get()
        key = np.array([0.1, 0.2, 0.3, 0.4])
        
        base_name = os.path.splitext(os.path.basename(self.input_image_path))[0]
        output_path = f"encrypted-images/encrypted-{base_name}.png"
        os.makedirs("encrypted-images", exist_ok=True)
        
        try:
            encrypt_image(self.input_image_path, block_size, rounds, key, output_path)
            self.encrypted_image_path = output_path
            
            original_image = np.array(Image.open(self.input_image_path).convert("RGB"))
            encrypted_image = np.array(Image.open(output_path).convert("RGB"))
            
            # plot
            plt.figure(figsize=(10, 5))
            plt.subplot(1, 2, 1)
            plt.title("Imagen Original")
            plt.imshow(original_image)
            plt.axis("off")
            
            plt.subplot(1, 2, 2)
            plt.title("Imagen Encriptada")
            plt.imshow(encrypted_image)
            plt.axis("off")
            
            plt.show()

            messagebox.showinfo("Éxito", f"Imagen encriptada guardada en: {output_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al encriptar la imagen: {e}")

    def decrypt_image(self):
        if not self.input_image_path:
            messagebox.showerror("Error", "Primero encripta una imagen.")
            return
        block_size = self.block_size_var.get()
        rounds = self.rounds_var.get()
        key = np.array([0.1, 0.2, 0.3, 0.4]) 
        
        # cambiar nombre
        base_name = os.path.splitext(os.path.basename(self.input_image_path))[0]
        if base_name.startswith("encrypted-"):
            base_name = base_name.replace("encrypted-", "")
        base_name = f"decrypted-{base_name}"
        
        output_path = f"decrypted-images/{base_name}.png"
        os.makedirs("decrypted-images", exist_ok=True)
        
        try:
            decrypt_image(self.input_image_path, block_size, rounds, key, output_path)
            self.decrypted_image_path = output_path

            original_image = np.array(Image.open(self.input_image_path).convert("RGB"))
            decrypted_image = np.array(Image.open(output_path).convert("RGB"))

            # plot
            plt.figure(figsize=(10, 5))
            plt.subplot(1, 2, 1)
            plt.title("Imagen Encriptada")
            plt.imshow(original_image)
            plt.axis("off")
            
            plt.subplot(1, 2, 2)
            plt.title("Imagen Desencriptada")
            plt.imshow(decrypted_image)
            plt.axis("off")
            
            plt.show()

            messagebox.showinfo("Éxito", f"Imagen desencriptada guardada en: {output_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al desencriptar la imagen: {e}")

    
    def analyze_correlation(self):
        if not self.input_image_path:
            messagebox.showerror("Error", "Primero carga una imagen.")
            return
        try:
            analizar_correlacion_pixeles(self.input_image_path)
        except Exception as e:
            messagebox.showerror("Error", f"Error al analizar la correlación: {e}")
    
    def show_histogram_red(self):
        if not self.input_image_path:
            messagebox.showerror("Error", "Primero carga una imagen.")
            return
        try:
            mostrar_histograma(self.input_image_path, 'r')
        except Exception as e:
            messagebox.showerror("Error", f"Error al mostrar el histograma: {e}")
    
    def show_histogram_green(self):
        if not self.input_image_path:
            messagebox.showerror("Error", "Primero carga una imagen.")
            return
        try:
            mostrar_histograma(self.input_image_path, 'g')
        except Exception as e:
            messagebox.showerror("Error", f"Error al mostrar el histograma: {e}")
    
    def show_histogram_blue(self):
        if not self.input_image_path:
            messagebox.showerror("Error", "Primero carga una imagen.")
            return
        try:
            mostrar_histograma(self.input_image_path, 'b')
        except Exception as e:
            messagebox.showerror("Error", f"Error al mostrar el histograma: {e}")

    def show_rob_roi(self):
        if not self.input_image_path:
            messagebox.showerror("Error", "Primero carga una imagen.")
            return

        block_size = self.rob_roi_block_size_var.get()
        threshold = self.rob_roi_threshold_var.get()

        try:
            original_image, roi_result = process_image(self.input_image_path, block_size, threshold)

            # plot
            plt.figure(figsize=(10, 5))
            plt.subplot(1, 2, 1)
            plt.title("Imagen Original")
            plt.imshow(original_image)
            plt.axis("off")

            plt.subplot(1, 2, 2)
            plt.title("Regiones de Interés (ROI)")
            plt.imshow(roi_result, cmap="gray")
            plt.axis("off")

            plt.show()

        except Exception as e:
            messagebox.showerror("Error", f"Error al procesar la imagen con ROB_ROI: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = EncryptionApp(root)
    root.mainloop()
