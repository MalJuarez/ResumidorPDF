# Librerías necesarias

import fitz  # PyMuPDF para manejar PDFs
import re  # Para manejar expresiones regulares
import nltk  # Para procesamiento de texto
import heapq  # Para seleccionar las oraciones más relevantes
from bs4 import BeautifulSoup  # Para procesar HTML
from pdfminer.high_level import extract_text  # Si usas pdfminer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize


# Descargamos datos necesarios de nltk
nltk.download('punkt')
nltk.download('stopwords')

import os

html_path = "c:\Users\Usuario\Downloads\METODOLOGÍA\Analisis Estructurado Moderno, Edward Yourdon MET.pdf"  # Cambia el nombre si usas otro archivo HTML

# Verifica que el archivo HTML se haya generado
if os.path.isfile(html_path):
    print(f"Archivo HTML generado correctamente: {html_path}")
else:
    print("Error: El archivo HTML no fue generado.")
    

# Lee el contenido del archivo HTML
with open(html_path, "r", encoding="utf-8") as f:
    html_content = f.read()
    print("Contenido del archivo HTML:")
    print(html_content[:500])  # Muestra los primeros 500 caracteres


def Resumen():
    # Ruta del archivo HTML generado
    html_path = "c:\Users\Usuario\Downloads\METODOLOGÍA\Analisis Estructurado Moderno, Edward Yourdon MET.pdf"  
    
    try:
        # Carga el contenido del archivo HTML
        with open(html_path, "r", encoding="utf-8") as f:
            html_content = f.read()
        
        # Usa BeautifulSoup para extraer texto del HTML
        soup = BeautifulSoup(html_content, "html.parser")
        articulo_texto = soup.get_text()  # Extrae solo el texto
        
        print("Texto extraído del HTML:")
        print(articulo_texto[:500])  # Muestra los primeros 500 caracteres
        
        # Continúa con el proceso de resumen
        articulo_texto = articulo_texto.replace("[ edit ]", "")
        articulo_texto = re.sub(r'\[[0-9]*\]', ' ', articulo_texto)
        articulo_texto = re.sub(r'\s+', ' ', articulo_texto)
        formatear_articulo = re.sub('[^a-zA-Z]', ' ', articulo_texto)
        formatear_articulo = re.sub(r'\s+', ' ', formatear_articulo)
        
        lista_palabras = nltk.sent_tokenize(articulo_texto)
        stopwords = nltk.corpus.stopwords.words('english')
        
        # Calcula frecuencias
        frecuencia_palabras = {}
        for word in nltk.word_tokenize(formatear_articulo):
            if word not in stopwords:
                if word not in frecuencia_palabras.keys():
                    frecuencia_palabras[word] = 1
                else:
                    frecuencia_palabras[word] += 1
        max_frecuencia = max(frecuencia_palabras.values())
        
        for word in frecuencia_palabras.keys():
            frecuencia_palabras[word] = (frecuencia_palabras[word] / max_frecuencia)
        
        # Calcula las frases más relevantes
        max_oracion = {}
        for sent in lista_palabras:
            for word in nltk.word_tokenize(sent.lower()):
                if word in frecuencia_palabras.keys():
                    if len(sent.split(' ')) < 90:  # Ajusta según tu caso
                        if sent not in max_oracion.keys():
                            max_oracion[sent] = frecuencia_palabras[word]
                        else:
                            max_oracion[sent] += frecuencia_palabras[word]
        
        # Resumen final
        resumen_oracion = heapq.nlargest(7, max_oracion, key=max_oracion.get)
        resumen = ' '.join(resumen_oracion)
        print("Resumen generado:")
        print(resumen)
        
        # Guarda el resumen en un archivo TXT
        with open("Resumen.txt", "w", encoding="utf-8") as resumen_file:
            resumen_file.write(resumen)
    
    except Exception as e:
        print(f"Error al generar el resumen: {e}")

# Ejecutar función principal
Resumen()
