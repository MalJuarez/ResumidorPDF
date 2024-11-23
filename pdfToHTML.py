# Librerías necesarias

import fitz  # PyMuPDF para leer y convertir PDF a HTML
import re
import nltk
from nltk.corpus import stopwords
from nltk import sent_tokenize, word_tokenize
from heapq import nlargest
from googletrans import Translator
from pdfminer.high_level import extract_text

# Descargamos datos necesarios de nltk
nltk.download('punkt')
nltk.download('stopwords')

import os

pdf_path = "c:\\Users\\Usuario\\Downloads\\Anexo V[J].pdf"

if not os.path.isfile(pdf_path):
    print(f"Error: El archivo '{pdf_path}' no se encuentra.")
else:
    print("El archivo se encontró correctamente.")


def PdfToHTML():
    # Insertamos el PDF (nombre de archivo)
    pdf = "c:\\Users\\Usuario\\Downloads\\Anexo V[J].pdf"  # Asegúrate de que el PDF esté en la misma carpeta o usa la ruta completa
    try:
        # Convertir PDF a HTML usando fitz
        doc = fitz.open(pdf)
        with open(f"{pdf}.html", "wb") as salida:
            for pagina in doc:
                texto = pagina.get_text("html").encode("utf8")
                salida.write(texto)
                salida.write(b"\n--------------------\n")
        print("Archivo HTML generado con éxito.")
        doc.close()

        # Pasar al resumen
        PdfToHTML()
    except Exception as e:
        print(f"Error al convertir PDF a HTML: {e}")