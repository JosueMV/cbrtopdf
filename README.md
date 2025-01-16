CBR to PDF Converter

Descripción

CBR to PDF Converter es una aplicación que permite convertir archivos CBR y CBZ en archivos PDF. Diseñada con una interfaz gráfica intuitiva, esta herramienta es ideal para gestionar tus cómics digitales y convertirlos a un formato más accesible y universal.

Características

Compatibilidad de formatos: Soporte para archivos CBR (RAR) y CBZ (ZIP).

Manejo de imágenes: Convierte imágenes en formatos como JPG, PNG, TIFF, entre otros, a un archivo PDF.

Interfaz gráfica: Diseñada con tkinter, es simple y fácil de usar.

Barra de progreso: Muestra el estado de las operaciones (importación y conversión).

Selecciona ruta de exportación: Guarda el archivo PDF generado en la ubicación deseada.

Compatible con múltiples idiomas: Configurable para usuarios hispanohablantes.

Requisitos del Sistema

Python 3.7 o superior.

Librerías requeridas:

tkinter

Pillow

rarfile

zipfile

Instalación

Clona este repositorio:

git clone https://github.com/tu-usuario/cbr-to-pdf-converter.git

Instala las dependencias necesarias utilizando pip:

pip install pillow rarfile

Asegúrate de tener instalado un controlador de RAR, como unrar:

En sistemas basados en Linux:

sudo apt install unrar

En Windows, asegúrate de que el ejecutable de unrar esté en tu PATH.

Uso

Ejecuta la aplicación:

python cbr_to_pdf_converter.py

Usa los botones de la interfaz para:

Seleccionar el archivo CBR o CBZ.

Elegir la ruta de exportación para el PDF generado.

Convertir el archivo a PDF.

El archivo PDF se guardará en la ruta especificada.

Capturas de Pantalla

Proporciona capturas de pantalla de la aplicación aquí para mostrar su funcionalidad.

Estructura del Proyecto

CBR-to-PDF-Converter/
├── cbr_to_pdf_converter.py  # Código fuente principal
├── README.md                # Documentación del proyecto
├── requirements.txt         # Lista de dependencias

Contribuciones

Las contribuciones son bienvenidas. Para contribuir:

Haz un fork del repositorio.

Crea una rama con tu función o corrección:

git checkout -b nueva-funcion

Realiza tus cambios y haz un commit:

git commit -m "Agrega nueva funcionalidad"

Sube tus cambios:

git push origin nueva-funcion

Crea un Pull Request.

Licencia

Este proyecto está licenciado bajo la MIT License. Siéntete libre de usar, modificar y compartir.

Autor

Creado por Tu Nombre. Si tienes alguna pregunta o sugerencia, no dudes en contactarme.

Notas

Asegúrate de que los archivos seleccionados contengan imágenes válidas.

La aplicación requiere permisos de escritura en la ruta de exportación especificada.

En caso de errores, revisa los requisitos del sistema y las dependencias instaladas.
