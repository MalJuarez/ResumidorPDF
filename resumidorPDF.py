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
        Resumen()
    except Exception as e:
        print(f"Error al convertir PDF a HTML: {e}")

def Resumen():
    try:
        # Leer texto del PDF
        pdf_text = extract_text("c:\\Users\\Usuario\\Downloads\\Anexo V[J].pdf")
        if not pdf_text:
            raise ValueError("No se pudo extraer el texto del PDF.")

        # Preprocesamiento del texto
        pdf_text = re.sub(r'\[[0-9]*\]', ' ', pdf_text)
        pdf_text = re.sub(r'\s+', ' ', pdf_text)
        
        print("#########################")
        print("##### R E S U M E N #####")
        print("#########################")

        # Tokenización y eliminación de palabras vacías
        sentences = sent_tokenize(pdf_text)
        formatted_text = re.sub('[^a-zA-Z]', ' ', pdf_text).lower()
        formatted_text = re.sub(r'\s+', ' ', formatted_text)
        stop_words = set(stopwords.words('english'))

        word_frequencies = {}
        for word in word_tokenize(formatted_text):
            if word not in stop_words:
                if word in word_frequencies:
                    word_frequencies[word] += 1
                else:
                    word_frequencies[word] = 1

        # Normalización de frecuencia de palabras
        max_frequency = max(word_frequencies.values())
        word_frequencies = {word: freq / max_frequency for word, freq in word_frequencies.items()}

        # Calcular puntajes de oraciones
        sentence_scores = {}
        for sentence in sentences:
            for word in word_tokenize(sentence.lower()):
                if word in word_frequencies:
                    if len(sentence.split(' ')) < 90:  # Limitar la longitud de la oración
                        if sentence not in sentence_scores:
                            sentence_scores[sentence] = word_frequencies[word]
                        else:
                            sentence_scores[sentence] += word_frequencies[word]

        # Seleccionar las oraciones más importantes
        summary_sentences = nlargest(7, sentence_scores, key=sentence_scores.get)
        summary = ' '.join(summary_sentences)
        print(summary)

        # Traducir el resumen (opcional)
        translator = Translator()
        translated_summary = translator.translate(summary, src="en", dest="es").text

        # Guardar el resumen traducido en un archivo .txt
        with open("Resumen.txt", "w", encoding="utf-8") as resumen_pdf:
            resumen_pdf.write("Resumen del texto:\n" + translated_summary)

        print("Resumen guardado exitosamente en Resumen.txt.")

    except Exception as e:
        print(f"Error al generar el resumen: {e}")

# Ejecutar función principal
PdfToHTML()
