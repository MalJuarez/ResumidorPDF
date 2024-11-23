import fitz 
import os

pdf = "Analisis Estructurado Moderno, Edward Yourdon MET.pdf"
if not os.path.exists(pdf):
    print(f"Archivo no encontrado: {pdf}")
else:
    # Continúa con el proceso
    print("El archivo existe. Continuando...")
def PdfToHTML():
    # Insertamos el PDF (nombre de archivo)
    pdf = "Analisis Estructurado Moderno, Edward Yourdon MET.pdf"  # Asegúrate de que el PDF esté en la misma carpeta o usa la ruta completa
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