import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import os
import rarfile
from zipfile import ZipFile
from PIL import Image, ImageTk
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

def contar_imagenes():
    imagenes_contadas = 0
    if archivo_seleccionado.lower().endswith('.cbr'):
        with rarfile.RarFile(archivo_seleccionado) as rf:
            for entry in rf.infolist():
                if entry.filename.endswith(('.jpg', '.jpeg', '.png', '.gif', '.tiff')):
                    imagenes_contadas += 1
    elif archivo_seleccionado.lower().endswith('.cbz'):
        with ZipFile(archivo_seleccionado) as zf:
            for entry in zf.infolist():
                if entry.filename.endswith(('.jpg', '.jpeg', '.png', '.gif', '.tiff')):
                    imagenes_contadas += 1
    return imagenes_contadas

# Función para importar imágenes y mostrar progreso
def importar_imagenes():
    try:
        total_imagenes = contar_imagenes()

        # Mostrar estado de procesamiento inicial
        procesando_label.config(text="Procesando archivo", foreground="#000000")
        porcentaje_label.config(text="", foreground="#000000")
        root.update_idletasks()
        
        images = []
        if archivo_seleccionado.lower().endswith('.cbr'):
            with rarfile.RarFile(archivo_seleccionado) as rf:
                for idx, entry in enumerate(sorted(rf.infolist(), key=lambda x: x.filename)):
                    if entry.filename.endswith(('.jpg', '.jpeg', '.png', '.gif', '.tiff')):
                        with rf.open(entry) as file:
                            image = Image.open(io.BytesIO(file.read()))
                            if image.mode != 'RGB':
                                image = image.convert('RGB')
                            images.append(image)
                            # Actualizar progreso de importación
                            progress = int((idx + 1) / total_imagenes * 100)
                            porcentaje_label.config(text=f"{progress} %")
                            root.update_idletasks()
        elif archivo_seleccionado.lower().endswith('.cbz'):
            with ZipFile(archivo_seleccionado) as zf:
                for idx, entry in enumerate(sorted(zf.infolist(), key=lambda x: x.filename)):
                    if entry.filename.endswith(('.jpg', '.jpeg', '.png', '.gif', '.tiff')):
                        with zf.open(entry) as file:
                            image = Image.open(io.BytesIO(file.read()))
                            if image.mode != 'RGB':
                                image = image.convert('RGB')
                            images.append(image)
                            # Actualizar progreso de importación
                            progress = int((idx + 1) / total_imagenes * 100)
                            porcentaje_label.config(text=f"{progress} %")
                            root.update_idletasks()

        # Actualizar indicador después de importar imágenes
        procesando_label.config(text="")
        porcentaje_label.config(text="100 %")
        root.update_idletasks()

        return images
    except Exception as e:
        messagebox.showerror("Error", f"Error al importar imágenes: {e}")
        return None

# Función para convertir imágenes a PDF y mostrar progreso
def convertir_a_pdf(images):
    try:
        if not images:
            messagebox.showwarning("Error", "No se encontraron imágenes para convertir")
            return
        
        # Mostrar estado de conversión inicial
        convirtiendo_label.config(text="Convirtiendo", foreground="#000000")
        estado_label.config(text="En curso", foreground="#0000FF")
        root.update_idletasks()

        base_name = os.path.basename(archivo_seleccionado)[:56]
        output_pdf_path = os.path.join(ruta_exportacion, f"{base_name}_PDF.pdf")

        total_images = len(images)
        for i, img in enumerate(images):
            if i == 0:
                img.save(output_pdf_path, save_all=True, append_images=images[1:])
            progress = int((i + 1) / total_images * 100)
            porcentaje_label.config(text=f"{progress} %")
            root.update_idletasks()
        
        estado_label.config(text="Hecho", foreground="#008000")
        convirtiendo_label.config(text="")
        messagebox.showinfo("Éxito", f'PDF guardado en {output_pdf_path}')
    except Exception as e:
        messagebox.showerror("Error", f"Error al convertir imágenes a PDF: {e}")

# Función para limpiar las etiquetas de estado
def limpiar_etiquetas(event=None):
    procesando_label.config(text="")
    porcentaje_label.config(text="")
    convirtiendo_label.config(text="")
    estado_label.config(text="")

# Crear la ventana principal
root = tk.Tk()
root.title("CBR to PDF Converter")

# Establecer tamaño de la ventana
root.geometry("400x400")

# Colores fríos
bg_color = "#E0F7FA"
button_bg = "#4FC3F7"
button_fg = "#FFFFFF"

# Configurar el fondo de la ventana
root.configure(bg=bg_color)

# Aplicar estilo
style = ttk.Style()
style.configure('TButton', font=('Helvetica', 12), padding=10)
style.configure('TLabel', font=('Helvetica', 14))

# Crear un título
label_titulo = ttk.Label(root, text="CBR to PDF Converter", style='TLabel', background=bg_color)
label_titulo.pack(pady=10)

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
botón_convertir = ttk.Button(root, text="Convertir a PDF", command=lambda: iniciar_conversion(), style='TButton')
botón_convertir.pack(pady=10)

# Etiquetas de estado
procesando_label = ttk.Label(root, text="", style='TLabel', background=bg_color)
procesando_label.pack(pady=5)

porcentaje_label = ttk.Label(root, text="", style='TLabel', background=bg_color)
porcentaje_label.pack(pady=5)

convirtiendo_label = ttk.Label(root, text="", style='TLabel', background=bg_color)
convirtiendo_label.pack(pady=5)

estado_label = ttk.Label(root, text="", style='TLabel', background=bg_color)
estado_label.pack(pady=5)

# Variables globales
archivo_seleccionado = None
ruta_exportacion = None

# Asociar evento de teclado para limpiar etiquetas
root.bind("<Key>", limpiar_etiquetas)

# Función para iniciar el proceso de importación y conversión
def iniciar_conversion():
    global archivo_seleccionado, ruta_exportacion

    if not archivo_seleccionado:
        messagebox.showwarning("Archivo no seleccionado", "Por favor selecciona un archivo CBR o CBZ primero")
        return

    if not ruta_exportacion:
        messagebox.showwarning("Ruta de Exportación no Seleccionada", "Por favor selecciona una ruta de exportación")
        return

    # Importar imágenes
    images = importar_imagenes()

    if images:
        # Convertir a PDF
        convertir_a_pdf(images)

# Ejecutar el bucle principal de la ventana
root.mainloop()
