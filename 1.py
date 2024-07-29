import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import os
import rarfile
from zipfile import ZipFile
from PIL import Image
import io

# Función para seleccionar la ruta de exportación del PDF
def seleccionar_ruta_exportacion():
    global ruta_exportacion
    ruta_exportacion = filedialog.askdirectory()
    if ruta_exportacion:
        messagebox.showinfo("Ruta de Exportación Seleccionada", f"Ruta seleccionada: {ruta_exportacion}")

# Función para abrir la ubicación de exportación
def abrir_ubicacion_exportacion():
    if ruta_exportacion:
        try:
            os.startfile(ruta_exportacion)
        except Exception as e:
            messagebox.showerror("Error al Abrir la Ubicación", f"No se pudo abrir la ubicación: {e}")
    else:
        messagebox.showwarning("Ruta de Exportación no Seleccionada", "Primero selecciona una ruta de exportación")

# Función para seleccionar archivo CBR o CBZ
def seleccionar_archivo():
    global archivo_seleccionado
    archivo_seleccionado = filedialog.askopenfilename(
        title="Seleccionar Archivo",
        filetypes=[("Archivos CBR", ".cbr"), ("Archivos CBZ", ".cbz"), ("Todos los archivos", ".")]
    )
    if archivo_seleccionado:
        messagebox.showinfo("Archivo Seleccionado", f"Has seleccionado: {archivo_seleccionado}")

# Función para convertir CBR o CBZ a PDF y guardar en la ruta de exportación seleccionada
def convertir_a_pdf():
    global ruta_exportacion
    if archivo_seleccionado and ruta_exportacion:
        try:
            images = []
            # Leer archivo CBR
            if archivo_seleccionado.lower().endswith('.cbr'):
                try:
                    with rarfile.RarFile(archivo_seleccionado) as rf:
                        for entry in sorted(rf.infolist(), key=lambda x: x.filename):
                            if entry.filename.endswith(('.jpg', '.jpeg', '.png', '.gif', '.tiff')):
                                with rf.open(entry) as file:
                                    image = Image.open(io.BytesIO(file.read()))
                                    if image.mode != 'RGB':
                                        image = image.convert('RGB')
                                    images.append(image)
                except rarfile.RarCannotExec as e:
                    print(f"Error al procesar archivo CBR: {e}")
                    messagebox.showerror("Error", f"Error al procesar archivo CBR: {e}")
                    return
            # Leer archivo CBZ
            elif archivo_seleccionado.lower().endswith('.cbz'):
                with ZipFile(archivo_seleccionado) as zf:
                    for entry in sorted(zf.infolist(), key=lambda x: x.filename):
                        if entry.filename.endswith(('.jpg', '.jpeg', '.png', '.gif', '.tiff')):
                            with zf.open(entry) as file:
                                image = Image.open(io.BytesIO(file.read()))
                                if image.mode != 'RGB':
                                    image = image.convert('RGB')
                                images.append(image)
            
            if images:
                output_pdf_path = os.path.join(ruta_exportacion, "output.pdf")
                images[0].save(output_pdf_path, save_all=True, append_images=images[1:])
                messagebox.showinfo("Éxito", f'PDF guardado en {output_pdf_path}')
            else:
                messagebox.showwarning("Error", "No se encontraron imágenes en el archivo .cbr o .cbz")
        except Exception as e:
            messagebox.showerror("Error", f"Error al convertir el archivo: {e}")
    else:
        if not archivo_seleccionado:
            messagebox.showwarning("Archivo no seleccionado", "Por favor selecciona un archivo CBR o CBZ primero")
        elif not ruta_exportacion:
            messagebox.showwarning("Ruta de Exportación no Seleccionada", "Por favor selecciona una ruta de exportación")

# Crear la ventana principal
root = tk.Tk()
root.title("Comic to PDF Converter")

# Establecer tamaño de la ventana
root.geometry("400x300")

# Colores fríos
bg_color = "#E0F7FA"  # Fondo de la ventana (menta)
button_bg = "#4FC3F7"  # Fondo del botón (azul claro)
button_fg = "#FFFFFF"  # Color del texto del botón (blanco)

# Configurar el fondo de la ventana
root.configure(bg=bg_color)

# Aplicar estilo
style = ttk.Style()
style.configure('TButton', font=('Helvetica', 12), padding=10)
style.configure('TLabel', font=('Helvetica', 14))

# Crear un título (sin resaltado)
label_titulo = ttk.Label(root, text="Comic to PDF Converter", style='TLabel', background=bg_color)
label_titulo.pack(pady=20)

# Botón para seleccionar la ruta de exportación
botón_ruta_exportacion = ttk.Button(root, text="Seleccionar Ruta de Exportación", command=seleccionar_ruta_exportacion, style='TButton')
botón_ruta_exportacion.pack(pady=10)

# Botón para abrir la ubicación de exportación
botón_abrir_ubicacion = ttk.Button(root, text="Abrir Ubicación de Exportación", command=abrir_ubicacion_exportacion, style='TButton')
botón_abrir_ubicacion.pack(pady=10)

# Botón para seleccionar archivo CBR o CBZ
botón_seleccionar = ttk.Button(root, text="Seleccionar Archivo", command=seleccionar_archivo, style='TButton')
botón_seleccionar.pack(pady=10)

# Botón para convertir a PDF
botón_convertir = ttk.Button(root, text="Convertir a PDF", command=convertir_a_pdf, style='TButton')
botón_convertir.pack(pady=10)

# Variables globales
archivo_seleccionado = None
ruta_exportacion = None

# Ejecutar el bucle principal de la ventana
root.mainloop()

