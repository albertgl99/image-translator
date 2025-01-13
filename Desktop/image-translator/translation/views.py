import pytesseract
from PIL import Image
from django.shortcuts import render
from decouple import config
import deepl

# Configurar la API de DeepL
DEEPL_API_KEY = config("DEEPL_API_KEY")
translator = deepl.Translator(DEEPL_API_KEY)

# Lista de idiomas soportados por DeepL
VALID_LANGUAGES = {"EN", "ES", "FR", "DE", "IT"}

def translate_image(request):
    if request.method == "POST":
        try:
            # Obtener la imagen y el idioma del formulario
            image = request.FILES.get('image')
            target_language = request.POST.get('language')

            if not image or not target_language:
                return render(request, "translation/translate.html", {
                    "error": "Faltan datos necesarios (imagen o idioma)."
                })

            # Validar el idioma de destino
            if target_language.upper() not in VALID_LANGUAGES:
                return render(request, "translation/translate.html", {
                    "error": "Idioma no soportado."
                })

            # Extraer texto de la imagen usando Tesseract
            img = Image.open(image)
            extracted_text = pytesseract.image_to_string(img)

            # Traducir el texto extraído con DeepL
            translated = translator.translate_text(extracted_text, target_lang=target_language.upper())

            # Renderizar la plantilla con los resultados
            return render(request, "translate.html", {
                "extracted_text": extracted_text,
                "translated_text": translated.text,
            })

        except deepl.exceptions.DeepLException as e:
            return render(request, "translate.html", {
                "error": f"Error con DeepL: {str(e)}"
            })

        except Exception as e:
            return render(request, "translate.html", {
                "error": f"Error inesperado: {str(e)}"
            })

    # Renderizar la página inicial (GET)
    return render(request, "translate.html")
