import openai
import os
import fitz

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

RUTA_DOCUMENTO = os.path.join(os.getcwd() ,"actual IPS.pdf")

print(f"📂 Buscando el archivo en: {RUTA_DOCUMENTO}")

def leer_documento(ruta_archivo):
    
    try:
        with fitz.open(ruta_archivo) as doc:
            contenido = ""
            for pagina in doc:
                contenido += pagina.get_text("text")+"\n"

            return contenido if contenido.strip() else "El documento está vacío."
    except Exception as e:
        return f"Error al leer el archivo: {str(e)}"

def analizar_documento(contenido):
    
    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "Eres un asistente experto en análisis de documentos y dar respuestas en español y sensatas."},
                {"role": "user", "content": f"Dame detalles del tratamiento de sueroterapia:\n\n{contenido}"}
            ],
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error al procesar el documento: {str(e)}"

contenido = leer_documento(RUTA_DOCUMENTO)

if contenido.startswith("Error"):
    print(contenido)
else:
    resultado = analizar_documento(contenido)
    print("Resumen del documento:")
    print(resultado)