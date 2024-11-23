import fitz  # PyMuPDF para manejar PDFs
import re  # Para expresiones regulares
import nltk  # Para procesamiento de lenguaje natural
import heapq  # Para seleccionar frases más relevantes
from bs4 import BeautifulSoup  # Para procesar texto HTML
from pdfminer.high_level import extract_text  # Para extraer texto de PDF
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import os  # Para manejar rutas y verificar archivos

# Descargamos datos necesarios de nltk
nltk.download('punkt')
nltk.download('stopwords')

# Ruta del archivo PDF
pdf_path = "c:/Users/Usuario/Downloads/METODOLOGÍA/Analisis Estructurado Moderno, Edward Yourdon MET.pdf"

# Verifica si el archivo existe
if os.path.isfile(pdf_path):
    print(f"Archivo encontrado correctamente: {pdf_path}")
else:
    print(f"Error: El archivo no fue encontrado en la ruta especificada: {pdf_path}")
    exit()  # Termina el programa si no encuentra el archivo


# Función para convertir PDF a HTML
def pdf_to_html(pdf_path):
    try:
        doc = fitz.open(pdf_path)
        html_path = pdf_path + ".html"  # Generará un archivo HTML con la misma base del PDF

        with open(html_path, "wb") as salida:
            for pagina in doc:
                texto_html = pagina.get_text("html").encode("utf-8")
                salida.write(texto_html)
                salida.write(b"\n--------------------\n")

        print(f"Archivo HTML generado correctamente: {html_path}")
        return html_path

    except Exception as e:
        print(f"Error al convertir PDF a HTML: {e}")
        exit()
