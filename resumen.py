def resumir_html(html_path):
    try:
        # Carga el contenido del archivo HTML
        with open(html_path, "r", encoding="utf-8") as f:
            html_content = f.read()

        # Usa BeautifulSoup para extraer texto del HTML
        soup = BeautifulSoup(html_content, "html.parser")
        articulo_texto = soup.get_text()  # Extrae solo el texto plano

        print("Texto extraído del HTML (primeros 500 caracteres):")
        print(articulo_texto[:500])  # Muestra los primeros 500 caracteres del texto

        # Preprocesamiento del texto
        articulo_texto = re.sub(r'\[[0-9]*\]', ' ', articulo_texto)  # Elimina referencias tipo [1]
        articulo_texto = re.sub(r'\s+', ' ', articulo_texto)  # Normaliza espacios
        formatear_articulo = re.sub('[^a-zA-Z]', ' ', articulo_texto)  # Elimina caracteres no alfabéticos
        formatear_articulo = re.sub(r'\s+', ' ', formatear_articulo)  # Normaliza espacios nuevamente

        # Tokenización y cálculo de frecuencia de palabras
        lista_palabras = nltk.sent_tokenize(articulo_texto)
        stopwords_ingles = set(stopwords.words('english'))
        frecuencia_palabras = {}

        for word in nltk.word_tokenize(formatear_articulo):
            if word.lower() not in stopwords_ingles:
                frecuencia_palabras[word] = frecuencia_palabras.get(word, 0) + 1

        # Normaliza las frecuencias
        max_frecuencia = max(frecuencia_palabras.values())
        for word in frecuencia_palabras.keys():
            frecuencia_palabras[word] /= max_frecuencia

        # Calcula las frases más relevantes
        max_oracion = {}
        for sent in lista_palabras:
            for word in nltk.word_tokenize(sent.lower()):
                if word in frecuencia_palabras.keys():
                    max_oracion[sent] = max_oracion.get(sent, 0) + frecuencia_palabras[word]

        # Selecciona las 7 frases más relevantes
        resumen_oracion = heapq.nlargest(7, max_oracion, key=max_oracion.get)
        resumen = ' '.join(resumen_oracion)

        print("Resumen generado:")
        print(resumen)

        # Guarda el resumen en un archivo de texto
        resumen_path = "Resumen.txt"
        with open(resumen_path, "w", encoding="utf-8") as resumen_file:
            resumen_file.write("Resumen del texto:\n")
            resumen_file.write(resumen)

        print(f"Resumen guardado correctamente en: {resumen_path}")

    except Exception as e:
        print(f"Error al generar el resumen: {e}")
        exit()


# Ejecutar el flujo principal
html_path = pdf_to_html(pdf_path)  # Convierte el PDF a HTML
resumir_html(html_path)  # Genera el resumen a partir del HTML